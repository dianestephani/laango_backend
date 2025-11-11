from django.urls import path
from .views import HealthCheckView, SendSMSView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('send-sms/', SendSMSView.as_view(), name='send-sms'),
]
