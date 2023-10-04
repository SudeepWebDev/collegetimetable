from django.contrib import admin
from .models import Course, Subject, Room, Timing, Faculty, Lecture, Semester, Timetable, TimetableEntry

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["course_name", "course_code"]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["subject_name", "subject_code"]

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

class TimetableEntryInline(admin.TabularInline):
    model = TimetableEntry
    extra = 1  

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "course_code",
        "semester",
        "is_current_sem",
    ]
    inlines = [TimetableEntryInline]

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
