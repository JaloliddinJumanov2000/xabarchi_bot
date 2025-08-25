from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser

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


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Students

@api_view(["POST"])
def save_chat_id(request):
    phone = request.data.get("phone")
    chat_id = request.data.get("chat_id")

    try:
        student = Students.objects.get(parents_phone_number=phone)
        student.parents_chat_id = chat_id
        student.save()
        return Response({"status": "ok"})
    except Students.DoesNotExist:
        return Response({"error": "Student topilmadi"}, status=404)
