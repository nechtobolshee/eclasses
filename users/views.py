from django.shortcuts import render

from .serializers import CurrentUserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class GetCurrentUser(APIView):
	authentication_classes = (TokenAuthentication, SessionAuthentication)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		serializer = CurrentUserSerializer(request.user)
		return Response(serializer.data)
