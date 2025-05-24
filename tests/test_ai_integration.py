import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
import sys

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.ai_upscaler import AIUpscaler

@pytest.mark.asyncio
async def test_ai_upscaler_initialization():
    """Test AIUpscaler initialization"""
    with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "test-token"}):
        upscaler = AIUpscaler()
        assert upscaler.api_token == "test-token"
        assert upscaler.model == "nightmareai/real-esrgan"

@pytest.mark.asyncio 
async def test_ai_upscaler_missing_token():
    """Test AIUpscaler fails without token"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="REPLICATE_API_TOKEN"):
            AIUpscaler()

@pytest.mark.asyncio
async def test_bytes_to_data_url():
    """Test image bytes to data URL conversion"""
    with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "test-token"}):
        upscaler = AIUpscaler()
        
        # Create a simple test image
        from PIL import Image
        import io
        img = Image.new('RGB', (10, 10), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        data_url = upscaler._bytes_to_data_url(img_bytes)
        assert data_url.startswith("data:image/png;base64,")

@pytest.mark.asyncio
async def test_upscale_image_mock():
    """Test upscale_image with mocked Replicate API"""
    with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "test-token"}):
        upscaler = AIUpscaler()
        
        # Mock the Replicate client and response
        mock_output = ["https://example.com/upscaled.png"]
        mock_response_content = b"fake upscaled image data"
        
        with patch.object(upscaler, '_run_model_async', return_value=mock_output) as mock_run:
            with patch.object(upscaler, '_download_result', return_value=mock_response_content) as mock_download:
                # Create test image bytes
                from PIL import Image
                import io
                img = Image.new('RGB', (10, 10), color='red')
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                test_bytes = img_bytes.getvalue()
                
                # Call upscale_image
                result = await upscaler.upscale_image(test_bytes)
                
                # Verify the result
                assert result == mock_response_content
                mock_run.assert_called_once()
                mock_download.assert_called_once_with(mock_output) 