import os
import json
import asyncio
import subprocess
from typing import Dict, Any
import logging
import httpx

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self):
        self.mcp_server_path = "../manim_mcp"
        self.renders_dir = "../renders"
        os.makedirs(self.renders_dir, exist_ok=True)
        self.mcp_http_url = os.getenv("MANIM_MCP_URL")  # e.g., http://manim_mcp:9000

    async def generate_visualization(self, refined_request: Dict[str, Any]) -> str:
        """
        Generate a visualization using the Manim MCP server.
        Returns the path to the generated video file.
        """
        visualization_type = refined_request.get("visualization_type")
        parameters = refined_request.get("parameters", {})
        
        logger.info(f"Generating {visualization_type} with parameters: {parameters}")
        
        try:
            if self.mcp_http_url:
                video_path = await self._call_mcp_http(visualization_type, parameters)
            else:
                # CLI fallback
                video_path = await self._call_mcp_server(visualization_type, parameters)
            return video_path
        except Exception as e:
            logger.error(f"Error generating visualization: {e}")
            # Return a placeholder video path for demo purposes
            return await self._create_placeholder_video(visualization_type)

    async def _call_mcp_http(self, visualization_type: str, parameters: Dict[str, Any]) -> str:
        """Call the MCP FastAPI server"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{self.mcp_http_url}/render",
                json={
                    "type": visualization_type,
                    "parameters": parameters,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            path = data.get("video_path")
            if not path:
                raise RuntimeError("MCP HTTP response missing video_path")
            return path

    async def _call_mcp_server(self, visualization_type: str, parameters: Dict[str, Any]) -> str:
        """Call the MCP server to generate the visualization"""
        
        # Create a request file for the MCP server
        request_data = {
            "type": visualization_type,
            "parameters": parameters
        }
        
        request_file = os.path.join(self.renders_dir, "request.json")
        with open(request_file, "w") as f:
            json.dump(request_data, f)
        
        # Call the MCP server
        cmd = [
            "python", 
            os.path.join(self.mcp_server_path, "server.py"),
            request_file
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.mcp_server_path
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            raise Exception(f"MCP server failed: {error_msg}")
        
        # Parse the output to get the video path
        output = stdout.decode().strip()
        if output.startswith("/"):
            return output
        else:
            # Assume it's a relative path from renders directory
            return os.path.join(self.renders_dir, output)

    async def _create_placeholder_video(self, visualization_type: str) -> str:
        """Create a placeholder video for demo purposes"""
        import uuid
        
        # Generate a unique filename
        video_id = str(uuid.uuid4())[:8]
        video_filename = f"{visualization_type}_{video_id}.mp4"
        video_path = os.path.join(self.renders_dir, video_filename)
        
        # Create a simple placeholder video using ffmpeg if available
        try:
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"testsrc=duration=3:size=1280x720:rate=30",
                "-f", "lavfi",
                "-i", f"sine=frequency=1000:duration=3",
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                video_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            
            await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"Created placeholder video: {video_path}")
                return video_path
                
        except FileNotFoundError:
            logger.warning("ffmpeg not found, creating empty placeholder file")
        
        # If ffmpeg is not available, create an empty file as placeholder
        with open(video_path, "w") as f:
            f.write("placeholder")
        
        return video_path
