from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# GROUP
class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

# STUDENT
class Students(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="To'liq ismi")
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students', verbose_name="Guruh")
    student_phone_number = PhoneNumberField(region='UZ', blank=True, null=True, verbose_name="O'quvchi telefoni")
    parents_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ota-ona ismi")
    parents_phone_number = PhoneNumberField(region='UZ', blank=True, null=True, verbose_name="Ota-ona telefoni")

    parents_chat_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="Telegram Chat ID")
    
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"

# TEST
class Test(models.Model):
    test_title = models.CharField(max_length=100, verbose_name="Test nomi")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tests', verbose_name="Guruh")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.test_title}({self.group.name})"

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"
        ordering = ['-created_at']

class TestScore(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='scores', verbose_name="Test")
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='test_scores', verbose_name="O'quvchi")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Ball")
    comment = models.TextField(blank=True, null=True, verbose_name="Izoh")


    def __str__(self):
        return f"{self.student.full_name} | {self.test.test_title} | {self.score}"

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        unique_together = ['test', 'student']  # Bir test uchun bir o'quvchi faqat bir marta ball olishi mumkin