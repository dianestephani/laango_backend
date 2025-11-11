from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from twilio.rest import Client
from job_requests.models import InterpreterContact
from jobs.models import Job
from accounts.models import InterpreterProfile
import json


class HealthCheckView(APIView):
    """
    API endpoint to check if the server is running
    """
    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'Laango API is running'
        }, status=status.HTTP_200_OK)


class SendSMSView(APIView):
    """
    API endpoint to send SMS messages to interpreters via Twilio
    """
    def post(self, request):
        try:
            # Get data from request
            phone_numbers = request.data.get('phone_numbers', [])
            message_text = request.data.get('message', '')
            job_id = request.data.get('job_id')

            if not phone_numbers:
                return Response({
                    'success': False,
                    'error': 'No phone numbers provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not message_text:
                return Response({
                    'success': False,
                    'error': 'No message provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not job_id:
                return Response({
                    'success': False,
                    'error': 'No job ID provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get the job
            try:
                job = Job.objects.get(id=job_id)
            except Job.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Job not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if Twilio credentials are configured
            if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
                return Response({
                    'success': False,
                    'error': 'Twilio credentials not configured. Please add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER to your .env file.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Initialize Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            # Send SMS to each phone number
            results = []
            errors = []

            for phone_number in phone_numbers:
                try:
                    message = client.messages.create(
                        body=message_text,
                        from_=settings.TWILIO_PHONE_NUMBER,
                        to=phone_number
                    )
                    results.append({
                        'phone_number': phone_number,
                        'sid': message.sid,
                        'status': message.status
                    })

                    # Log the contact in the database
                    try:
                        interpreter = InterpreterProfile.objects.get(phone_number=phone_number)
                        InterpreterContact.objects.create(
                            job=job,
                            interpreter=interpreter,
                            message_sent=message_text,
                            phone_number=phone_number
                        )
                    except InterpreterProfile.DoesNotExist:
                        # If interpreter not found by phone number, still record that we sent the message
                        pass

                except Exception as e:
                    errors.append({
                        'phone_number': phone_number,
                        'error': str(e)
                    })

            return Response({
                'success': True,
                'sent': len(results),
                'failed': len(errors),
                'results': results,
                'errors': errors
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
