"""
VAPI Request Serializer Middleware

Handles incoming VAPI tool call format and normalizes it for route handlers.
"""
import json
from typing import Any, Dict, Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.logger import get_logger

logger = get_logger("vapi-serializer")


class VAPISerializer(BaseHTTPMiddleware):
    """
    Middleware to parse VAPI tool call format and normalize request body
    """
    
    async def dispatch(self, request: Request, call_next):
        # Only process POST requests
        if request.method == "POST":
            # Read the original body
            body = await request.body()
            
            try:
                if body:
                    data = json.loads(body)
                    logger.info(f"Received VAPI request: {json.dumps(data)}")
                    
                    # Extract arguments from VAPI format
                    if "message" in data and "toolCalls" in data["message"]:
                        tool_calls = data["message"]["toolCalls"]
                        if tool_calls and len(tool_calls) > 0:
                            first_tool_call = tool_calls[0]
                            
                            # Extract toolCallId
                            tool_call_id = first_tool_call.get("id")
                            
                            # Extract arguments (already parsed as dict)
                            function_data = first_tool_call.get("function", {})
                            normalized_data = function_data.get("arguments", {})
                            
                            # Store in request state
                            request.state.normalized_body = normalized_data
                            request.state.vapi_tool_call_id = tool_call_id
                            logger.info(f"Parsed VAPI - body: {normalized_data}, toolCallId: {tool_call_id}")
                        else:
                            logger.warning("VAPI request has no toolCalls")
                            request.state.normalized_body = {}
                            request.state.vapi_tool_call_id = None
                    else:
                        # Not VAPI format
                        logger.warning(f"Not VAPI format. Keys: {list(data.keys())}")
                        request.state.normalized_body = {}
                        request.state.vapi_tool_call_id = None
                        
            except json.JSONDecodeError as e:
                # If JSON is invalid, let the route handler deal with it
                logger.error(f"JSON decode error: {e}")
                pass
            except Exception as e:
                logger.error(f"VAPI serializer error: {e}", exc_info=True)
        
        response = await call_next(request)
        return response


async def get_normalized_body(request: Request) -> Dict[str, Any]:
    """
    Helper function to get normalized body from request
    Use this in route handlers instead of await request.json()
    """
    if hasattr(request.state, "normalized_body"):
        return request.state.normalized_body
    
    # Fallback if middleware didn't run
    return {}


def format_vapi_response(request: Request, result: Any) -> Dict[str, Any]:
    #Normalize response into VAPI format

    tool_call_id = getattr(request.state, "vapi_tool_call_id", None)
    
    return {
        "results": [
            {
                "toolCallId": tool_call_id,
                "result": result
            }
        ]
    }

