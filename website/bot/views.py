import re
import httpx
from django.http import JsonResponse
from django.views import View
from django.http import HttpRequest
from bot.lex import Chat
from utils.http import get_client_ip
from django.shortcuts import render

class ChatBotView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        """Handles GET requests to render the chatbot page."""
        return render(request, "chatbot.html")

    async def post(self, request: HttpRequest, *args, **kwargs):
        """Handles POST requests to send a message or image to the chatbot."""

        message = request.POST.get("message", "").strip()
        image = request.FILES.get("image", None)
        session_id = get_client_ip(request=request)

        image_key = None

        if image:
            # Obter URL pre-assinada da nossa API Serverless
            url = await Chat.get_presigned_url(session_id, image.content_type)
            if url:
                # Fazer o upload do arquivo diretamente para o S3 via HTTP PUT sem usar boto3!
                async with httpx.AsyncClient(timeout=30.0) as client:
                    await client.put(
                        url,
                        content=image.read(),
                        headers={"Content-Type": image.content_type}
                    )
                image_key = f"{session_id}-image.jpg"

        chat_input = message or image_key
        response_data = await Chat.post_message(
            message=chat_input,
            session_id=session_id,
        )

        response = JsonResponse(response_data)
        response.set_cookie("session_id", session_id)

        return response
