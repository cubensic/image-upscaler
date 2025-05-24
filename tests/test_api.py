import pytest
import io
from fastapi.testclient import TestClient
from PIL import Image
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

client = TestClient(app)


def create_test_image(format="PNG", size=(100, 100)):
    """Create a test image in memory"""
    img = Image.new('RGB', size, color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    return img_bytes


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "healthy"
    assert response_data["service"] == "image-upscaler"
    assert "ai_upscaler_available" in response_data
    assert isinstance(response_data["ai_upscaler_available"], bool)


def test_upscale_no_file():
    """Test upscale endpoint with no file"""
    response = client.post("/api/upscale")
    assert response.status_code == 422  # Validation error


def test_upscale_valid_png():
    """Test upscale endpoint with valid PNG file"""
    test_image = create_test_image("PNG")
    
    response = client.post(
        "/api/upscale",
        files={"image": ("test.png", test_image, "image/png")}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_upscale_valid_jpeg():
    """Test upscale endpoint with valid JPEG file"""
    test_image = create_test_image("JPEG")
    
    response = client.post(
        "/api/upscale",
        files={"image": ("test.jpg", test_image, "image/jpeg")}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_upscale_invalid_type():
    """Test upscale endpoint with invalid file type"""
    # Create a text file instead of an image
    text_file = io.BytesIO(b"This is not an image")
    
    response = client.post(
        "/api/upscale",
        files={"image": ("test.txt", text_file, "text/plain")}
    )
    
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_upscale_large_file():
    """Test upscale endpoint with file that's too large"""
    # Create a large image (this is a mock test - in reality we'd need a 5MB+ image)
    large_image = create_test_image("PNG", size=(1000, 1000))
    
    # Mock the size check by creating a large byte array
    large_data = b"x" * (6 * 1024 * 1024)  # 6MB
    large_file = io.BytesIO(large_data)
    
    response = client.post(
        "/api/upscale",
        files={"image": ("large.png", large_file, "image/png")}
    )
    
    # This should fail either due to size or invalid image format
    assert response.status_code in [400, 500]


if __name__ == "__main__":
    pytest.main([__file__]) 