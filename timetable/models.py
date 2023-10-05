from django.db import models

# Choices for days
DAYS_CHOICES = [
    ("MONDAY", "Monday"),
    ("TUESDAY", "Tuesday"),
    ("WEDNESDAY", "Wednesday"),
    ("THURSDAY", "Thursday"),
    ("FRIDAY", "Friday"),
    ("SATURDAY", "Saturday"),
]


# Course Model
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.course_name

    def get_course_code(self):
        return self.course_code

# Section Model
class Section(models.Model):
    section_type = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.section_type
    
# Subject Model
class Subject(models.Model):
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.subject_name


# Room Model
class Room(models.Model):
    room_number = models.CharField(max_length=100)

    def __str__(self):
        return self.room_number


# Timing Model
class Timing(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


# Faculty Model
class Faculty(models.Model):
    faculty_name = models.CharField(max_length=200)
    faculty_code = models.CharField(max_length=100, default="CODE")

    def __str__(self):
        return self.faculty_name


# Lecture Model
class Lecture(models.Model):
    Lecture_type = models.CharField(
        max_length=100, default="TH", verbose_name="Lecture code"
    )
    Lecture_type_ff = models.CharField(
        max_length=100, default="Theory", verbose_name="Lecture Name"
    )

    def __str__(self):
        return str(self.Lecture_type_ff)


# Semester Model
class Semester(models.Model):
    semester_name = models.CharField(max_length=100)
    is_current_sem = models.BooleanField(
        verbose_name="Current Semester",
        default=True,
    )

    def __str__(self):
        return self.semester_name


# Timetable Model
class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    course_code = models.CharField(
        max_length=10, blank=True
    )  # Define course_code as CharField
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_current_sem = models.BooleanField(
        verbose_name="Current Semester",
        default=True,
    )

    def __str__(self):
        return f"{self.course.course_name} - {self.section.section_type} - {self.semester.semester_name} ({self.course.get_course_code()})"


class TimetableEntry(models.Model):
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, related_name="entries", default=None
    )
    day = models.CharField(max_length=100, choices=DAYS_CHOICES, verbose_name="Day")
    lecture_type = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, verbose_name="Lecture Type"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Subject"
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Room")
    timing = models.ForeignKey(Timing, on_delete=models.CASCADE, verbose_name="Timing")
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, verbose_name="Faculty"
    )
    faculty_2 = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faculty_2",
        verbose_name="Faculty 2 (for lab)",
    )
    faculty_3 = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faculty_3",
        verbose_name="Faculty 3 (for lab)",
    )
    faculty_4 = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faculty_4",
        verbose_name="Faculty 4 (for lab)",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="course"
    )


    def __str__(self):
        return f"{self.day} - {self.subject} - {self.timing} - {self.faculty}"


class Meta:
    unique_together = [
        "day",
        "lecture_type",
        "subject",
        "room",
        "timing",
        "faculty",
        "faculty_2",
        "faculty_3",
        "faculty_4",
    ]
