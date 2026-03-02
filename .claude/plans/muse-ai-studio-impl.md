# Implementation Plan: MUSE AI Studio Demo v0.1

## Context

The MUSE AI Studio project has a solid foundation with AI provider implementations (LLM, Image, Video), but lacks the application layer. This plan implements the Demo v0.1 PRD requirements to create an end-to-end fashion content creation and consumption platform.

**Current State:**
- Provider layer: Complete (Zhipu, Gemini, 302.AI for LLM/Image/Video)
- FastAPI backend: Empty (`main.py`)
- Database models: Empty (`models.py`)
- Frontend components: Scaffold only

**Goal:** Deliver a working demo in 1 week with complete Studio → Pick Board → Feedback loop.

---

## Task Type
- [x] Fullstack (→ Parallel development)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React + Vite)                 │
├─────────────────────────────────────────────────────────────┤
│  Studio Dashboard              │  Pick Board                 │
│  - Home (metrics + list)       │  - Feed (waterfall)         │
│  - Asset Pool (upload)         │  - Detail view              │
│  - Canvas (drag-drop)          │  - Interactions             │
│  - Generation Panel            │                              │
│  - Results Panel               │                              │
│  - Settings                    │                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
├─────────────────────────────────────────────────────────────┤
│  /api/designs     /api/outfits     /api/generations         │
│  /api/assets      /api/feed        /api/interactions        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Services Layer (Business Logic)                 │
├─────────────────────────────────────────────────────────────┤
│  DesignService  OutfitService  GenerationService            │
│  AssetService   FeedService    InteractionService           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              AI Provider Layer (Already Done)                │
├─────────────────────────────────────────────────────────────┤
│  LLM Providers    Image Providers    Video Providers         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                       │
├─────────────────────────────────────────────────────────────┤
│  users  designs  outfits  generations  media  interactions  │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Phase 1: Foundation (Days 1-2)

#### Step 1.1: Database Models & Schemas
**Files:** `backend/app/models.py`, `backend/app/schemas.py`

Create ORM models and Pydantic schemas:

```python
# models.py - Core tables
- User (id, name, role, created_at)
- Design (id, user_id, name, status, created_at)
- Asset (id, design_id, url, tags: category/color/season/style, created_at)
- Outfit (id, design_id, items: JSON, description, created_at)
- Generation (id, outfit_id, type, status, params: JSON, result_urls: JSON, created_at)
- Media (id, generation_id, url, type: image/video, is_published, created_at)
- Interaction (id, media_id, user_id, type: like/save/tryon/select/comment, content, created_at)
```

#### Step 1.2: FastAPI Application Setup
**Files:** `backend/app/main.py`

```python
- CORS middleware for frontend
- SQLAlchemy session dependency
- Exception handlers
- Health check endpoint
- Mount static files for generated media
```

#### Step 1.3: Database Migration
**Files:** `backend/scripts/init_db.py`

```bash
- Create alembic migration
- Run initial schema creation
- Seed test data
```

---

### Phase 2: Backend Services (Days 2-3)

#### Step 2.1: Design Service
**Files:** `backend/app/services/design_service.py`

```python
class DesignService:
    - create_design(name, user_id)
    - list_designs(user_id)
    - get_design(design_id)
    - delete_design(design_id)
    - get_metrics(design_id) → content_count, total_likes
```

#### Step 2.2: Asset Service
**Files:** `backend/app/services/asset_service.py`

```python
class AssetService:
    - upload_asset(file, design_id) → URL
    - list_assets(design_id)
    - delete_asset(asset_id)
    - auto_tag_image(asset_id) → uses Vision model
```

#### Step 2.3: Outfit Service
**Files:** `backend/app/services/outfit_service.py`

```python
class OutfitService:
    - create_outfit(design_id, item_ids)
    - generate_suggestions(outfit_id) → uses LLM
    - update_outfit(outfit_id, items)
    - get_outfit(outfit_id)
```

#### Step 2.4: Generation Service
**Files:** `backend/app/services/generation_service.py`

