from django.contrib import admin
from .models import Course, Subject, Room, Timing, Faculty, Semester, Timetable, TimetableEntry, Lecture

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["course_name", "course_code"]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["subject_name", "course"]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_number"]

@admin.register(Timing)
class TimingAdmin(admin.ModelAdmin):
    list_display = ["start_time", "end_time"]

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["faculty_name", "faculty_code"]

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ["Lecture_type", "Lecture_type_ff"]

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["semester_name", "is_current_sem"]

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "semester",
        "is_current_sem",
    ]

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = [
        "day",
        "lecture_type",
        "subject",
        "room",
        "timing",
        "faculty",
        "faculty_2",
    ]
    # Add unique constraint to ensure no duplicate entries
    unique_together = [
        'day',
        'lecture_type',
        'subject',
        'room',
        'timing',
        'faculty',
        'faculty_2',
    ]
