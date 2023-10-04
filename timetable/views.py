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
# Common for both faculty, course and room --> sorting and adding breaks
def get_timetable(request, timetable_entries, room_bool, course_bool, faculty_bool):
    days_of_week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
    timetable_entries = sorted(
        timetable_entries,
        key=lambda x: (days_of_week.index(x.day), x.timing.start_time),
    )
    data = []

    for entry in timetable_entries:
        data.append(
            {
                "day": entry.day,  # Day of the week
                "lecture_type": entry.lecture_type.Lecture_type,  # Lecture type (lab or theory)
                "subject": entry.subject.subject_name,  # Subject name
                "room": entry.room.room_number if room_bool else "",  # Room number
                "timing": entry.timing.start_time,  # Timing/start time
                "faculty": entry.faculty.faculty_name
                if faculty_bool
                else "",  # Faculty name
                "faculty_2": entry.faculty_2.faculty_name
                if entry.faculty_2
                else None,  # Faculty 2 name (if available)
                "course": entry.course if course_bool else "",
            }
        )

    data = sorted(data, key=lambda x: (days_of_week.index(x["day"]), x["timing"]))
    # Iterate through entries to add breaks
    for i in range(len(data) - 1):
        current_timing = data[i]["timing"]
        next_timing = data[i + 1]["timing"]

        time_diff_hour = (
            datetime.combine(datetime.today(), next_timing)
            - datetime.combine(datetime.today(), current_timing)
        ).total_seconds() / 3600

        if time_diff_hour > 1:
            num_breaks = int(time_diff_hour )

            for j in range(1, num_breaks):
                break_timing = (
                    datetime.combine(datetime.today(), current_timing)
                    + timedelta(minutes=60 * j)
                ).time()

                break_entry = {
                    "day": data[i]["day"],
                    "lecture_type": "Break",
                    "subject": "Break",
                    "room": "",
                    "timing": break_timing,
                    "faculty": "",
                    "faculty_2": None,
                }

                data.insert(i + j, break_entry)


    for i in range(len(days_of_week)):
        day_entries = [
            entry for entry in timetable_entries if entry.day == days_of_week[i]
        ]

        # If the first class on the day doesn't start at 8:30, add breaks
        if (
            day_entries
            and day_entries[0].timing.start_time
            > datetime.strptime("08:30:00", "%H:%M:%S").time()
        ):
            first_class_time = day_entries[0].timing.start_time

            # Calculate the number of breaks needed
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

            # Insert break entries
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
    print(data)
    print()
    for i in range(len(days_of_week)):
        day_entries = [
            entry for entry in timetable_entries if entry.day == days_of_week[i]
        ]

        # If the last class on the day doesn't end at 4:30, add breaks
        if (
            day_entries
            and day_entries[-1].timing.end_time
            < datetime.strptime("17:30:00", "%H:%M:%S").time()
        ):
            last_class_end_time = day_entries[-1].timing.end_time

            # Calculate the number of breaks needed
            num_breaks = int(
                (
                    datetime.combine(
                        datetime.today(),
                        datetime.strptime("17:30:00", "%H:%M:%S").time(),
                    )
                    - datetime.combine(datetime.today(), last_class_end_time)
                ).total_seconds()
                / 60
                / 60
            )

            # Insert break entries
            for j in range(num_breaks):
                break_entry = {
                    "day": days_of_week[i],
                    "lecture_type": "",
                    "subject": "",
                    "room": "",
                    "timing": (
                        datetime.combine(datetime.today(), last_class_end_time)
                        + timedelta(hours=j)
                    ).time(),
                    "faculty": "",
                    "faculty_2": None,
                }
                data.append(break_entry)
    print(data)
    print()

    days_in_timetable = {entry.day for entry in timetable_entries}
    days_without_classes = set(days_of_week) - days_in_timetable
    
    for day in days_without_classes:
        num_breaks = int(
            (
                datetime.combine(
                    datetime.today(),
                    datetime.strptime("17:30:00", "%H:%M:%S").time(),
                )
                - datetime.combine(
                    datetime.today(),
                    datetime.strptime("08:30:00", "%H:%M:%S").time(),
                )
            ).total_seconds()
            / 60
            / 60
        )
        # Insert break entries
        for j in range(num_breaks):
            break_entry = {
                "day": day,
                "lecture_type": "",
                "subject": "",
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
    context = {
            "timetable_entries": data,
            "daysloop": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
    }    
    print(context)
    # return JsonResponse(data, safe=False)
    return render(request, "time-table.html", context)

def get_timetable_for_semester_and_course(request, semester_id, course_id):
    semester = get_object_or_404(Semester, id=semester_id)

    try:
        course = get_object_or_404(Course, course_name=course_id)
    except Course.DoesNotExist:
        return HttpResponse(f"Course with ID {course_id} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(
        timetable__semester=semester, timetable__course=course
    )
    # room_bool, course_bool, faculty_bool
    return get_timetable(request, timetable_entries, True, False, True)


def get_timetable_for_faculty(request, faculty_name):
    try:
        faculty = get_object_or_404(Faculty, faculty_name=faculty_name)
    except Faculty.DoesNotExist:
        return HttpResponse(f"Faculty with name {faculty_name} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(faculty=faculty)

    # room_bool, course_bool, faculty_bool
    return get_timetable(request, timetable_entries, True, True, False)


def get_timetable_for_room(request, room_number):
    try:
        room = get_object_or_404(Room, room_number=room_number)
    except Room.DoesNotExist:
        return HttpResponse(f"Room with number {room_number} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(room=room)
    # room_bool, course_bool, faculty_bool
    return get_timetable(request, timetable_entries, False, True, True)