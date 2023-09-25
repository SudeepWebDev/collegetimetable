from datetime import datetime, timedelta
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
    return render(
        request,
        "time-table.html",
        {
            "rooms": rooms,
            "courses": courses,
            "semesters": semesters,
            "facultys": facultys,
        },
    )



def get_timetable_for_semester(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)

    # Filter TimetableEntry objects based on the semester
    timetable_entries = TimetableEntry.objects.filter(timetable__semester=semester)

    data = []

    for entry in timetable_entries:
        data.append({
            "day": entry.day,  # Day of the week
            "lecture_type": entry.lecture_type.Lecture_type,  # Lecture type (e.g., lab or theory)
            "subject": entry.subject.subject_name,  # Subject name
            "room": entry.room.room_number,  # Room number
            "timing": entry.timing.start_time,  # Timing/start time
            "faculty": entry.faculty.faculty_name,  # Faculty name
            "faculty_2": entry.faculty_2.faculty_name if entry.faculty_2 else None,  # Faculty 2 name (if available)
            # Add more fields as needed
        })

    # Iterate through entries to add breaks
    i = 0
    while i < len(data) - 1:
        current_timing = data[i]["timing"]
        next_timing = data[i + 1]["timing"]

        # Calculate the time difference in minutes
        time_diff_minutes = (datetime.combine(datetime.today(), next_timing) - datetime.combine(datetime.today(), current_timing)).total_seconds() / 60

        if time_diff_minutes > 60:
            # Calculate the number of breaks needed
            num_breaks = int(time_diff_minutes / 60)

            # Insert break entries
            for j in range(num_breaks - 1):
                break_entry = {
                    "day": data[i]["day"],
                    "lecture_type": "Break",
                    "subject": "Break",
                    "room": "",
                    "timing": (datetime.combine(datetime.today(), current_timing) + timedelta(minutes=60 * (j + 1))).time(),
                    "faculty": "",
                    "faculty_2": None,
                }
                data.insert(i + 1, break_entry)
                i += 1  # Skip the added break entry

        i += 1  # Move to the next entry

    context = {"timetable_entries": data}

    # Render the template and include the JSON data
    return render(request, "time-table.html", context)
    # return JsonResponse(data, safe=False)

def timetablehome(request):
    form = SemesterSelectionForm(request.POST or None)

    if form.is_valid():
        selected_semester = form.cleaned_data["semester"]
        timetable_entries1 = TimetableEntry.objects.filter(
            timetable__semester=selected_semester
        )
    else:
        timetable_entries = []

    return render(
        request,
        "time-table.html",
        {"form": form, "timetable_entries1": timetable_entries1},
    )
