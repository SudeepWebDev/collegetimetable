from datetime import datetime, timedelta
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from .models import TimetableEntry
from .forms import SemesterSelectionForm

from django.shortcuts import get_object_or_404, render
from .models import Room, Course, Semester, Faculty

def get_timetable_for_semester_and_course(request, semester_id, course_id):

    semester = get_object_or_404(Semester, id=semester_id)
        
    try:
            course = get_object_or_404(Course, course_name=course_id)
    except Course.DoesNotExist:
            return HttpResponse(f"Course with ID {course_id} does not exist.")  # Debugging output
        
    timetable_entries = TimetableEntry.objects.filter(
            timetable__semester=semester,
            timetable__course=course  
        )
    days_of_week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
    timetable_entries = sorted(timetable_entries, key=lambda x: (days_of_week.index(x.day), x.timing.start_time))
    data = []


    for entry in timetable_entries:
        data.append({
            "day": entry.day,  # Day of the week
            "lecture_type": entry.lecture_type.Lecture_type,  # Lecture type (lab or theory)
            "subject": entry.subject.subject_name,  # Subject name
            "room": entry.room.room_number,  # Room number
            "timing": entry.timing.start_time,  # Timing/start time
            "faculty": entry.faculty.faculty_name,  # Faculty name
            "faculty_2": entry.faculty_2.faculty_name if entry.faculty_2 else None,  # Faculty 2 name (if available)
        })

    data = sorted(data, key=lambda x: (days_of_week.index(x["day"]), x["timing"]))
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
                i += 1  

        i += 1  # Move to the next entry

    for i in range(len(days_of_week)):
            day_entries = [entry for entry in timetable_entries if entry.day == days_of_week[i]]

            # If the first class on the day doesn't start at 8:30, add breaks
            if day_entries and day_entries[0].timing.start_time > datetime.strptime("08:30:00", "%H:%M:%S").time():
                first_class_time = day_entries[0].timing.start_time

                # Calculate the number of breaks needed
                num_breaks = int((datetime.combine(datetime.today(), first_class_time) - datetime.combine(datetime.today(), datetime.strptime("08:30:00", "%H:%M:%S").time())).total_seconds() / 60 / 60)

                # Insert break entries
                for j in range(num_breaks):
                    break_entry = {
                        "day": days_of_week[i],
                        "lecture_type": "Break",
                        "subject": "Break",
                        "room": "",
                        "timing": (datetime.combine(datetime.today(), datetime.strptime("08:30:00", "%H:%M:%S").time()) + timedelta(hours=j)).time(),
                        "faculty": "",
                        "faculty_2": None,
                    }
                    data.append(break_entry)
    data = sorted(data, key=lambda x: (days_of_week.index(x["day"]), x["timing"]))
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
        timetable_entries1 = []

    return render(
        request,
        "time-table.html",
        {"form": form, "timetable_entries1": timetable_entries1},
    )
