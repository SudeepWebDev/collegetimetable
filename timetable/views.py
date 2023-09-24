from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from .models import TimetableEntry
from .forms import SemesterSelectionForm

from django.shortcuts import get_object_or_404, render
from .models import Room, Course, Semester, Faculty

def timetablehome(request):
    rooms = Room.objects.all()
    courses = Course.objects.all()
    semesters = Semester.objects.all()
    facultys = Faculty.objects.all()
    return render(request, 'time-table.html', {'rooms': rooms, 'courses': courses, 'semesters': semesters, 'facultys': facultys})

def get_timetable_for_semester(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    
    # Filter TimetableEntry objects based on the semester
    timetable_entries = TimetableEntry.objects.filter(timetable__semester=semester)
    
    data = [
        {
            "day": entry.day,                     # Day of the week
            "lecture_type": entry.lecture_type.Lecture_type,  # Lecture type (e.g., lab or theory)
            "subject": entry.subject.subject_name,  # Subject name
            "room": entry.room.room_number,        # Room number
            "timing": entry.timing.start_time,     # Timing/start time
            "faculty": entry.faculty.faculty_name, # Faculty name
            "faculty_2": entry.faculty_2.faculty_name if entry.faculty_2 else None,  # Faculty 2 name (if available)
            # Add more fields as needed
        }
        for entry in timetable_entries
    ]
    return JsonResponse(data, safe=False)

def timetablehome(request):
    form = SemesterSelectionForm(request.POST or None)

    if form.is_valid():
        selected_semester = form.cleaned_data['semester']
        timetable_entries = TimetableEntry.objects.filter(timetable__semester=selected_semester)
    else:
        timetable_entries = []

    return render(request, 'time-table.html', {'form': form, 'timetable_entries': timetable_entries})

