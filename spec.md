# Image Upscaling Web App Specification

## 1. Overview  
A minimal web application that lets a user drag-and-drop a single image (JPG, PNG, WEBP, ≤ 5 MB), sends it to an AI upscaling API via a FastAPI backend, and returns a higher-resolution image for download. The app is optimized for rapid MVP delivery, learning, and deployment on Vercel.

## 2. Goals  
- Deliver a working MVP in days  
- Learn FastAPI, file handling, serverless deployment  
- Keep code simple, modular, and easy to iterate on  

## 3. Functional Requirements  
1. **Image Upload**  
   - User drags-and-drops or clicks to select one image.  
   - Acceptable formats: JPG, PNG, WEBP.  
   - Maximum file size: 5 MB.  
2. **Validation**  
   - Client-side: check file type & size.  
   - Server-side: re-validate type & size, reject invalid inputs with 400 errors.  
3. **Upscale Request**  
   - Frontend POSTs image (multipart/form-data) to `POST /api/upscale`.  
   - Backend forwards the binary payload to an AI upscaling API (configured but not yet called).  
4. **Result Handling**  
   - Backend returns the upscaled image as a binary response (`Content-Type: image/png`).  
   - Frontend displays the result in an <img> element.  
   - Provide a "Download" button to save the upscaled file.  
5. **Single-Image Flow**  
   - Only one image in flight at a time.  
   - New upload clears previous result and status.  

## 4. Non-Functional Requirements  
- **Performance**: UI remains responsive for uploads ≤ 5 MB.  
- **Scalability**: Stateless serverless functions suitable for Vercel.  
- **Maintainability**: Clear separation between frontend, backend, and AI integration code.  
- **Security**:  
  - Strict file validation.  
  - No persistence of uploaded or processed images.  

## 5. Technical Stack  
- **Backend**: Python 3.x + FastAPI + Uvicorn  
- **Frontend**:  
  - HTML5, plain CSS, vanilla JavaScript (Fetch API)  
  - Single static `index.html` served by FastAPI or as a Vercel static asset  
- **AI Upscaling**: Third-party REST API (stubbed for MVP; configurable via environment variables)  
- **Hosting & Deployment**: Vercel (serverless Python functions via `vercel-python`)  
- **Environments**:  
  - `.env.development`  
  - `.env.production`  

## 6. Architecture & Data Flow  
```
[User Drag/Drop] → [Frontend Validation]
        ↓
[POST /api/upscale] ──→ [FastAPI Endpoint]
        ↓                    -  Validate file
                            -  (Stub) Forward to AI API
                            -  Return binary image
        ↓
[Frontend Receives Blob] → [Display & Download]
```

## 7. API Endpoints  

### POST /api/upscale  
- **Request**  
  - Content-Type: `multipart/form-data`  
  - Field: `image` (binary file)  
- **Responses**  
  - `200 OK`: binary image (`Content-Type: image/png`)  
  - `400 Bad Request`: invalid file type/size  
  - `502 Bad Gateway`: AI API error (future)  

## 8. Frontend Components  

1. **DragDropZone**  
   - Handles drag events & click-to-open file picker  
   - Validates file type and size before upload  

2. **ProgressIndicator**  
   - Visual feedback during upload & processing  
   - States: idle, uploading, processing, done  

3. **ResultViewer**  
   - Displays the upscaled image in an <img>  
   - "Download" button uses `URL.createObjectURL(blob)`  

4. **NotificationBanner**  
   - Shows inline errors (e.g., "File too large")  
   - Shows API/network errors  

## 9. Error Handling & UX  
- **Client-side**  
  - Inline warnings for unsupported files or size > 5 MB  
- **Server-side**  
  - Return clear JSON error payloads:  
    ```
    { "error": "File exceeds 5 MB limit." }
    ```  
- **Global Banner** for network or processing failures  

## 10. Logging & Monitoring  
- Use `console.log()` in frontend & backend for key events:  
  - Upload start/end  
  - API request/response status  
  - Validation failures  
- No external logging/monitoring services in MVP  

## 11. Styling  
- Plain CSS (no frameworks)  
- Responsive layout: centered drop zone, result preview below  
- Simple visual feedback (hover states, error color)  

## 12. Development Workflow  

1. **Repository Structure**  
   ```
   /app
     ├─ main.py            # FastAPI entrypoint
     ├─ api/
     └─ static/
         ├─ index.html
         ├─ styles.css
         └─ script.js
   /tests
   .env.development
   .env.production
   vercel.json
   ```

2. **Local Setup**  
   - Create Python venv, `pip install fastapi uvicorn python-multipart`  
   - Place static assets in `app/static`  
   - Run: `uvicorn app.main:app --reload`

3. **Testing**  
   - Pytest for backend: validate `POST /api/upscale` error cases & success stub.  
   - Manual UI testing in browser.

4. **Version Control**  
   - Main branches: `dev` → feature branches → PR → `main`  
   - Commit early, push often.

## 13. Deployment on Vercel  

- **vercel.json**: configure Python serverless function under `/api/*`  
- **Environment Variables**  
  - `AI_API_URL` (placeholder)  
  - `AI_API_KEY` (placeholder)  
- Push `main` → Vercel auto-deploys both static frontend & serverless backend  

## 14. Next Steps & Learning Opportunities  
- Hook up real AI API & remove stub  
- Add selectable upscale factors (2×, 4×)  
- Introduce simple unit tests for frontend logic (e.g., file validation)  
- Explore caching or CDN for hot images  

---

**Ready to proceed with implementation?** 