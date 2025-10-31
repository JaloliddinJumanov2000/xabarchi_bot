from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# GROUP
class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# STUDENT
class Students(models.Model):
    full_name = models.CharField(max_length=100)
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    student_phone_number = PhoneNumberField(region='UZ', blank=True, null=True)
    parents_name = models.CharField(max_length=100, blank=True, null=True)
    parents_phone_number = PhoneNumberField(region='UZ', blank=True, null=True, unique=True)

    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    parents_chat_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.full_name


# TEST
class Test(models.Model):
    test_title = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tests')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_title} ({self.group.name})"


# TEST SCORE
class TestScore(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='scores')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='test_scores')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.full_name} | {self.test.test_title} | {self.score}"
