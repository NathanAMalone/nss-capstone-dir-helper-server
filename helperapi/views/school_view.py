from django.http import HttpResponseServerError
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import School, Director

class SchoolView(ViewSet):
    permission_classes = [AllowAny]
    
    def list(list,request):
        schools = School.objects.all()
        serialized = SchoolSerializer(schools, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            if request.auth.user.is_staff == True:
                school = School.objects.get(pk=pk)
                serialized = SchoolSerializer(school, context={'request': request})
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
        except School.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )