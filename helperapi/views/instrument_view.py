from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import Instrument, School, Director

class InstrumentView(ViewSet):
    
    def list(list,request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            instruments = Instrument.objects.filter(school=director.school)
            serialized = InstrumentSerializer(instruments, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            instrument = Instrument.objects.get(pk=pk)
            if instrument.school == director.school:
                serialized = InstrumentSerializer(instrument, context={'request': request})
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'ERROR: This instrument is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            school = director.school
            serializer = CreateInstrumentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(school=school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You must be a director to create this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            instrument = Instrument.objects.get(pk=pk)
            if instrument.school == director.school:
                instrument.name = request.data["name"]
                instrument.type = request.data["type"]
                instrument.serial_number = request.data["serial_number"]
                instrument.out_for_repair = request.data["out_for_repair"]
                instrument.school_owned = request.data["school_owned"]
                instrument.assigned = request.data["assigned"]
                instrument.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This instrument is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to update this data.'},status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            instrument = Instrument.objects.get(pk=pk)
            if instrument.school == director.school:
                instrument.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This instrument is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to delete this data.'},status=status.HTTP_401_UNAUTHORIZED)


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreateInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ['id', 'name', 'type', 'serial_number', 'out_for_repair', 'school_owned', 'assigned', ]

class InstrumentSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'type', 'serial_number', 'out_for_repair', 'school_owned', 'assigned', 'school', )