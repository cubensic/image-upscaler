# TODO List for Image Upscaling Web App

## 1. Repository & Environment Setup
- [ ] Initialize Git repository  
- [ ] Create `dev` and `main` branches  
- [ ] Add `.gitignore` (Python, environment files, `__pycache__`, etc.)  
- [ ] Create Python virtual environment  
- [ ] Install backend dependencies:
  - fastapi  
  - uvicorn  
  - python-multipart  
- [ ] Create `.env.development` and `.env.production` files  
- [ ] Add README with project overview and setup instructions

## 2. Directory Structure
- [ ] Create folder structure:
  ```
  /app
    ├── main.py
    ├── api/
    └── static/
        ├── index.html
        ├── styles.css
        └── script.js
  /tests
  vercel.json
  ```
- [ ] Ensure `app/static` is served as static assets

## 3. Backend Implementation (FastAPI)
- [ ] In `app/main.py`, initialize FastAPI app  
- [ ] Mount static files directory for `/`  
- [ ] Create `POST /api/upscale` endpoint:
  - Accept `multipart/form-data` field `image`  
  - Server-side validation:
    - Check file exists  
    - Check MIME type (jpg, png, webp)  
    - Check size ≤ 5 MB  
    - Return `400` with JSON error on failure  
  - Stub AI upscaling call:
    - Log receipt of file  
    - (Placeholder) simulate processing delay  
  - Return binary PNG image with `200 OK`  
- [ ] Add console logging for:
  - Incoming requests  
  - Validation failures  
  - Stub processing steps

## 4. Frontend Implementation
### 4.1 index.html
- [ ] Basic HTML5 skeleton  
- [ ] Include dropzone container, status area, result viewer  
- [ ] Link `styles.css` and `script.js`

### 4.2 styles.css
- [ ] Centered, responsive layout  
- [ ] Styles for:
  - Drop zone (hover, active states)  
  - Progress indicator  
  - Notification banner (error/success colors)  
  - Result viewer & download button  

### 4.3 script.js
- [ ] Implement **DragDropZone**:
  - Handle `dragenter`/`dragleave`/`drop`  
  - Fallback click-to-select ``  
- [ ] Client-side validation:
  - File type  
  - File size ≤ 5 MB  
  - Show inline errors via NotificationBanner  
- [ ] Implement **ProgressIndicator**:
  - States: idle, uploading, processing, done  
- [ ] POST to `/api/upscale` using Fetch API:
  - Send `FormData` with `image`  
  - Handle binary response as Blob  
- [ ] Implement **ResultViewer**:
  - Display returned image in ``  
  - Create "Download" link with `URL.createObjectURL(blob)`  
- [ ] Implement **NotificationBanner** for:
  - Validation errors  
  - Network/API errors  
- [ ] Add `console.log()` calls for:
  - File selection  
  - Upload start/end  
  - API response status  

## 5. Testing
- [ ] Add `pytest` to dev dependencies  
- [ ] Write tests in `/tests/test_api.py`:
  - Upload with no file → 400  
  - Upload unsupported type → 400  
  - Upload too large → 400  
  - Upload valid file → 200 + correct `Content-Type`  
- [ ] Run `pytest` locally and ensure all pass

## 6. Deployment Configuration
- [ ] Create `vercel.json`:
  ```
  {
    "functions": {
      "api/**/*.py": { "runtime": "vercel-python@0.5.0" }
    },
    "routes": [
      { "src": "/api/(.*)", "dest": "app/main.py" },
      { "src": "/(.*)",      "dest": "app/static/$1" }
    ]
  }
  ```
- [ ] Define environment variables in Vercel dashboard:
  - `AI_API_URL` (placeholder)  
  - `AI_API_KEY` (placeholder)  
- [ ] Push `main` branch → verify Vercel auto–deploy succeeds  
- [ ] Test live endpoint and static UI

## 7. Documentation & Wrap-Up
- [ ] Update README with:
  - Project description  
  - Setup & run instructions (local & Vercel)  
  - Environment variable details  
- [ ] Tag initial release (v0.1.0)  
- [ ] Merge `dev` → `main` after review  
- [ ] Celebrate MVP completion! 🎉 