from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrCreateOnly, IsOwnerOrAdmin 


#View all users or create a new user

class CustomUserList(APIView):
    permission_classes = [IsAdminOrCreateOnly]

    def get(self, request):
        User = get_user_model()
        users = User.objects.all() 
        serializer = CustomUserSerializer(users, many=True)  
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
# View  for viewing and updating a specific user's details

class CustomUserDetail(APIView):

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        User = get_user_model()
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user) 
            return user
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user = self.get_object(pk)
        self.check_object_permissions(request, user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'username': user.username,  # Include username
            'first_name': user.first_name,  # Include first name (if applicable)
        })

        
