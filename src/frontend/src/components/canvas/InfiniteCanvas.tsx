import { useEffect, useRef, useCallback, useState } from 'react';
import { useFabricCanvas } from '../../hooks/useFabricCanvas';
import { useCanvasStore } from '../../store';
import { DESIGN_TOKENS, LIMITS } from '../../types';
import './InfiniteCanvas.css';

/**
 * 无限画布组件
 */
export function InfiniteCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Store 状态
  const { isPanning, setPanning, togglePanMode } = useCanvasStore();

  // Fabric 画布 Hook
  const { canvas, viewport, resize, setZoom, pan, addImage, addText, deleteSelected } =
    useFabricCanvas(canvasRef, {
      width: window.innerWidth,
      height: window.innerHeight,
      backgroundColor: DESIGN_TOKENS.canvas.bg,
      onViewportChange: () => {},
    });

  // 本地状态
  const [isDragging, setIsDragging] = useState(false);
  const [lastMousePos, setLastMousePos] = useState({ x: 0, y: 0 });
  const [isSpacePressed, setIsSpacePressed] = useState(false);

  /**
   * 初始化：设置画布大小和事件监听
   */
  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        resize(containerRef.current.clientWidth, containerRef.current.clientHeight);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [resize]);

  /**
   * 键盘快捷键
   */
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // 空格键：临时平移模式（按住时生效，松开恢复）
      if (e.code === 'Space' && !e.repeat) {
        e.preventDefault();
        setIsSpacePressed(true);
      }

      // Delete/Backspace：删除选中元素
      if ((e.code === 'Delete' || e.code === 'Backspace') && canvas) {
        const activeObject = canvas.getActiveObject();
        if (activeObject && !(activeObject as any).isEditing) {
          e.preventDefault();
          deleteSelected();
        }
      }

      // ESC：退出平移模式（工具栏切换的）并取消选择
      if (e.code === 'Escape') {
        setPanning(false);
        if (canvas) {
          canvas.discardActiveObject();
          canvas.requestRenderAll();
        }
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.code === 'Space') {
        setIsSpacePressed(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [canvas, setPanning, deleteSelected]);

  /**
   * 根据平移状态更新 Fabric.js 画布的可选择性
   */
  useEffect(() => {
    if (!canvas) return;

    // 按住空格 或 工具栏平移模式开启时，禁用选择
    const shouldDisableSelection = isSpacePressed || isPanning;

    canvas.selection = !shouldDisableSelection;

    // 禁用所有对象的选择和拖动
    canvas.getObjects().forEach((obj) => {
      obj.selectable = !shouldDisableSelection;
      obj.evented = !shouldDisableSelection;
    });

    canvas.requestRenderAll();
  }, [canvas, isSpacePressed, isPanning]);

  /**
   * 实际的平移状态（空格按住 或 工具栏模式开启）
   */
  const isActuallyPanning = isSpacePressed || isPanning;

  /**
   * 鼠标按下
   */
  const handleMouseDown = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      // 平移模式或中键：开始拖拽
      if (isActuallyPanning || e.button === 1) {
        setIsDragging(true);
        setLastMousePos({ x: e.clientX, y: e.clientY });
      }
    },
    [isActuallyPanning]
  );

  /**
   * 鼠标移动
   */
  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (isDragging) {
        const dx = e.clientX - lastMousePos.x;
        const dy = e.clientY - lastMousePos.y;
        pan(dx, dy);
        setLastMousePos({ x: e.clientX, y: e.clientY });
      }

      // 更新鼠标样式
      if (isActuallyPanning) {
        (e.currentTarget as HTMLDivElement).style.cursor = isDragging ? 'grabbing' : 'grab';
      } else {
        (e.currentTarget as HTMLDivElement).style.cursor = 'default';
      }
    },
    [isDragging, isActuallyPanning, lastMousePos, pan]
  );

  /**
   * 鼠标释放
   */
  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  /**
   * 鼠标滚轮：缩放
   */
  const handleWheel = useCallback(
    (e: React.WheelEvent<HTMLDivElement>) => {
      e.preventDefault();

      const zoomDelta = e.deltaY > 0 ? -0.1 : 0.1;
      const newZoom = Math.max(
        LIMITS.minZoom,
        Math.min(LIMITS.maxZoom, viewport.zoom + zoomDelta)
      );

      setZoom(newZoom, { x: e.clientX, y: e.clientY });
    },
    [viewport.zoom, setZoom]
  );

  /**
   * 添加文字
   */
  const handleAddText = useCallback(() => {
    // 将屏幕中心坐标转换为画布坐标
    // viewport.x = -vpt[4], 所以 vpt[4] = -viewport.x
    // CanvasX = (ScreenX - vpt[4]) / zoom = (ScreenX + viewport.x) / zoom
    const x = (window.innerWidth / 2 + viewport.x) / viewport.zoom;
    const y = (window.innerHeight / 2 + viewport.y) / viewport.zoom;
    addText('双击编辑文字', { x, y });
  }, [addText, viewport]);

  /**
   * 触发图片上传
   */
  const handleUploadClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  /**
   * 处理图片文件选择
   */
  const handleFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file) return;

      // 读取图片
      const reader = new FileReader();
      reader.onload = (event) => {
        const url = event.target?.result as string;
        // 将屏幕中心坐标转换为画布坐标
        const x = (window.innerWidth / 2 + viewport.x) / viewport.zoom;
        const y = (window.innerHeight / 2 + viewport.y) / viewport.zoom;
        addImage(url, { x, y });
      };
      reader.readAsDataURL(file);

      // 重置 input
      e.target.value = '';
    },
    [viewport, addImage]
  );

  /**
   * 处理文件拖拽
   */
  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();

      const file = e.dataTransfer.files[0];
      if (!file || !file.type.startsWith('image/')) return;

      const reader = new FileReader();
      reader.onload = (event) => {
        const url = event.target?.result as string;
        // 将屏幕坐标转换为画布坐标
        const x = (e.clientX + viewport.x) / viewport.zoom;
        const y = (e.clientY + viewport.y) / viewport.zoom;
        addImage(url, { x, y });
      };
      reader.readAsDataURL(file);
    },
    [viewport, addImage]
  );

  return (
    <div
      ref={containerRef}
      className="infinite-canvas-container"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <canvas ref={canvasRef} />

      {/* 隐藏的文件输入 */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />

      {/* 工具栏 */}
      <div className="canvas-toolbar">
        {/* 工具组 */}
        <div className="toolbar-group">
          <button onClick={handleAddText} className="toolbar-button" title="添加文字">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M4 7V4h16v3M9 20h6M12 4v16" strokeLinecap="round" />
            </svg>
            <span>文字</span>
          </button>
          <button onClick={handleUploadClick} className="toolbar-button" title="上传图片">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <circle cx="9" cy="9" r="2" fill="currentColor" />
              <path d="M21 15l-5-5L5 21" />
            </svg>
            <span>图片</span>
          </button>
          <button onClick={deleteSelected} className="toolbar-button" title="删除选中 (Delete)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" strokeLinecap="round" />
            </svg>
            <span>删除</span>
          </button>
        </div>

        <div className="toolbar-divider" />

        {/* 视图组 */}
        <div className="toolbar-group">
          <button
            onClick={togglePanMode}
            className={`toolbar-button ${isPanning ? 'active' : ''}`}
            title="切换平移模式 (或按住空格临时平移)"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 9l-3 3 3 3M9 5l3-3 3 3M19 9l3 3-3 3M9 19l3 3 3-3M2 12h20M12 2v20" strokeLinecap="round" />
            </svg>
            <span>{isPanning ? '平移中' : '平移'}</span>
          </button>
          <button
            onClick={() => setZoom(Math.max(LIMITS.minZoom, viewport.zoom - 0.1))}
            className="toolbar-button icon-only"
            title="缩小"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14" strokeLinecap="round" />
            </svg>
          </button>
          <span className="zoom-display">{Math.round(viewport.zoom * 100)}%</span>
          <button
            onClick={() => setZoom(Math.min(LIMITS.maxZoom, viewport.zoom + 0.1))}
            className="toolbar-button icon-only"
            title="放大"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 5v14M5 12h14" strokeLinecap="round" />
            </svg>
          </button>
        </div>

        <div className="toolbar-divider" />

        {/* 更多 */}
        <div className="toolbar-group">
          <button className="toolbar-button icon-only" title="更多选项">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="1" fill="currentColor" />
              <circle cx="19" cy="12" r="1" fill="currentColor" />
              <circle cx="5" cy="12" r="1" fill="currentColor" />
            </svg>
          </button>
        </div>
      </div>

      {/* 平移模式提示 */}
      {isActuallyPanning && (
        <div className="pan-mode-indicator">
          {isSpacePressed ? '松开空格退出平移' : '按 ESC 退出平移模式'}
        </div>
      )}

      {/* 拖拽提示 */}
      <div className="drag-hint">
        拖拽图片到画布上传
      </div>
    </div>
  );
}
