from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Workshop, Notes
from .serializers import WorkshopSerializer, NoteSerializer, WorkshopDetailSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class WorkshopList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        workshops = Workshop.objects.all()
        serializer = WorkshopSerializer(workshops, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.copy()
        serializer = WorkshopSerializer(data=data)  # Use the modified copy
        if serializer.is_valid():
            serializer.save(created_by_user=request.user)
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class WorkshopDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]


    def get_object(self, pk):
        try:
            workshop = Workshop.objects.get(pk=pk)
            self.check_object_permissions(self.request, workshop)
            return workshop
        except Workshop.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        workshop = self.get_object(pk=pk)
        serializer=WorkshopDetailSerializer(workshop) #this where I added DETAILserializer to get the notes
        return Response(serializer.data)
    
    def put(self,request, pk):
        workshop = self.get_object(pk)
        serializer = WorkshopDetailSerializer(
            instance=workshop,
            data=request.data,
            partial=True #to allow partial updates
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class Notelist(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        notes = Notes.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("Request data:", request.data)
        serializer = NoteSerializer(data=request.data)
        print("Is valid:", serializer.is_valid())
        if not serializer.is_valid():
            print("Errors:", serializer.errors)
        if serializer.is_valid():
            note = serializer.save(
                user=request.user,
                added_by_user=request.user,
                workshop_id=request.data.get('workshop')  # Add this line
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    