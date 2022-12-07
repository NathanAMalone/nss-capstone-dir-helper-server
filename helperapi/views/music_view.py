from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import Music, School

class MusicView(ViewSet):

    def list(list,request):
        if request.auth.user.is_staff == True:
            musics = Music.objects.all()
            serialized = MusicSerializer(musics, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):

        if request.auth.user.is_staff == True:
            music = Music.objects.get(pk=pk)
            serialized = MusicSerializer(music, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request):

        if request.auth.user.is_staff == True:
            serializer = CreateMusicSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You must be a director to create this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):

        if request.auth.user.is_staff == True:
            music = Music.objects.get(pk=pk)
            music.name = request.data["name"]
            music.part = request.data["part"]
            music.assigned = request.data["assigned"]
            school = School.objects.get(pk=request.data["school"])
            music.school = school
            music.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You must be a director to update this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):

        if request.auth.user.is_staff == True:
            music = Music.objects.get(pk=pk)
            music.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You must be a director to delete this data.'},status=status.HTTP_401_UNAUTHORIZED)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreateMusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ['id', 'name', 'part', 'assigned', 'school', ]

class MusicSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Music
        fields = ('id', 'name', 'part', 'assigned', 'school', )