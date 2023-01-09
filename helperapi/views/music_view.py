from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import Music, School, Director

class MusicView(ViewSet):

    def list(list,request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            musics = Music.objects.filter(school=director.school).order_by("name")
            serialized = MusicSerializer(musics, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):
        try:
            if request.auth.user.is_staff == True:
                director = Director.objects.get(user=request.auth.user)
                music = Music.objects.get(pk=pk)
                if music.school == director.school:
                    serialized = MusicSerializer(music, context={'request': request})
                    return Response(serialized.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'ERROR: This music is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
        except Music.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            school = director.school
            serializer = CreateMusicSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(school=school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You must be a director to create this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            music = Music.objects.get(pk=pk)
            if music.school == director.school:
                music.name = request.data["name"]
                music.part = request.data["part"]
                music.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This music is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to update this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            music = Music.objects.get(pk=pk)
            if music.school == director.school:            
                music.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This music is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to delete this data.'},status=status.HTTP_401_UNAUTHORIZED)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreateMusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ['id', 'name', 'part', 'assigned', ]

class MusicSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Music
        fields = ('id', 'name', 'part', 'assigned', 'school', )