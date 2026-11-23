import json
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import WellnessLogForm
from .models import WellnessLog


def is_admin_user(user):
    return user.is_superuser or user.is_staff or getattr(user, 'role', '').lower() == 'admin'


@login_required
def log_list(request):
    logs = WellnessLog.objects.filter(user=request.user).prefetch_related('triggers')
    stats = logs.aggregate(
        avg_stress=Avg('stress_level'),
        avg_sleep=Avg('sleep_hours'),
        total_logs=Count('id'),
    )
    return render(request, 'wellness/log_list.html', {'logs': logs, 'stats': stats})


@login_required
def log_create(request):
    if request.method == 'POST':
        form = WellnessLogForm(request.POST, user=request.user)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            form.save_m2m()
            messages.success(request, f"Wellness log for {log.log_date} saved.")
            return redirect('wellness:log_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = WellnessLogForm(user=request.user)
    return render(request, 'wellness/log_form.html', {'form': form, 'action': 'New'})


@login_required
def log_update(request, pk):
    log = get_object_or_404(WellnessLog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WellnessLogForm(request.POST, instance=log, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Wellness log for {log.log_date} updated.")
            return redirect('wellness:log_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = WellnessLogForm(instance=log, user=request.user)
    return render(request, 'wellness/log_form.html', {'form': form, 'action': 'Edit'})


@login_required
def log_delete(request, pk):
    log = get_object_or_404(WellnessLog, pk=pk, user=request.user)
    if request.method == 'POST':
        date_str = str(log.log_date)
        log.delete()
        messages.success(request, f"Wellness log for {date_str} deleted.")
        return redirect('wellness:log_list')
    return render(request, 'wellness/log_confirm_delete.html', {'log': log})


@login_required
def weekly_trends(request):
    seven_days_ago = timezone.localdate() - timedelta(days=6)
    logs = WellnessLog.objects.filter(
        user=request.user,
        log_date__gte=seven_days_ago,
    ).order_by('log_date')

    labels = [str(log.log_date) for log in logs]
    stress_data = [log.stress_level for log in logs]
    sleep_data = [float(log.sleep_hours) for log in logs]
    workload_data = [log.academic_workload for log in logs]

    context = {
        'logs': logs,
        'labels_json': json.dumps(labels),
        'stress_json': json.dumps(stress_data),
        'sleep_json': json.dumps(sleep_data),
        'workload_json': json.dumps(workload_data),
    }
    return render(request, 'wellness/weekly_trends.html', context)


@login_required
def admin_analytics(request):
    if not is_admin_user(request.user):
        messages.error(request, "Access denied. Administrators only.")
        return redirect('wellness:log_list')

    all_logs = WellnessLog.objects.all()
    summary = all_logs.aggregate(
        total_logs=Count('id'),
        active_students=Count('user', distinct=True),
        avg_stress=Avg('stress_level'),
        avg_sleep=Avg('sleep_hours'),
    )
    high_stress_count = all_logs.filter(stress_level__gte=8).count()
    return render(request, 'wellness/admin_analytics.html', {
        'summary': summary,
        'high_stress_count': high_stress_count,
    })