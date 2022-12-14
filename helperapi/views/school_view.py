from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import School

class SchoolView(ViewSet):

    def list(list,request):
        schools = School.objects.all()
        serialized = SchoolSerializer(schools, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )