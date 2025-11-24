"""
VAPI Request Serializer Middleware

Handles incoming VAPI tool call format and normalizes it for route handlers.
"""
import json
from typing import Any, Dict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import get_logger

logger = get_logger("vapi-serializer")


class VAPISerializer(BaseHTTPMiddleware):
    """Middleware to parse VAPI tool call format and normalize request body"""
    
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            body = await request.body()
            
            try:
                data = json.loads(body)
                logger.info(f"Received VAPI request: {json.dumps(data)}")
                
                # Extract from VAPI format: message.toolCalls[0].function.arguments
                tool_calls = data.get("message", {}).get("toolCalls", [])
                
                if tool_calls:
                    first_call = tool_calls[0]
                    tool_call_id = first_call.get("id")
                    normalized_data = first_call.get("function", {}).get("arguments", {})
                    
                    request.state.normalized_body = normalized_data
                    request.state.vapi_tool_call_id = tool_call_id
                    logger.info(f"Parsed - body: {normalized_data}, toolCallId: {tool_call_id}")
                else:
                    logger.warning(f"No toolCalls found. Keys: {list(data.keys())}")
                    request.state.normalized_body = {}
                    request.state.vapi_tool_call_id = None
                        
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
            except Exception as e:
                logger.error(f"Serializer error: {e}", exc_info=True)
        
        return await call_next(request)


async def get_normalized_body(request: Request) -> Dict[str, Any]:
    """Get normalized body from request state"""
    return getattr(request.state, "normalized_body", {})


def format_vapi_response(request: Request, result: Any) -> Dict[str, Any]:
    """Format response in VAPI's expected format"""
    tool_call_id = getattr(request.state, "vapi_tool_call_id", None)
    
    return {
        "results": [{
            "toolCallId": tool_call_id,
            "result": result
        }]
    }

