from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import Students, Group, Test, TestScore
from app.serializer import (
    StudentSerializer,
    GroupSerializer,
    TestSerializer,
    TestScoreSerializer,
)


from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(summary="Barcha o‘quvchilar ro‘yxati"),
    retrieve=extend_schema(summary="Bitta o‘quvchi ma'lumotlari"),
    create=extend_schema(summary="Yangi o‘quvchi qo‘shish"),
    update=extend_schema(summary="O‘quvchi ma'lumotini yangilash"),
    partial_update=extend_schema(summary="O‘quvchi ma'lumotini qisman yangilash"),
    destroy=extend_schema(summary="O‘quvchi o‘chirish"),
)

# STUDENTS
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'parents_name', 'student_phone_number']
    permission_classes = [IsAdminUser]


# GROUP
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [IsAdminUser]


# TEST
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['test_title', 'group__name']
    permission_classes = [IsAdminUser]


# TEST SCORE
class TestScoreViewSet(viewsets.ModelViewSet):
    queryset = TestScore.objects.all()
    serializer_class = TestScoreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['student__full_name', 'test__test_title']
    permission_classes = [IsAdminUser]


# ✅ OTA-ONA CHAT ID SAQLASH API
@api_view(["POST"])
def save_chat_id(request):
    """
    Ota-onaning Telegram chat_id sini saqlash uchun API.
    Telegram botdan quyidagi formatda POST so‘rov yuboriladi:
    {
        "phone": "+998901234567",
        "chat_id": "123456789"
    }
    """
    phone = request.data.get("phone")
    chat_id = request.data.get("chat_id")

    # 1️⃣ Ma'lumotlar to‘liq kiritilganini tekshirish
    if not phone or not chat_id:
        return Response(
            {"error": "Telefon raqami yoki chat_id yuborilmadi."},
            status=400
        )

    # 2️⃣ Telefon raqamini formatlash
    phone = str(phone).replace(" ", "").replace("-", "")
    if phone.startswith("998"):
        phone = "+" + phone
    elif not phone.startswith("+998"):
        phone = "+998" + phone[-9:]

    # 3️⃣ Bazadan ota-onani topish
    try:
        student = Students.objects.get(parents_phone_number=phone)
    except Students.DoesNotExist:
        return Response(
            {"error": f"{phone} raqamli ota-ona topilmadi."},
            status=404
        )

    # 4️⃣ Chat ID ni saqlash
    student.parents_chat_id = str(chat_id)
    student.save(update_fields=["parents_chat_id"])

    return Response({
        "status": "ok",
        "message": f"{student.parents_name or 'Ota-ona'} uchun chat_id saqlandi.",
        "student": student.full_name,
        "group": student.group_name.name if student.group_name else None
    })
