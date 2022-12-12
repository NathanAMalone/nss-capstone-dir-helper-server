from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import School, Uniform, Director

class UniformView(ViewSet):

    def list(list,request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            uniforms = Uniform.objects.filter(school=director.school)
            serialized = UniformSerializer(uniforms, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            uniform = Uniform.objects.get(pk=pk)
            if uniform.school == director.school:
                serialized = UniformSerializer(uniform, context={'request': request})
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'ERROR: This uniform is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            school = director.school
            serializer = CreateUniformSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(school=school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You must be a director to create this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            uniform = Uniform.objects.get(pk=pk)
            if uniform.school == director.school:
                uniform.uniform_number = request.data["uniform_number"]
                uniform.size = request.data["size"]
                uniform.out_for_cleaning = request.data["out_for_cleaning"]
                uniform.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This uniform is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to update this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            uniform = Uniform.objects.get(pk=pk)
            if uniform.school == director.school:
                uniform.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This uniform is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to delete this data.'},status=status.HTTP_401_UNAUTHORIZED)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreateUniformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uniform
        fields = ['id', 'uniform_number', 'size', 'out_for_cleaning', 'assigned', ]

class UniformSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Uniform
        fields = ('id', 'uniform_number', 'size', 'out_for_cleaning', 'assigned', 'school', )