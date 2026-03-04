// ==================== 类型定义 ====================

/** 画布元素类型 */
export type CanvasItemType = 'text' | 'image';

/** 基础画布元素 */
export interface BaseCanvasItem {
  id: string;
  type: CanvasItemType;
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: number;
}

/** 文字元素 */
export interface TextNoteItem extends BaseCanvasItem {
  type: 'text';
  content: string;
  fontSize: number;
  color: string;
  fontFamily: string;
  minWidth: number;
  minHeight: number;
}

/** 图片元素 */
export interface ImageItem extends BaseCanvasItem {
  type: 'image';
  url: string;
  file?: File;
  originalWidth?: number;
  originalHeight?: number;
}

/** 画布元素 */
export type CanvasItem = TextNoteItem | ImageItem;

/** 视口状态 */
export interface Viewport {
  x: number;
  y: number;
  zoom: number;
}

// ==================== 设计系统 ====================

/** 设计 tokens - 字节跳动风格 */
export const DESIGN_TOKENS = {
  // 主色 - 飞书蓝
  primary: {
    main: '#1f71ff',
    hover: '#1a63e6',
    active: '#1557cc',
    light: '#e6f0ff',
    lighter: '#f0f6ff',
  },
  // 语义色
  semantic: {
    success: '#00b628',
    warning: '#ff8800',
    error: '#f54a45',
    info: '#1f71ff',
  },
  // 背景
  bg: {
    primary: '#ffffff',
    secondary: '#f5f6f7',
    tertiary: '#ebecef',
    overlay: 'rgba(0, 0, 0, 0.45)',
  },
  // 边框
  border: {
    light: '#e5e6eb',
    default: '#dfe1e6',
    dark: '#c5c9d0',
  },
  // 文字
  text: {
    primary: '#1f2329',
    secondary: '#646a73',
    tertiary: '#8f959e',
    quaternary: '#c9cdd4',
    inverse: '#ffffff',
  },
  // 画布专用
  canvas: {
    bg: '#f5f6f7',
    grid: '#e5e6eb',
    selection: '#1f71ff',
    selectionBg: 'rgba(31, 113, 255, 0.1)',
  },
} as const;

/** 圆角系统 */
export const RADIUS = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
  full: '9999px',
} as const;

/** 阴影系统 */
export const SHADOWS = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.04), 0 1px 6px -1px rgba(0, 0, 0, 0.04)',
  md: '0 2px 4px rgba(0, 0, 0, 0.06), 0 4px 12px -2px rgba(0, 0, 0, 0.08)',
  lg: '0 4px 8px rgba(0, 0, 0, 0.08), 0 8px 24px -4px rgba(0, 0, 0, 0.12)',
  xl: '0 8px 16px rgba(0, 0, 0, 0.1), 0 16px 48px -8px rgba(0, 0, 0, 0.14)',
} as const;

/** 间距系统 */
export const SPACING = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
  xxl: '32px',
} as const;

/** 动画缓动函数 */
export const EASING = {
  standard: 'cubic-bezier(0.4, 0, 0.2, 1)',
  decelerate: 'cubic-bezier(0, 0, 0.2, 1)',
  accelerate: 'cubic-bezier(0.4, 0, 1, 1)',
} as const;

/** 动画时长 */
export const DURATION = {
  fast: 150,
  normal: 200,
  slow: 300,
} as const;

// ==================== 旧常量（兼容） ====================

/** @deprecated 使用 DESIGN_TOKENS.canvas */
export const COLORS = {
  background: '#f5f6f7',
  grid: '#e5e6eb',
  selection: '#1f71ff',
  text: '#1f2329',
} as const;

/** 画布尺寸限制 */
export const LIMITS = {
  minZoom: 0.1,
  maxZoom: 5,
  defaultFontSize: 16,
  minTextWidth: 120,
} as const;
