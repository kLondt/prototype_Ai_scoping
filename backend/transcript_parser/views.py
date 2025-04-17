from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transcript
from agents.objective_agent import extract_objectives
from agents.persona_agent import identify_personas
from agents.marketing_agent import generate_marketing_plan
from agents.review_agent import review_document


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TranscriptSerializer


class TranscriptUploadView(APIView):
    def post(self, request):
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class GenerateHackathonDocumentView(APIView):
    def post(self, request):
        content = request.data.get("content", " ")
        if not content:
            return Response({"error": "No content provided"}, status=status.HTTP_400_BAD_REQUEST)
        document = {
            "objectives": extract_objectives(content),
            "personas": identify_personas(content),
            "marketing_plan": generate_marketing_plan(content),
        }
        reviewed_document = review_document(document)
        return Response(reviewed_document, status=status.HTTP_200_OK)
    #view that accepst the edited generated doc
class EditDocumentView(APIView):
    def post(self, request):
        document = request.data.get("document", {})  # Get the refined document from the request
        if not document:
            return Response({"error": "No document provided"}, status=status.HTTP_400_BAD_REQUEST)

        # For now, simply return the edited document 
        return Response(document, status=status.HTTP_200_OK)