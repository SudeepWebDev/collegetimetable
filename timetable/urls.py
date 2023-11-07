from django.urls import path
from . import views

urlpatterns = [
    path("timetable/", views.timetablehome, name="timetablehome"),
    path("timetable/vacant-room", views.vacant_room, name="vacant_room"),
     path('search-rooms/', views.search_rooms, name='search_rooms'),
    path(
        "timetable/course/<int:semester_id>/<str:course_id>/<str:section_id>/",
        views.get_timetable_for_semester_and_course,
        name="get_timetable_for_semester_and_course",
    ),
    path(
        "timetable/faculty/<str:faculty_code>/<str:faculty_name>/",
        views.get_timetable_for_faculty,
        name="faculty_timetable",
    ),
    path(
        "timetable/room/<str:room_number>/",
        views.get_timetable_for_room,
        name="room_timetable",
    ),
    path(
        "timetable/gvs/<str:subject_name>/<str:section_id>/<str:semester_id>/",
        views.get_timetable_for_gvs,
        name="gvs_timetable",
    ),
]
