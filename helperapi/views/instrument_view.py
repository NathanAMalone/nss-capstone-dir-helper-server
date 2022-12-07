from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import Instrument, School

class InstrumentView(ViewSet):

    def list(list,request):

        instruments = Instrument.objects.all()
        serialized = InstrumentSerializer(instruments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):

        instrument = Instrument.objects.get(pk=pk)
        serialized = InstrumentSerializer(instrument, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):

        serializer = CreateInstrumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):

        instrument = Instrument.objects.get(pk=pk)
        instrument.name = request.data["name"]
        instrument.type = request.data["type"]
        instrument.serial_number = request.data["serial_number"]
        instrument.out_for_repair = request.data["out_for_repair"]
        instrument.school_owned = request.data["school_owned"]
        instrument.assigned = request.data["assigned"]
        school = School.objects.get(pk=request.data["school"])
        instrument.school = school
        instrument.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):

        instrument = Instrument.objects.get(pk=pk)
        instrument.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class CreateInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ['id', 'name', 'type', 'serial_number', 'out_for_repair', 'school_owned', 'assigned', 'school', ]

class InstrumentSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'type', 'serial_number', 'out_for_repair', 'school_owned', 'assigned', 'school', )