import os
import replicate
from dotenv import load_dotenv
import base64
import io
from PIL import Image

# Load environment variables from .env.development
dotenv_path = os.path.join(os.path.dirname(__file__), '.env.development')
load_dotenv(dotenv_path=dotenv_path)

API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
# Let's use the specific model ID from your .env for this direct test first
MODEL_ID = os.getenv("AI_UPSCALE_MODEL", "nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa")

print(f"Using Replicate API Token: {API_TOKEN[:12]}...") # Print part of token for verification
print(f"Using Model ID: {MODEL_ID}")

def create_dummy_image_data_url():
    # Create a tiny dummy PNG image
    img = Image.new('RGB', (10, 10), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    b64_string = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/png;base64,{b64_string}"

if not API_TOKEN:
    print("ERROR: REPLICATE_API_TOKEN not found in .env.development")
else:
    try:
        client = replicate.Client(api_token=API_TOKEN)
        image_data_url = create_dummy_image_data_url()
        
        print("Sending request to Replicate...")
        output = client.run(
            MODEL_ID,
            input={
                "image": image_data_url,
                "scale": 2, # Using a smaller scale for faster test
                "face_enhance": False
            }
        )
        print("Replicate API call successful!")
        print("Output:", output)
    except replicate.exceptions.ReplicateError as e:
        print(f"Replicate API Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            try:
                print(f"Response JSON: {e.response.json()}")
            except Exception:
                print(f"Response Text: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 