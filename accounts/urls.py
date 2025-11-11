from django.urls import path
from .views import (
    InterpreterJobsListView,
    InterpreterDetailView,
    interpreter_jobs_page,
    available_jobs_page,
    AcceptJobView,
    accept_job
)

app_name = 'accounts'

urlpatterns = [
    path('interpreters/<int:interpreter_id>/jobs/', InterpreterJobsListView.as_view(), name='interpreter-jobs-api'),
    path('interpreters/<int:id>/', InterpreterDetailView.as_view(), name='interpreter-detail'),
    path('interpreters/<int:interpreter_id>/jobs/page/', interpreter_jobs_page, name='interpreter-jobs-page'),
    path('interpreters/<int:interpreter_id>/jobs/available/', available_jobs_page, name='available-jobs-page'),
    path('interpreters/<int:interpreter_id>/jobs/<int:job_id>/accept/', AcceptJobView.as_view(), name='accept-job-api'),
    path('interpreters/<int:interpreter_id>/jobs/<int:job_id>/accept/page/', accept_job, name='accept-job'),
]
