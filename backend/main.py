from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import logging
from llm import LLMService
from mcp_client import MCPClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Manim Visualizer API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving rendered videos
os.makedirs("../renders", exist_ok=True)
app.mount("/renders", StaticFiles(directory="../renders"), name="renders")

# Initialize services
llm_service = LLMService()
mcp_client = MCPClient()

class PromptRequest(BaseModel):
    prompt: str

class VisualizationResponse(BaseModel):
    video_url: str
    refined_prompt: str
    visualization_type: str
    explanation: str

@app.get("/")
async def root():
    return {"message": "Manim Visualizer API is running"}

@app.post("/api/generate", response_model=VisualizationResponse)
async def generate_visualization(request: PromptRequest):
    try:
        logger.info(f"Received prompt: {request.prompt}")
        
        # Step 1: Refine the prompt using LLM
        refined_request = await llm_service.refine_prompt(request.prompt)
        logger.info(f"Refined request: {refined_request}")
        
        # Step 2: Generate visualization using MCP
        video_path = await mcp_client.generate_visualization(refined_request)
        logger.info(f"Generated video at: {video_path}")
        
        # Step 2.5: Generate an educational explanation
        explanation = await llm_service.generate_explanation(refined_request, request.prompt)
        
        # Step 3: Return the response
        video_url = f"/renders/{os.path.basename(video_path)}"
        
        return VisualizationResponse(
            video_url=video_url,
            refined_prompt=refined_request.get("description", request.prompt),
            visualization_type=refined_request.get("visualization_type", "unknown"),
            explanation=explanation,
        )
        
    except Exception as e:
        logger.error(f"Error generating visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
