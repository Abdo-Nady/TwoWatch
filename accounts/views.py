from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserProfile, Genre
from .serializers import UserProfileSerializer, GenreSerializer , ChangePasswordSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET: Display the Profile
    PUT/PATCH: Update the Profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_context(self):
        """add request for context for avatar_url"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ChangePasswordView(APIView):
    """
    change password
    POST: old_password, new_password1, new_password2
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadAvatarView(APIView):
    """
    upload avatar
    POST: avatar (file)
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        profile = request.user.profile
        avatar = request.FILES.get('avatar')

        if not avatar:
            return Response(
                {'error': 'No avatar file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # delete old avatar
        if profile.avatar:
            profile.avatar.delete(save=False)

        profile.avatar = avatar
        profile.save()

        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """delete avatar"""
        profile = request.user.profile

        if profile.avatar:
            profile.avatar.delete(save=False)
            profile.avatar = None
            profile.save()
            return Response(
                {'message': 'Avatar deleted successfully'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'No avatar to delete'},
            status=status.HTTP_400_BAD_REQUEST
        )


class GenreListView(generics.ListAPIView):
    """
    Display all available Genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UpdateFavoriteGenresView(APIView):
    """
    Update user's favorite Genres
    POST: Add genres
    DELETE: Remove genres
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Add genres to favorites"""
        genre_ids = request.data.get('genre_ids', [])

        if not genre_ids:
            return Response(
                {'error': 'genre_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile = request.user.profile
        genres = Genre.objects.filter(id__in=genre_ids)
        profile.favorite_genres.add(*genres)

        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def delete(self, request):
        """Remove genres from favorites"""
        genre_ids = request.data.get('genre_ids', [])

        if not genre_ids:
            return Response(
                {'error': 'genre_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile = request.user.profile
        genres = Genre.objects.filter(id__in=genre_ids)
        profile.favorite_genres.remove(*genres)

        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
