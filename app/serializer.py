from rest_framework import serializers
from .models import Group, Students, Test, TestScore


# GROUP SERIALIZER
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


# STUDENT SERIALIZER
class StudentSerializer(serializers.ModelSerializer):
    group_name = GroupSerializer(read_only=True)  # nested group info
    group_name_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        source="group_name",
        write_only=True
    )


    class Meta:
        model = Students
        fields = [
            'id',
            'full_name',
            'group_name',
            'group_name_id',
            'student_phone_number',
            'parents_name',
            'parents_phone_number',
        ]


# TEST SERIALIZER
class TestSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        source="group",
        write_only=True
    )

    class Meta:
        model = Test
        fields = ['id', 'test_title', 'group', 'group_id', 'created_at']


# TEST SCORE SERIALIZER
class TestScoreSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Students.objects.all(),
        source="student",
        write_only=True
    )

    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(),
        source="test",
        write_only=True
    )

    class Meta:
        model = TestScore
        fields = ['id', 'test', 'test_id', 'student', 'student_id', 'score','comment']