```python
class GenerationService:
    - create_generation(outfit_id, params) → enqueue job
    - process_generation(generation_id) → calls Image/Video providers
    - get_generation_status(generation_id) → queuing/processing/completed/failed
    - list_results(outfit_id)
```

#### Step 2.5: Feed & Interaction Services
**Files:** `backend/app/services/feed_service.py`, `backend/app/services/interaction_service.py`

```python
class FeedService:
    - get_feed(page, limit) → published media
    - get_media_detail(media_id)

class InteractionService:
    - like(media_id, user_id)
    - save(media_id, user_id)
    - comment(media_id, user_id, content)
    - get_metrics(media_id) → likes, saves, comments count
```

---

### Phase 3: API Routes (Day 3)

#### Step 3.1: Studio Dashboard Routes
**Files:** `backend/app/api/routes/designs.py`, `backend/app/api/routes/generations.py`

```python
# Design routes
GET    /api/designs              → list designs
POST   /api/designs              → create design
GET    /api/designs/{id}         → get design
DELETE /api/designs/{id}         → delete design
GET    /api/designs/{id}/metrics → get metrics

# Asset routes
POST   /api/designs/{id}/assets  → upload asset
GET    /api/designs/{id}/assets  → list assets

# Outfit routes
POST   /api/designs/{id}/outfits → create outfit
POST   /api/outfits/{id}/suggest → AI suggestions

# Generation routes
POST   /api/outfits/{id}/generate → trigger generation
GET    /api/generations/{id}      → get status
GET    /api/outfits/{id}/results  → list results
POST   /api/media/{id}/publish    → publish to Pick Board
```

#### Step 3.2: Pick Board Routes
**Files:** `backend/app/api/routes/feed.py`, `backend/app/api/routes/interactions.py`

```python
# Feed routes
GET /api/feed?page=1&limit=20         → get feed
GET /api/media/{id}                   → get detail

# Interaction routes
POST /api/media/{id}/like             → toggle like
POST /api/media/{id}/save             → toggle save
POST /api/media/{id}/comment          → add comment
GET  /api/media/{id}/metrics          → get metrics
```

---

### Phase 4: Frontend - Studio Dashboard (Days 3-4)

#### Step 4.1: State Management
**Files:** `frontend/src/store/designStore.ts`, `frontend/src/store/assetStore.ts`

```typescript
// Zustand stores
- designStore: current design, designs list, metrics
- assetStore: assets list, upload status
- outfitStore: current outfit, suggestions
- generationStore: generation jobs, results
```

#### Step 4.2: Home Page
**Files:** `frontend/src/pages/studio/Home.tsx`

```tsx
- Metrics cards (content count, total likes)
- Design list with thumbnails
- "New Design" button → navigate to canvas
```

#### Step 4.3: Asset Pool
**Files:** `frontend/src/pages/studio/AssetPool.tsx`

```tsx
- Upload area (drag & drop + file picker)
- Asset grid with thumbnails
- Tag display (category, color, season, style)
- Delete button
```

#### Step 4.4: Canvas Workspace
**Files:** `frontend/src/pages/studio/Canvas.tsx`, `frontend/src/components/CanvasEditor.tsx`

```tsx
- Left sidebar: Asset pool (draggable items)
- Center: Canvas area (drop zone, 2-6 items)
- Right sidebar: Current outfit items list
- "Generate Suggestions" button
- "Start Shoot" button → open generation panel
```

Use `@dnd-kit` or `react-grid-layout` for drag-drop.

#### Step 4.5: Generation Panel
**Files:** `frontend/src/components/GenerationPanel.tsx`

```tsx
- Model selection (dropdown or presets)
- Scene selection (dropdown or presets)
- Custom instruction input
- Generate button
- Job queue with status indicators
- Results gallery
- Accept/Reject buttons
- Publish to Pick Board button
```

#### Step 4.6: Settings Page
**Files:** `frontend/src/pages/studio/Settings.tsx`

```tsx
- Model selection (Gemini model)
- System prompt editor
- Version display
```

---

### Phase 5: Frontend - Pick Board (Days 4-5)

#### Step 5.1: Feed Page
**Files:** `frontend/src/pages/pickboard/Feed.tsx`

```tsx
- Waterfall layout (masonry-grid)
- Content cards (image, outfit items preview)
- Infinite scroll pagination
- Like/Save buttons on cards
```

Use `react-masonry-css` or similar.

#### Step 5.2: Content Detail Modal
**Files:** `frontend/src/components/MediaDetail.tsx`

```tsx
- Full-size image/video
- Outfit items list with thumbnails
- Style description
- Like/Save/Tryon/Select buttons
- Comments section
```

#### Step 5.3: Interaction Components
**Files:** `frontend/src/components/InteractionButtons.tsx`

```tsx
- Like button (with counter)
- Save/Collect button
- Try On button
- Select Item button
```

---

### Phase 6: Integration & Testing (Days 5-6)

#### Step 6.1: End-to-End Flow Testing
```
1. Create design → upload assets
2. Create outfit → drag items to canvas
3. Generate suggestions → view AI descriptions
4. Trigger shoot → monitor job queue
5. View results → accept images
6. Publish to Pick Board
7. Browse feed → like/save content
8. Check Studio metrics → verify feedback
```

#### Step 6.2: Error Handling
- Loading states for all async operations
- Error messages for failed generations
- Retry mechanisms
- Offline handling

#### Step 6.3: Demo Preparation
- Seed sample data
- Test 15-minute continuous demo
- Prepare demo script

---

### Phase 7: Polish & Documentation (Day 7)

#### Step 7.1: UI Polish
- Consistent styling (use shadcn/ui or similar)
- Loading animations
- Success/error toasts
- Responsive design

#### Step 7.2: Documentation
- API documentation (OpenAPI)
- Deployment guide
- Demo script

---

## Key Files Summary

| File | Operation | Description |
|------|-----------|-------------|
| `backend/app/models.py` | Create | Database ORM models |
| `backend/app/schemas.py` | Create | Pydantic request/response schemas |
| `backend/app/main.py` | Modify | FastAPI app setup with routes |
| `backend/app/services/*.py` | Create | Business logic services |
| `backend/app/api/routes/*.py` | Create | API route handlers |
| `frontend/src/store/*.ts` | Create | Zustand state management |
| `frontend/src/pages/studio/*.tsx` | Modify/Implement | Studio dashboard pages |
| `frontend/src/pages/pickboard/*.tsx` | Modify/Implement | Pick Board pages |
| `frontend/src/components/*.tsx` | Modify/Implement | Reusable components |
| `frontend/src/api.ts` | Modify | API client functions |

---

## Risks and Mitigation

| Risk | Mitigation |
|------|------------|
| AI generation slow/unreliable | Implement async job queue, show progress, allow retry |
| Drag-drop complexity | Use proven library (@dnd-kit), simplify to click-select first |
| Database migration issues | Use Alembic, test migrations locally first |
| Frontend state management complexity | Use Zustand for simplicity, keep state flat |
| Demo time constraint | Prioritize P0 features only, defer P1 enhancements |
| Provider API rate limits | Add rate limiting, queue management, fallback providers |

---

## Dependencies to Install

### Backend
```bash
# Already present providers, add:
pip install alembic sqlalchemy-utils
pip install aiofiles  # async file upload
pip install celery redis  # optional: for job queue
```

### Frontend
```bash
npm install @dnd-kit/core @dnd-kit/sortable
npm install @tanstack/react-query
npm install react-masonry-css
npm install zustand
npm install lucide-react  # icons
npm install clsx tailwind-merge  # styling
```

---

## Verification (Demo Success Criteria)

- [ ] Complete at least 1 end-to-end creation chain (import → create → generate → publish)
- [ ] Pick Board displays published content
- [ ] Users can generate real interactions (like, save, comment)
- [ ] Studio shows feedback data from Pick Board
- [ ] Core workflow stable for ≥15 minute demo
- [ ] No blocking errors in key pages
- [ ] Real-time data updates working

---

*Plan generated based on PRD v0.1 and current codebase state*
