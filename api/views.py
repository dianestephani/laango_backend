from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HealthCheckView(APIView):
    """
    API endpoint to check if the server is running
    """
    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'Laango API is running'
        }, status=status.HTTP_200_OK)
