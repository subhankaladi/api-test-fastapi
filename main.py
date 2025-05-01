# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import StreamingResponse
# from service.remover import BackgroundRemover
# from service.utils import FileHandler
# import io
# import logging

# app = FastAPI(title="AI Background Remover")

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Encapsulation: Object of logic class
# remover = BackgroundRemover()

# @app.get("/")
# def root():
#     return {"message": "Welcome to the AI Background Remover API"}

# @app.post("/remove-bg")
# async def remove_bg(file: UploadFile = File(...)):
#     try:
#         logger.info(f"Received file: {file.filename}, content-type: {file.content_type}")
        
#         # Read & Validate
#         image_data = await FileHandler.read_image(file)

#         # Remove background
#         result = remover.remove_background(image_data)

#         # Return image
#         return StreamingResponse(
#             io.BytesIO(result), 
#             media_type="image/png",
#             headers={"Content-Disposition": f"attachment; filename=removed_bg_{file.filename}"}
#         )
        
#     except HTTPException as he:
#         raise he
#     except Exception as e:
#         logger.error(f"Error processing image: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")from fastapi import FastAPI, UploadFile, File, HTTPException




from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  # CORS ke liye import
from service.remover import BackgroundRemover
# from service.utils import FileHandler
import io
import logging
from PIL import Image

app = FastAPI(title="AI Background Remover")

# CORS Middleware ko configure karna
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend ka origin (port adjust karein agar alag hai)
    allow_credentials=True,
    allow_methods=["*"],  # Sabhi HTTP methods allow karna (POST, GET, etc.)
    allow_headers=["*"],  # Sabhi headers allow karna
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported image formats
SUPPORTED_TYPES = ["image/jpeg", "image/png", "image/webp"]

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        # Validate content type
        if file.content_type not in SUPPORTED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported types: {SUPPORTED_TYPES}"
            )

        # Read image data
        image_data = await file.read()
        
        # Convert WebP to PNG if needed
        if file.content_type == "image/webp":
            image = Image.open(io.BytesIO(image_data))
            png_buffer = io.BytesIO()
            image.save(png_buffer, format="PNG")
            image_data = png_buffer.getvalue()

        # Process image
        result = BackgroundRemover().remove_background(image_data)
        
        return StreamingResponse(
            io.BytesIO(result),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=result.png"}
        )
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))