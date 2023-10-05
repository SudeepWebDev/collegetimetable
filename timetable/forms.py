from django import forms
from .models import Semester, Course, Faculty, Room, Section

class SemesterSelectionForm(forms.Form):
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label=None)
    section= forms.ModelChoiceField(queryset=Section.objects.all(), empty_label=None)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False, empty_label='Select Course')
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=False, empty_label='Select Faculty')
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False, empty_label='Select Room')
