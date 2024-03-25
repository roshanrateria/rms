from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.db.models import Count
from .models import Faculty, Class, TimeSlot, Day, Schedule

def index(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        if request.user.is_authenticated:
            faculty = Faculty.objects.get(user=request.user)
            schedules = Schedule.objects.filter(faculty=faculty)
            context = {'schedules': schedules}
            return render(request, 'Routine/index.html', context)
        else:
            return redirect('login')

@login_required
def generate_reports(request):
    if not request.user.is_superuser:
        return redirect('index')
    
    # Get all schedules grouped by faculty and day
    faculty_reports = Faculty.objects.annotate(num_classes=Count('schedule')).order_by('-num_classes')
    
    context = {'faculty_reports': faculty_reports}
    return render(request, 'Routine/reports.html', context)



@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('index')
    
    # Prefetch related objects to minimize database queries
    schedules = Schedule.objects.select_related('faculty', 'classroom', 'day', 'time_slot').order_by('time_slot__slot')
    
    # Initialize dictionaries to hold schedules for each day
    days = {day: [] for day, _ in Day.day_choices}
    
    # Organize schedules by day and period
    for schedule in schedules:
        days[schedule.day.day].append(schedule)
    
    # Prepare a list of periods
    periods = [time_slot.slot for time_slot in TimeSlot.objects.all()]
    faculties = Faculty.objects.all()
    classes = Class.objects.all()
    context = {'days': days, 'periods': periods, 'faculties': faculties, 'classes': classes}
    return render(request, 'Routine/admin_dashboard.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'Routine/login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'Routine/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def view_timetable(request):
    available_classes = [class_obj.name for class_obj in Class.objects.all()]
    if request.method == 'POST':
        selected_class = request.POST.get('class_name')
        cl=Class.objects.get(name=selected_class)
        schedules = Schedule.objects.select_related('faculty', 'classroom', 'day', 'time_slot').order_by('time_slot__slot')
        
        # Initialize dictionaries to hold schedules for each day
        days = {day: [] for day, _ in Day.day_choices}
        
        # Organize schedules by day and period
        for schedule in schedules:
            if schedule.classroom==cl:
                days[schedule.day.day].append(schedule)
        
        # Prepare a list of periods
        periods = [time_slot.slot for time_slot in TimeSlot.objects.all()]
        context = {'days': days, 'periods': periods,  'selected_class': selected_class,'available_classes': available_classes}
        return render(request, 'Routine/view_timetable.html', context)
    return render(request, 'Routine/view_timetable.html', {'available_classes': available_classes})


@login_required
def update_timetable(request):
    if not request.user.is_superuser:
        return redirect('index')
    if request.method == 'POST':
        try: 
            schedule_id = request.POST.get('schedule_id')
        except:
            schedule_id=None
        day_id = request.POST.get('day')
        TimeSlot_id = request.POST.get('period')
        faculty_id = request.POST.get('faculty')
        class_id = request.POST.get('class')

        day = Day.objects.get(day=day_id)
        timeslot = TimeSlot.objects.get(slot=TimeSlot_id)
        faculty = Faculty.objects.get(pk=faculty_id)
        class_assigned = Class.objects.get(pk=class_id)
        if Schedule.objects.filter(day=day, time_slot=timeslot, faculty=faculty, classroom=class_assigned).exists():
               return redirect('admin_dashboard')
        if schedule_id:
            schedule = Schedule.objects.get(pk=schedule_id)
            schedule.day = day
            schedule.time_slot = timeslot
            schedule.faculty = faculty
            schedule.classroom = class_assigned
            schedule.save()
        else:
            Schedule.objects.create(day=day, time_slot=timeslot, faculty=faculty, classroom=class_assigned)


    return redirect('admin_dashboard')

def alerts(request):
    if not request.user.is_superuser:
        return redirect('index')
    
    schedules = Schedule.objects.all()
    classes=Class.objects.all()
    day=Day.objects.all()
    period=TimeSlot.objects.all()
    
    alert_data = []
    for i in classes:
     for j in day:
       for k in period:
         try:
             q=Schedule.objects.get(day=j,time_slot=k,classroom=i)
         except:
        
            alert_data.append({
                'class_name': i.name,
                'period': k,
                'day': j,
                'faculty_name': 'Not Assigned'
            })
    
    conflicting_periods = []
    for schedule1 in schedules:
        for schedule2 in schedules:
            if schedule1 != schedule2 and schedule1.day == schedule2.day and schedule1.time_slot == schedule2.time_slot and schedule1.faculty == schedule2.faculty:
                conflicting_periods.append({
                    'faculty_name': schedule1.faculty.user,
                    'period': schedule1.time_slot,
                    'day':schedule1.day,
                    'conflicting_period': schedule2.classroom.name
                })
    
    context = {
        'alert_data': alert_data,
        'conflicting_periods': conflicting_periods
    }
    return render(request, 'Routine/alerts.html', context)