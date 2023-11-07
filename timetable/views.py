from django.db.models import Q
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from .models import Subject, TimetableEntry, Room
from .forms import (
    Course_selection,
    Faculty_selection,
    Room_selection,
    Ge_selection,
    Sec_selection,
    Vac_selection,
)

from django.shortcuts import get_object_or_404, render
from .models import Room, Course, Semester, Faculty, Section


def timetablehome(request):
    # Create instances of all your form classes
    course_selection = Course_selection()
    faculty_selection = Faculty_selection()
    room_selection = Room_selection()
    ge_selection = Ge_selection()
    sec_selection = Sec_selection()
    vac_selection = Vac_selection()

    # Check if the request is an AJAX request and includes the 'option' parameter
    if (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        and "option" in request.GET
    ):
        option = request.GET.get("option")

        # Depending on the selected option, choose the appropriate form
        if option == "faculty-opt":
            form = faculty_selection
            template_part = "faculty-part.html"
        elif option == "room-opt":
            form = room_selection
            template_part = "room-part.html"
        elif option == "ge-opt":
            form = ge_selection
            template_part = "ge-part.html"
        elif option == "sec-opt":
            form = sec_selection
            template_part = "sec-part.html"
        elif option == "vac-opt":
            form = vac_selection
            template_part = "vac-part.html"
        else:
            form = None

        if form is not None:
            return render(
                request,
                template_part,
                {"form": form},
            )
    return render(
        request,
        "time-table.html",
        {"form": course_selection},
    )

def vacant_room(request):
   
    return render(
        request,
        "vacant-room.html",
    )


def search_rooms(request):
    if request.method == 'POST':
        # Retrieve the selected day and time from the request's POST data
        selected_day = request.POST.get('day')
        selected_time = request.POST.get('time')

        # Query the database for available rooms based on selected_day and selected_time
        not_available_rooms1 = TimetableEntry.objects.filter(day=selected_day, timing__start_time=selected_time)
        not_available_rooms = [entry.room.room_number for entry in not_available_rooms1]

        all_room_numbers = Room.objects.values_list('room_number', flat=True)
        # Convert the queryset to a list
        room_numbers_list = list(all_room_numbers)
        
        available_rooms = [item for item in room_numbers_list if item not in not_available_rooms]
        # print(room_numbers_list)
        # print(not_available_rooms)
        # print(available_rooms)

        response_data = {
            'available_rooms': available_rooms,
            'selected_day': selected_day,
            'selected_time': selected_time
        }

        return render(request, "vacant-room.html", response_data)

    else:
        # Handle cases where the form is not submitted with a POST request
        return JsonResponse({'error': 'Invalid request method'})

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
                "lecture_type": entry.lecture_type.Lecture_type_ff,  # Lecture type (lab or theory)
                "subject": entry.subject.subject_name,  # Subject name
                "room": entry.room.room_number if room_bool else "",  # Room number
                "timing": entry.timing.start_time,  # Timing/start time
                "faculty": entry.faculty if faculty_bool else "",  # Faculty name
                "faculty_2": entry.faculty_2
                if entry.faculty_2 and faculty_bool
                else "",
                "faculty_3": entry.faculty_3
                if entry.faculty_3 and faculty_bool
                else "",
                "faculty_4": entry.faculty_4
                if entry.faculty_4 and faculty_bool
                else "",
                "course": entry.course if course_bool else "",
            }
        )

    data = sorted(data, key=lambda x: (days_of_week.index(x["day"]), x["timing"]))

    # Iterate through days of the week
    for i in range(len(days_of_week)):
        day_entries = [
            entry for entry in timetable_entries if entry.day == days_of_week[i]
        ]

        # Sort entries by start time
        day_entries.sort(key=lambda x: x.timing.start_time)

        # Iterate through classes to add breaks between consecutive classes
        for j in range(1, len(day_entries)):
            current_class_end_time = day_entries[j - 1].timing.end_time
            next_class_start_time = day_entries[j].timing.start_time

            # Check if there is a gap between classes
            if current_class_end_time < next_class_start_time:
                # Calculate the number of breaks needed
                num_breaks = int(
                    (
                        datetime.combine(datetime.today(), next_class_start_time)
                        - datetime.combine(datetime.today(), current_class_end_time)
                    ).total_seconds()
                    / 60
                    / 60
                )

                # Insert break entries
                for k in range(num_breaks):
                    break_entry = {
                        "day": days_of_week[i],
                        "lecture_type": "Break",
                        "subject": "Break",
                        "room": "",
                        "timing": (
                            datetime.combine(datetime.today(), current_class_end_time)
                            + timedelta(hours=k)
                        ).time(),
                        "faculty": "",
                        "faculty_2": "",
                        "faculty_3": "",
                        "faculty_4": "",
                    }
                    data.append(break_entry)

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
                    "faculty_2": "",
                    "faculty_3": "",
                    "faculty_4": "",
                }
                data.append(break_entry)
    # Adding breaks after classes
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
                    "faculty_2": "",
                    "faculty_3": "",
                    "faculty_4": "",
                }
                data.append(break_entry)

    days_in_timetable = {entry.day for entry in timetable_entries}
    days_without_classes = set(days_of_week) - days_in_timetable
    # managing days without classes

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
                "faculty_2": "",
                "faculty_3": "",
                "faculty_4": "",
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
    # return JsonResponse(data, safe=False)
    return render(request, "time-table.html", context)


def get_timetable_for_semester_and_course(request, semester_id, course_id, section_id):
    semester = get_object_or_404(Semester, semester_name=semester_id)

    try:
        course = get_object_or_404(Course, course_name=course_id)
        section = get_object_or_404(Section, section_type=section_id)
    except Course.DoesNotExist:
        return HttpResponse(f"Course with ID {course_id} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(
        timetable__semester=semester,
        timetable__course=course,
        timetable__section=section,
    )
    # room_bool, course_bool, faculty_bool
    return get_timetable(request, timetable_entries, True, False, True)


def get_timetable_for_faculty(request, faculty_code, faculty_name):
    try:
        faculty = get_object_or_404(Faculty, faculty_code=faculty_code)
    except Faculty.DoesNotExist:
        return HttpResponse(f"Faculty with name {faculty_name} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(
        Q(faculty=faculty)
        | Q(faculty_2=faculty)
        | Q(faculty_3=faculty)
        | Q(faculty_4=faculty)
    )

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


def get_timetable_for_gvs(request, subject_name, section_id, semester_id):
    try:
        semester = get_object_or_404(Semester, semester_name=semester_id)
        section = get_object_or_404(Section, section_type=section_id)
        subject = get_object_or_404(Subject, subject_name=subject_name)

    except Semester.DoesNotExist:
        return HttpResponse(f"Semester with number {semester_id} does not exist.")

    timetable_entries = TimetableEntry.objects.filter(
        timetable__semester=semester,
        subject__subject_name=subject,
        timetable__section=section,
    )

    # room_bool, course_bool, faculty_bool
    return get_timetable(request, timetable_entries, True, True, True)
