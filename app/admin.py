from django.contrib import admin
from .models import Group, Students, Test, TestScore


# STUDENT INLINE (Group ichida ko‘rsatish uchun)
class StudentInline(admin.TabularInline):
    model = Students
    extra = 1
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
    list_display = ("full_name", "group_name", "student_phone_number", "parents_name", "parents_phone_number", "has_telegram")
    search_fields = ("full_name", "parents_name", "student_phone_number", "parents_phone_number")
    list_filter = ("group_name",)
    list_display_links = ("full_name",)
    actions = ["clear_all_students", "clear_telegram_ids"]

    def has_telegram(self, obj):
        return "✅" if obj.parents_chat_id else "❌"
    has_telegram.short_description = "Telegram"
    def clear_all_students(self, request, queryset):
        count, _ = Students.objects.all().delete()
        self.message_user(request, f"✅ {count} ta o'quvchi o'chirildi")

    clear_all_students.short_description = "🗑 Barcha o‘quvchilarni o‘chirish"
    def clear_telegram_ids(self, request, queryset):
        count = queryset.update(parents_chat_id=None)
        self.message_user(request, f"✅ {count} ta o'quvchining Telegram ID si o'chirildi")

    clear_telegram_ids.short_description = "📱 Telegram ID larni tozalash"



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
    list_display = ("id", "test", "student", "score", "comment", "telegram_sent")
    search_fields = ("test__test_title", "student__full_name")
    list_filter = ("test", "student__group_name")
    ordering = ("-id",)

    def telegram_sent(self, obj):
        return "✅" if obj.student.parents_chat_id else "❌"
    telegram_sent.short_description = "Telegram yuborildi"