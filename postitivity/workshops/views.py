from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Workshop, Notes, Location, Organisation
from .serializers import WorkshopSerializer, NoteSerializer, NoteDetailSerializer, WorkshopDetailSerializer, LocationSerializer, OrganisationSerializer, OrganisationDetailSerializer, LocationDetailSerializer
from .permissions import IsAdminOrReadOnly, IsAdminOwnerOrSuperuser, IsSuperUserOnly
from datetime import date,timedelta
from rest_framework import generics
from django.db.models import Q 


# Create your views here.

class RecentNotesList(generics.ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        today = date.today()
        thirty_days_ago = today + timedelta(days=-30)
        return Notes.objects.filter(
            date_created__date__gt=thirty_days_ago,
            date_created__date__lte=today,
            is_archived=0
        ).order_by('-date_created')

class ActiveWorkshopsList(generics.ListAPIView):
    serializer_class = WorkshopSerializer

    def get_queryset(self):
        thirty_days_ago = date.today() - timedelta(days=30)
        today = date.today()
        return Workshop.objects.filter(
            (Q(start_date__gte=thirty_days_ago) & Q(start_date__lte=today)) |
            Q(start_date=today),
            is_archived=0
        ).order_by('start_date')

class WorkshopList(APIView):
    permission_classes = [IsAdminOrReadOnly]

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

    permission_classes = [permissions.IsAuthenticated, IsAdminOwnerOrSuperuser]

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
            partial=True, #to allow partial updates
            context={'request': request} # Add request to context
        )
        if serializer.is_valid():
            serializer.save(created_by_user=workshop.created_by_user)
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class Notelist(APIView):
    permission_classes = [IsAdminOwnerOrSuperuser]

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
            serializer.save(
                user=request.user,
                added_by_user=request.user,
                workshop_id=request.data.get('workshop'),  # Add this line
                likes_count=0,
                is_archived=0
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class NoteDetail(APIView):
    permission_classes = [IsAdminOwnerOrSuperuser]

    def get_object(self, pk):
        try:
            note = Notes.objects.get(pk=pk)
            self.check_object_permissions(self.request, note)
            return note
        except Notes.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        note = self.get_object(pk=pk)
        serializer=NoteDetailSerializer(note) #this where I added DETAILserializer to get the notes
        return Response(serializer.data)
    
    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteDetailSerializer(
            instance=note,
            data=request.data,
            partial=True,
            context={'request': request}  # Add request context
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Create, View, Update location by ADMIN only
class LocationList (APIView):
    permission_classes = [IsSuperUserOnly]  
    
    def get(self, request):
        locations = Location.objects.filter(is_archived=False)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by_user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class LocationDetail(APIView):
    permission_classes = [IsSuperUserOnly] 

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationDetailSerializer(location)
        return Response(serializer.data)
    
    def put(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationDetailSerializer(
            instance=location,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
# Create, view, update organisations by ADMIN only

class OrganisationList (APIView):
    permission_classes = [IsSuperUserOnly]

    def get(self, request):
        organisations = Organisation.objects.filter(is_archived=False)
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by_user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class OrganisationDetail (APIView):
    permission_classes = [IsSuperUserOnly] 

    def get_object(self, pk):
        try:
            return Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        Organisation = self.get_object(pk)
        serializer = OrganisationDetailSerializer(Organisation)
        return Response(serializer.data)
    
    def put(self, request, pk):
        Organisation = self.get_object(pk)
        serializer = OrganisationDetailSerializer(
            instance=Organisation,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

