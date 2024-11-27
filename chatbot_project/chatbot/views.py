from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_openai import ChatOpenAI  # 최신 경로 사용
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

class ChatAPIView(APIView):
    def get(self, request):
        # 브라우저에서 GET 요청으로 확인할 때 기본 안내 메시지를 반환
        return Response({"message": "Welcome to the Chat API. Use POST to interact with the chatbot."}, status=status.HTTP_200_OK)

    def post(self, request):
        # POST 요청 처리
        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # OpenAI API 키 가져오기
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return Response({"error": "OpenAI API key not found. Check your environment variables."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            # GPT 호출
            llm = ChatOpenAI(
                model="gpt-4",
                openai_api_key=api_key,
            )
            # OpenAI GPT 호출
            messages = [
                {"role": "system", "content": "You are a culinary expert. Answer all questions related to food, recipes, and cooking techniques."},
                {"role": "user", "content": user_message}
            ]
            bot_response = llm.predict(user_message)
            

            return Response({
                "user_message": user_message,
                "response": bot_response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)