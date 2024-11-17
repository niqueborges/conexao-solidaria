from uuid import uuid4
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from app.aws.s3 import s3
from bot.lex import Chat
from app.settings import S3_BUCKET_NAME
from django.http import HttpRequest


class ChatBotView(View):
    """
    View to handle chatbot interactions. Supports GET and POST requests
    for rendering the chatbot page and sending messages or media to the chatbot.
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        """Handles GET requests to render the chatbot page."""

        return render(request, "chatbot.html")

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handles POST requests to send a message or media file to the chatbot."""

        message = request.POST.get("message", "").strip()
        audio = request.FILES.get("audio", None)
        image = request.FILES.get("image", None)

        # Checks if a session_id already exists,
        # otherwise creates a new one and stores it in the cookie
        session_id = request.COOKIES.get("session_id") or str(uuid4())

        # Store audio and image files in S3 (if they exist)
        audio_url = (
            s3.put_object(
                bucket=S3_BUCKET_NAME,
                body=audio.read(),
                key=f"{session_id}-audio.mp3",
                contentType=audio.content_type,
            )
            if audio
            else None
        )

        image_url = (
            s3.put_object(
                bucket=S3_BUCKET_NAME,
                body=image.read(),
                key=f"{session_id}-image",
                contentType=image.content_type,
            )
            if image
            else None
        )

        # Sends the message or URLs to the bot
        response = Chat.post_message(
            message=message or audio_url or image_url,
            session_id=session_id,
        )

        # Returns the response with the session_id cookie
        response = JsonResponse(response)
        # Sets the session_id cookie
        response.set_cookie("session_id", session_id)

        return response
