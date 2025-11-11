from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import InterpreterProfile
from .serializers import InterpreterProfileSerializer
from jobs.models import Job
from jobs.serializers import JobSerializer


class InterpreterJobsListView(APIView):
    """
    API endpoint to get all jobs for a specific interpreter
    """
    def get(self, request, interpreter_id):
        interpreter = get_object_or_404(InterpreterProfile, id=interpreter_id)
        jobs = interpreter.jobs.all().order_by('-date', '-time')
        serializer = JobSerializer(jobs, many=True)

        # Calculate projected earnings
        projected_earnings = sum(job.payment for job in jobs)

        return Response({
            'interpreter': {
                'id': interpreter.id,
                'name': f"{interpreter.first_name} {interpreter.last_name}",
                'email': interpreter.email_address,
            },
            'jobs': serializer.data,
            'total_jobs': jobs.count(),
            'projected_earnings': projected_earnings
        })


class InterpreterDetailView(generics.RetrieveAPIView):
    """
    API endpoint to get interpreter details including all their jobs
    """
    queryset = InterpreterProfile.objects.all()
    serializer_class = InterpreterProfileSerializer
    lookup_field = 'id'


def interpreter_jobs_page(request, interpreter_id):
    """
    Template view for interpreters to see their jobs
    """
    interpreter = get_object_or_404(InterpreterProfile, id=interpreter_id)
    jobs = interpreter.jobs.all().order_by('-date', '-time')

    # Calculate projected earnings
    projected_earnings = sum(job.payment for job in jobs)

    context = {
        'interpreter': interpreter,
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'projected_earnings': projected_earnings,
    }

    return render(request, 'accounts/interpreter_jobs.html', context)


def available_jobs_page(request, interpreter_id):
    """
    Template view for interpreters to see available jobs they can accept
    """
    interpreter = get_object_or_404(InterpreterProfile, id=interpreter_id)

    # Get unassigned jobs that match the interpreter's languages
    interpreter_languages = interpreter.get_languages()
    available_jobs = Job.objects.filter(status='unassigned').order_by('-date', '-time')

    # Filter jobs that require DSHS certification if interpreter doesn't have it
    if not interpreter.dshs_certified:
        available_jobs = available_jobs.filter(requires_dshs_certification=False)

    context = {
        'interpreter': interpreter,
        'available_jobs': available_jobs,
        'total_available': available_jobs.count(),
    }

    return render(request, 'accounts/available_jobs.html', context)


class AcceptJobView(APIView):
    """
    API endpoint for an interpreter to accept a job
    """
    def post(self, request, interpreter_id, job_id):
        interpreter = get_object_or_404(InterpreterProfile, id=interpreter_id)
        job = get_object_or_404(Job, id=job_id)

        # Assign the interpreter to the job
        job.assigned_interpreter = interpreter
        job.status = 'assigned'
        job.save()

        return Response({
            'success': True,
            'message': f'Job successfully assigned to {interpreter.first_name} {interpreter.last_name}',
            'job_id': job.id,
            'status': job.status
        }, status=status.HTTP_200_OK)


def accept_job(request, interpreter_id, job_id):
    """
    Template view for accepting a job (form submission)
    """
    if request.method == 'POST':
        interpreter = get_object_or_404(InterpreterProfile, id=interpreter_id)
        job = get_object_or_404(Job, id=job_id)

        # Assign the interpreter to the job
        job.assigned_interpreter = interpreter
        job.status = 'assigned'
        job.save()

        messages.success(request, f'You have successfully accepted the job!')
        return redirect('accounts:interpreter-jobs-page', interpreter_id=interpreter_id)

    # If not POST, redirect back to jobs page
    return redirect('accounts:interpreter-jobs-page', interpreter_id=interpreter_id)
