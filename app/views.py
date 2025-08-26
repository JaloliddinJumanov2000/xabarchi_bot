from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.models import Students, Group, Test, TestScore
from app.serializer import (
    StudentSerializer,
    GroupSerializer,
    TestSerializer,
    TestScoreSerializer,
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


@api_view(["GET"])
@permission_classes([AllowAny])
def students_by_phone(request):
    """Telefon raqami bo'yicha o'quvchilarni topish"""
    phone = request.GET.get("phone")
    
    if not phone:
        return Response({"error": "Phone parameter majburiy"}, status=400)
    
    try:
        students = Students.objects.filter(parents_phone_number=phone)
        
        result = []
        for student in students:
            result.append({
                "id": student.id,
                "full_name": student.full_name,
                "group_name": {
                    "name": student.group_name.name
                }
            })
        
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([AllowAny])
def save_chat_id(request):
    """Telegram bot orqali chat_id ni saqlash"""
    phone = request.data.get("phone")
    chat_id = request.data.get("chat_id")
    student_id = request.data.get("student_id")

    if not phone or not chat_id:
        return Response({"error": "Phone va chat_id majburiy"}, status=400)
    
    try:
        if student_id:
            # Aniq o'quvchi ID si berilgan bo'lsa
            student = Students.objects.get(id=student_id, parents_phone_number=phone)
        else:
            # Faqat telefon raqami bo'yicha (bitta o'quvchi bo'lsa)
            student = Students.objects.get(parents_phone_number=phone)
        
        student.parents_chat_id = chat_id
        student.save()
        
        print(f"✅ {student.full_name} uchun chat_id saqlandi: {chat_id}")
        return Response({
            "status": "success", 
            "message": "Chat ID muvaffaqiyatli saqlandi",
            "student": student.full_name,
            "group": student.group_name.name
        })
    except Students.DoesNotExist:
        print(f"❌ O'quvchi topilmadi: phone={phone}, student_id={student_id}")
        return Response({"error": "Bu telefon raqami bilan ro'yxatdan o'tgan o'quvchi topilmadi"}, status=404)
    except Students.MultipleObjectsReturned:
        print(f"❌ Bir nechta o'quvchi topildi: {phone}")
        return Response({"error": "Bir nechta o'quvchi topildi, student_id ni ham yuboring"}, status=400)