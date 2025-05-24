import os
import logging
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image

# Load environment variables
from dotenv import load_dotenv

# Load environment variables from the appropriate file
env_file = ".env.development" if os.path.exists(".env.development") else ".env"
load_dotenv(env_file)

# Import our AI service
from app.services.ai_upscaler import AIUpscaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Image Upscaler API", version="1.0.0")

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

# Initialize AI upscaler
try:
    ai_upscaler = AIUpscaler()
    logger.info("AI upscaler initialized successfully")
except Exception as e:
    logger.warning(f"AI upscaler initialization failed: {e}")
    ai_upscaler = None

@app.post("/api/upscale")
async def upscale_image(image: UploadFile = File(...)):
    """
    Upscale an uploaded image using AI.
    
    Accepts: JPG, PNG, WEBP files up to 5MB
    Returns: Upscaled image as PNG
    """
    logger.info(f"Received upload request: {image.filename}, content_type: {image.content_type}")
    
    # Validate file existence
    if not image:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate content type
    if image.content_type not in ALLOWED_TYPES:
        logger.warning(f"Invalid content type: {image.content_type}")
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_TYPES)}"
        )
    
    # Read file content
    content = await image.read()
    
    # Validate file size
    if len(content) > MAX_FILE_SIZE_BYTES:
        logger.warning(f"File too large: {len(content)} bytes")
        raise HTTPException(
            status_code=400, 
            detail=f"File exceeds {MAX_FILE_SIZE_MB}MB limit"
        )
    
    logger.info(f"Processing image: {len(content)} bytes")
    
    try:
        if ai_upscaler:
            # Use AI upscaling
            logger.info("Using AI upscaling service")
            upscaled_bytes = await ai_upscaler.upscale_image(
                content, 
                scale=4,  # 4x upscaling
                face_enhance=True  # Enable face enhancement
            )
            
            logger.info("AI upscaling completed successfully")
            
            return StreamingResponse(
                io.BytesIO(upscaled_bytes),
                media_type="image/png",
                headers={"Content-Disposition": f"attachment; filename=upscaled_{image.filename}.png"}
            )
        else:
            # Fallback to stub (convert to PNG)
            logger.warning("AI upscaler not available, using fallback")
            img = Image.open(io.BytesIO(content))
            output_buffer = io.BytesIO()
            img.save(output_buffer, format="PNG")
            output_buffer.seek(0)
            
            return StreamingResponse(
                io.BytesIO(output_buffer.getvalue()),
                media_type="image/png",
                headers={"Content-Disposition": f"attachment; filename=fallback_{image.filename}.png"}
            )
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "image-upscaler",
        "ai_upscaler_available": ai_upscaler is not None
    }

# Mount static files (after API routes)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 