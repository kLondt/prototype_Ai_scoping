from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transcript
from .serialzers import TranscriptSerializer
from agents.objective_agent import extract_objectives
from agents.persona_agent import identify_personas
from agents.marketing_agent import generate_marketing_plan
from agents.review_agent import review_document


class TranscriptUploadView(APIView):
    def post(self, request):
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
class GenerateHackathonDocumentView(APIView):
    def post(self, request):
        content = request.data.get("content", "")
        document = {
            "objectives": extract_objectives(content),
            "personas": identify_personas(content),
            "marketing_plan": generate_marketing_plan(content),
        }
        reviewed_document = review_document(document)
        return Response(reviewed_document)
