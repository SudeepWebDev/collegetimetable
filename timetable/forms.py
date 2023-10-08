from django import forms
from .models import Semester, Course, Faculty, Room, Section, Subject

class SemesterSelectionForm(forms.Form):
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label=None)
    section= forms.ModelChoiceField(queryset=Section.objects.all(), empty_label=None)
    course = forms.ModelChoiceField(
    queryset=Course.objects.exclude(course_code__in=['GE', 'SEC', 'VAC']),
    required=False,
    empty_label='Select Course'
)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=False, empty_label='Select Faculty')
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False, empty_label='Select Room')
    subject_ge = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)
    subject_sec = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)
    subject_vac = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter the queryset based on subject names containing "GE"
        self.fields['subject_ge'].queryset = Subject.objects.filter(
            subject_name__icontains='- GE')

        # Filter the queryset based on subject names containing "SEC"
        self.fields['subject_sec'].queryset = Subject.objects.filter(
            subject_name__icontains='- SEC')

        # Filter the queryset based on subject names containing "VAC"
        self.fields['subject_vac'].queryset = Subject.objects.filter(
            subject_name__icontains='- VAC')

