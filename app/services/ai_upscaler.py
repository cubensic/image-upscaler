import os
import logging
import base64
import io
from typing import Optional, Union, List
import replicate
from PIL import Image
from replicate.helpers import FileOutput

logger = logging.getLogger(__name__)

class AIUpscaler:
    def __init__(self):
        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        self.model = os.getenv("AI_UPSCALE_MODEL", "nightmareai/real-esrgan")
        logger.info(f"AIUpscaler initialized with model ID: {self.model}")
        
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN environment variable is required")
        
        # Initialize replicate client
        self.client = replicate.Client(api_token=self.api_token)
        
    async def upscale_image(self, image_bytes: bytes, scale: int = 4, face_enhance: bool = True) -> bytes:
        """
        Upscale an image using Replicate's Real-ESRGAN model
        
        Args:
            image_bytes: Raw image bytes
            scale: Upscaling factor (2, 4, or 8)
            face_enhance: Whether to enhance faces using GFPGAN
            
        Returns:
            Upscaled image bytes
        """
        try:
            logger.info(f"Starting AI upscaling with {self.model}, scale={scale}, face_enhance={face_enhance}")
            
            # Convert image bytes to base64 data URL
            image_data_url = self._bytes_to_data_url(image_bytes)
            
            # Prepare input for Replicate
            input_data = {
                "image": image_data_url,
                "scale": scale,
                "face_enhance": face_enhance
            }
            
            # Run the model
            logger.info("Sending request to Replicate API...")
            output = await self._run_model_async(input_data)
            
            # Download the result
            logger.info("Downloading upscaled image...")
            result_bytes = await self._download_result(output)
            
            logger.info(f"AI upscaling completed successfully. Output size: {len(result_bytes)} bytes")
            return result_bytes
            
        except Exception as e:
            logger.error(f"Error during AI upscaling: {str(e)}")
            raise
    
    def _bytes_to_data_url(self, image_bytes: bytes) -> str:
        """Convert image bytes to data URL format"""
        # Detect image format
        img = Image.open(io.BytesIO(image_bytes))
        img_format = img.format.lower()
        
        # Convert to base64
        b64_string = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:image/{img_format};base64,{b64_string}"
    
    async def _run_model_async(self, input_data: dict):
        """Run the Replicate model asynchronously"""
        import asyncio
        
        # Run replicate in thread pool since it's synchronous
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            lambda: self.client.run(self.model, input=input_data)
        )
    
    async def _download_result(self, output: Union[str, List[Union[str, FileOutput]], FileOutput]) -> bytes:
        """Download the result from Replicate output."""
        import asyncio
        import httpx
        
        url_to_download = None
        
        if isinstance(output, FileOutput):
            url_to_download = output.url
        elif isinstance(output, list) and len(output) > 0:
            first_item = output[0]
            if isinstance(first_item, FileOutput):
                url_to_download = first_item.url
            elif isinstance(first_item, str):
                url_to_download = first_item
        elif isinstance(output, str):
            url_to_download = output
            
        if not url_to_download:
            raise ValueError(f"Could not extract URL from Replicate output. Output type: {type(output)}, Output: {output}")
        
        logger.info(f"Downloading from URL: {url_to_download}")
        
        # Download the image
        async with httpx.AsyncClient() as client:
            response = await client.get(url_to_download)
            response.raise_for_status() # Raise an exception for bad status codes
            return response.content 