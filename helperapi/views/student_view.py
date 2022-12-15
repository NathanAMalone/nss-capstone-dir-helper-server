from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helperapi.models import School, Student, Prop, Uniform, Instrument, Music, Director

class StudentView(ViewSet):

    def list(list,request):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            students = Student.objects.filter(school=director.school)
            serialized = StudentSerializer(students, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            student = Student.objects.get(user=request.auth.user)
            serialized = StudentSerializer(student, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):

        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            student = Student.objects.get(pk=pk)
            if student.school == director.school:
                serialized = StudentSerializer(student, context={'request': request})
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'ERROR: This student is not enrolled at your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to view this data.'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            student = Student.objects.get(pk=pk)
            if student.school == director.school:
                if request.data["prop"] == None:
                    student.prop =None
                else:
                    student.prop = Prop.objects.get(id=request.data["prop"])
                if request.data["uniform"] == None:
                    student.uniform = None
                else:
                    student.uniform = Uniform.objects.get(id=request.data["uniform"])
                if request.data["instrument"] == None:
                    student.instrument = None
                else:
                    student.instrument = Instrument.objects.get(id=request.data["instrument"])
                student.music_parts.set(request.data["music_parts"])
                student.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This instrument is not from your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to update this data.'},status=status.HTTP_401_UNAUTHORIZED)
            
    def destroy(self, request, pk):
        if request.auth.user.is_staff == True:
            director = Director.objects.get(user=request.auth.user)
            student = Student.objects.get(pk=pk)
            if student.school == director.school:
                student.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'ERROR: This student is not enrolled at your school.'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You must be a director to delete this data.'},status=status.HTTP_401_UNAUTHORIZED)

class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id', 'name', 'part', )

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', )

class PropSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prop
        fields = ('id', 'name', )

class UniformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uniform
        fields = ('id', 'uniform_number', )

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ('id', 'name', 'serial_number', )

class StudentSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(many=False)
    prop = PropSerializer(many=False)
    uniform = UniformSerializer(many=False)
    instrument = InstrumentSerializer(many=False)
    music_parts = MusicSerializer(many=True)

    class Meta:
        model = Student
        fields = ('id', 'uniform', 'full_name', 'prop', 'instrument', 'school', 'music_parts', )