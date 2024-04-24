from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializer import *
from rest_framework import status, permissions, authentication
from rest_framework.response import Response
from .serializer import CustomUserSerializer, UserFileUploadSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .miscellaneous import GradientColorRenderer


class AdminCreateUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [GradientColorRenderer]

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserGetView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    renderer_classes = [GradientColorRenderer]

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

class UserFileUploadView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [GradientColorRenderer]

    def post(self, request, format=None):
        serializer = UserFileUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

class UserFilesView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [GradientColorRenderer]

    def get(self, request, format=None):
        if request.user.is_active:
            if request.user.is_admin or request.user.id == request.user.id:
                files = FileUpload.objects.filter(user=request.user)
                serializer = UserFileUploadSerializer(files, many=True)
                return Response(serializer.data)
            else:
                return Response(
                    {"error": "You do not have permission to access this view"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"error": "User is inactive or deleted"},
                status=status.HTTP_403_FORBIDDEN,
            )

class DeleteFileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [GradientColorRenderer]

    def post(self, request, pk, format=None):
        print("Request user:", request.user)
        print("Files in database:", FileUpload.objects.all())
        try:
            file = FileUpload.objects.get(pk=pk, user=request.user)
        except FileUpload.DoesNotExist:
            user_files = FileUpload.objects.filter(user=request.user)
            return Response(
                {"error": "File not found", "files": [{"pk": f.pk} for f in user_files]},
                status=status.HTTP_404_NOT_FOUND,
            )

        print("Deleting file:", file)
        file.delete()
        print("File deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteAllFilesView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        files = FileUpload.objects.filter(user=request.user)
        if files:
            files.delete()
            return Response(
                {"message": "All files deleted successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "No files found"}, status=status.HTTP_404_NOT_FOUND
            )
