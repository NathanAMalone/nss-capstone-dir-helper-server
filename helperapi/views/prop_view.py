from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import School, Prop

class PropView(ViewSet):

    def list(list,request):

        props = Prop.objects.all()
        serialized = PropSerializer(props, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):

        prop = Prop.objects.get(pk=pk)
        serialized = PropSerializer(prop, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):

        serializer = CreatePropSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):

        prop = Prop.objects.get(pk=pk)
        prop.name = request.data["name"]
        prop.assigned = request.data["assigned"]
        school = School.objects.get(pk=request.data["school"])
        prop.school = school
        prop.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):

        prop = Prop.objects.get(pk=pk)
        prop.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreatePropSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prop
        fields = ['id', 'name', 'assigned', 'school', ]

class PropSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Prop
        fields = ('id', 'name', 'assigned', 'school', )