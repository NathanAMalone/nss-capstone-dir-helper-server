from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import School, Prop, Director

class PropView(ViewSet):

    def list(list,request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            props = Prop.objects.filter(school=director.school)
            serialized = PropSerializer(props, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):
        try:
            if request.auth.user.is_staff == True:
                director = Director.objects.get(user=request.auth.user)
                prop = Prop.objects.get(pk=pk)
                if prop.school == director.school:
                    serialized = PropSerializer(prop, context={'request': request})
                    return Response(serialized.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'ERROR: This prop is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
        except Prop.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    
    def create(self, request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            school = director.school
            serializer = CreatePropSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(school=school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You must be a director to create this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            prop = Prop.objects.get(pk=pk)
            if prop.school == director.school:
                prop.name = request.data["name"]
                prop.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This prop is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to update this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            prop = Prop.objects.get(pk=pk)
            if prop.school == director.school:
                prop.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This instrument is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to delete this data.'},status=status.HTTP_401_UNAUTHORIZED)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreatePropSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prop
        fields = ['id', 'name', 'assigned', ]

class PropSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Prop
        fields = ('id', 'name', 'assigned', 'school', )