from django.contrib import admin
from .models import Group, Students, Test, TestScore


# STUDENT INLINE (Group ichida ko‘rsatish uchun)
class StudentInline(admin.TabularInline):  # yoki admin.StackedInline
    model = Students
    extra = 1   # yangi qo‘shish uchun bo‘sh qator
    fields = ("full_name", "student_phone_number", "parents_name", "parents_phone_number")
    show_change_link = True


# GROUP ADMIN
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "student_count")  # ustunlar
    search_fields = ("name",)                       # qidiruv
    inlines = [StudentInline]                       # ichiga Students qo‘shish

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "O‘quvchilar soni"


# STUDENT ADMIN

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ("full_name", "group_name", "student_phone_number", "parents_name", "parents_phone_number")
    search_fields = ("full_name", "parents_name", "student_phone_number", "parents_phone_number")
    list_filter = ("group_name",)
    list_display_links = ("full_name",)
    actions = ["clear_all_students"]

    def clear_all_students(self, request, queryset):
        count, _ = Students.objects.all().delete()
        self.message_user(request, f"✅ {count} ta o‘quvchi o‘chirildi", level="warning")

    clear_all_students.short_description = "🗑 Barcha o‘quvchilarni o‘chirish"




# TEST ADMIN
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "test_title", "group", "created_at")
    search_fields = ("test_title", "group__name")
    list_filter = ("group", "created_at")
    ordering = ("-created_at",)


# TEST SCORE ADMIN
@admin.register(TestScore)
class TestScoreAdmin(admin.ModelAdmin):
    list_display = ("id", "test", "student", "score", "comment")
    search_fields = ("test__test_title", "student__full_name")
    list_filter = ("test", "student__group_name")
    ordering = ("-id",)
