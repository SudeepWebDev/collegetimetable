from django.urls import path
from . import views

urlpatterns = [
    path("", views.timetablehome, name="timetablehome"),
    path('api/get_timetable/<int:semester_id>/', views.get_timetable_for_semester, name='get_timetable_for_semester'),
]
