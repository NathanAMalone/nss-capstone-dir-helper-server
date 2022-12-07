from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import School, Uniform

class UniformView(ViewSet):

    def list(list,request):

        uniforms = Uniform.objects.all()
        serialized = UniformSerializer(uniforms, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):

        uniform = Uniform.objects.get(pk=pk)
        serialized = UniformSerializer(uniform, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):

        serializer = CreateUniformSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):

        uniform = Uniform.objects.get(pk=pk)
        uniform.uniform_number = request.data["uniform_number"]
        uniform.size = request.data["size"]
        uniform.out_for_cleaning = request.data["out_for_cleaning"]
        uniform.assigned = request.data["assigned"]
        school = School.objects.get(pk=request.data["school"])
        uniform.school = school
        uniform.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):

        uniform = Uniform.objects.get(pk=pk)
        uniform.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreateUniformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uniform
        fields = ['id', 'uniform_number', 'size', 'out_for_cleaning', 'assigned', 'school', ]

class UniformSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Uniform
        fields = ('id', 'uniform_number', 'size', 'out_for_cleaning', 'assigned', 'school', )