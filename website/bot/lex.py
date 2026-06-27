import httpx
from typing import Any
from app.settings import CHATBOT_API_URL, CHATBOT_API_KEY

class DialogFlow:
    """Class for interacting with the Serverless Chatbot API."""

    async def post_message(self, message: str, session_id: str) -> dict[str, Any]:
        """Sends a message to the Chatbot Proxy API and receives the Lex response."""
        try:
            url = f"{CHATBOT_API_URL.rstrip('/')}/web-proxy"
            payload = {
                "message": message,
                "session_id": session_id
            }
            
            headers = {}
            if CHATBOT_API_KEY:
                headers["x-api-key"] = CHATBOT_API_KEY
                
            async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as exc:
            return {"error": f"Request failed: {exc}", "user": message}
        except httpx.HTTPStatusError as exc:
            return {"error": f"API returned error status: {exc.response.status_code}", "user": message}

    async def get_presigned_url(self, session_id: str, content_type: str) -> str | None:
        """Requests a presigned URL for direct S3 upload from the API."""
        try:
            url = f"{CHATBOT_API_URL.rstrip('/')}/upload-url"
            payload = {
                "session_id": session_id,
                "content_type": content_type
            }
            
            headers = {}
            if CHATBOT_API_KEY:
                headers["x-api-key"] = CHATBOT_API_KEY
                
            async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("url")
        except Exception:
            return None

Chat = DialogFlow()

