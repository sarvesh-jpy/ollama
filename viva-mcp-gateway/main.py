import os
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.routing import Route, Mount
# pyrefly: ignore [missing-import]
from mcp.server import Server
# pyrefly: ignore [missing-import]
from mcp.server.sse import SseServerTransport
import mcp.types as types  # Added the official types module

# 1. Initialize the Gateway
app = FastAPI(
    title="Antigravity-Ollama MCP Gateway",
    description="A secure gateway routing IDE agent requests to a local Ollama instance."
)

# 2. Security Middleware
API_KEY = os.environ.get("MCP_API_KEY", "viva-project-key")

def verify_request(request: Request):
    api_key_header = request.headers.get("X-API-Key")
    api_key_query = request.query_params.get("api_key")
    if api_key_header != API_KEY and api_key_query != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized Agent Access")

# 3. Initialize the MCP Server
mcp = Server("ollama-gateway")

# 4. Ollama Config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:8b" 

# 5. Define the MCP Tool for Antigravity (The Correct Protocol Method)
@mcp.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Tells the Antigravity IDE what tools are available on this server."""
    return [
        types.Tool(
            name="local-ollama-node",
            description="Query the local Ollama model for private code generation or analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The coding prompt or question for the local AI."
                    }
                },
                "required": ["prompt"]
            }
        )
    ]

@mcp.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Executes the tool when the IDE agent requests it."""
    if name != "local-ollama-node":
        raise ValueError(f"Unknown tool requested: {name}")
        
    prompt = arguments.get("prompt")
    if not prompt:
        raise ValueError("A prompt is required to query Ollama.")

    print(f"\nIntercepted Request from Antigravity. Routing to {MODEL_NAME}...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": 4096
                    }
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            result_text = f"LOCAL OLLAMA RESPONSE:\n{data.get('response', '')}"
            return [types.TextContent(type="text", text=result_text)]
            
        except Exception as e:
            error_text = f"Error connecting to Ollama Engine: {str(e)}"
            return [types.TextContent(type="text", text=error_text)]

# 6. Configure the SSE Transport 
sse = SseServerTransport("/mcp/messages")

async def handle_sse(request: Request):
    verify_request(request)
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp.run(streams[0], streams[1], mcp.create_initialization_options())

async def secure_message_handler(scope, receive, send):
    request = Request(scope, receive)
    verify_request(request)
    await sse.handle_post_message(scope, receive, send)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# 7. Mount routes
app.router.routes.append(Route("/mcp/sse", endpoint=handle_sse, methods=["GET"]))
app.router.routes.append(Mount("/mcp/messages", app=secure_message_handler))

# 8. Start the Server
if __name__ == "__main__":
    print("Starting production gateway on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8003)