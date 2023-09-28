from datetime import datetime, timedelta
from itertools import groupby
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from .models import TimetableEntry
from .forms import SemesterSelectionForm

from django.shortcuts import get_object_or_404, render
from .models import Room, Course, Semester, Faculty

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

def get_timetable_entries(query_set):
    days_of_week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
    timetable_entries = sorted(
        query_set,
        key=lambda x: (days_of_week.index(x.day), x.timing.start_time),
    )
    data = []

    for entry in timetable_entries:
        data.append({
            "day": entry.day,
            "lecture_type": entry.lecture_type.Lecture_type,
            "subject": entry.subject.subject_name,
            "room": entry.room.room_number if hasattr(entry, 'room') else "",
            "timing": entry.timing.start_time,
            "faculty": entry.faculty.faculty_name if hasattr(entry, 'faculty') else "",
            "faculty_2": entry.faculty_2.faculty_name if hasattr(entry, 'faculty_2') and entry.faculty_2 else None,
        })

    i = 0
    while i < len(data) - 1:
        current_timing = data[i]["timing"]
        next_timing = data[i + 1]["timing"]

        time_diff_minutes = (
            datetime.combine(datetime.today(), next_timing)
            - datetime.combine(datetime.today(), current_timing)
        ).total_seconds() / 60
        if time_diff_minutes > 60:
            num_breaks = int(time_diff_minutes / 60)

            for j in range(num_breaks - 1):
                break_entry = {
                    "day": data[i]["day"],
                    "lecture_type": "Break",
                    "subject": "Break",
                    "room": "",
                    "timing": (
                        datetime.combine(datetime.today(), current_timing)
                        + timedelta(minutes=60 * (j + 1))
                    ).time(),
                    "faculty": "",
                    "faculty_2": None,
                }
                data.insert(i + 1, break_entry)
                i += 1

        i += 1

    for i in range(len(days_of_week)):
        day_entries = [
            entry for entry in timetable_entries if entry.day == days_of_week[i]
        ]

        if (
            day_entries
            and day_entries[0].timing.start_time
            > datetime.strptime("08:30:00", "%H:%M:%S").time()
        ):
            first_class_time = day_entries[0].timing.start_time
            num_breaks = int(
                (
                    datetime.combine(datetime.today(), first_class_time)
                    - datetime.combine(
                        datetime.today(),
                        datetime.strptime("08:30:00", "%H:%M:%S").time(),
                    )
                ).total_seconds()
                / 60
                / 60
            )

            for j in range(num_breaks):
                break_entry = {
                    "day": days_of_week[i],
                    "lecture_type": "Break",
                    "subject": "Break",
                    "room": "",
                    "timing": (
                        datetime.combine(
                            datetime.today(),
                            datetime.strptime("08:30:00", "%H:%M:%S").time(),
                        )
                        + timedelta(hours=j)
                    ).time(),
                    "faculty": "",
                    "faculty_2": None,
                }
                data.append(break_entry)

    data = sorted(data, key=lambda x: (days_of_week.index(x["day"]), x["timing"]))
    return data


def get_timetable_for_semester_and_course(request, semester_id, course_id):
    semester = get_object_or_404(Semester, id=semester_id)

    try:
        course = get_object_or_404(Course, course_name=course_id)
    except Course.DoesNotExist:
        return HttpResponse(f"Course with ID {course_id} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(
        timetable__semester=semester, timetable__course=course
    )

    data = get_timetable_entries(timetable_entries)

    context = {"timetable_entries": data}
    return render(request, "time-table.html", context)


def get_timetable_for_faculty(request, faculty_name):
    try:
        faculty = get_object_or_404(Faculty, faculty_name=faculty_name)
    except Faculty.DoesNotExist:
        return HttpResponse(f"Faculty with name {faculty_name} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(faculty=faculty)
    data = get_timetable_entries(timetable_entries)

    context = {"timetable_entries": data}
    return render(request, "time-table.html", context)


def get_timetable_for_room(request, room_number):
    try:
        room = get_object_or_404(Room, room_number=room_number)
    except Room.DoesNotExist:
        return HttpResponse(f"Room with number {room_number} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(room=room)
    data = get_timetable_entries(timetable_entries)

    context = {"timetable_entries": data}
    return render(request, "time-table.html", context)
