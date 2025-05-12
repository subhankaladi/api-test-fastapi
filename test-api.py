import requests
import os

def test_background_removal():
    # Server details
    BASE_URL = "http://127.0.0.1:8000"
    ENDPOINT = "/remove-bg"
    
    # Test image - change this to your actual image path
    IMAGE_PATH = "subhankaladi.png"  # or "test-image.jpeg" based on your file
    
    # Verify image exists
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Test image not found at {IMAGE_PATH}")
        print("Current directory contents:", os.listdir())
        return
    
    try:
        # Open the image file
        with open(IMAGE_PATH, 'rb') as img_file:
            files = {'file': (os.path.basename(IMAGE_PATH), img_file, 'image/jpeg')}
            
            print(f"Sending POST request to {BASE_URL+ENDPOINT}")
            response = requests.post(BASE_URL + ENDPOINT, files=files)
            
            if response.status_code == 200:
                output_path = "result.png"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Success! Result saved to {output_path}")
            else:
                print(f"Error {response.status_code}: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_background_removal()