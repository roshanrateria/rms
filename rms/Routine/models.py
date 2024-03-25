from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    # You can add more fields like email, contact number, etc. as per your requirements

    def __str__(self):
        return self.user.username

class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    slot_choices = [
        ('1st', '1st (09.30‐10.20)'),
        ('2nd', '2nd (10.20‐11.10)'),
        ('3rd', '3rd (11.10‐12.00)'),
        ('4th', '4th (12.00‐12.50)'),
        ('5th', '5th (1.40‐02.30)'),
        ('6th', '6th (02.30‐03.20)'),
        ('7th', '7th (03.20-04.10)'),
        ('8th', '8th (04.10-05.00)'),
    ]
    slot = models.CharField(max_length=5, choices=slot_choices)

    def __str__(self):
        return self.slot

class Day(models.Model):
    day_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    day = models.CharField(max_length=10, choices=day_choices)

    def __str__(self):
        return self.day

class Schedule(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    # Add more fields if needed, like subject, class, etc.

    def __str__(self):
        return f'{self.day} - {self.time_slot}: {self.faculty.user.username} ({self.classroom})'
