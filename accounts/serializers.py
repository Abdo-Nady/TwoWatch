from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User, UserProfile, Genre


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genres"""

    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User Profile"""
    favorite_genres = GenreSerializer(many=True, read_only=True)
    favorite_genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        source='favorite_genres',
        required=False
    )
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'bio',
            'avatar',
            'avatar_url',
            'favorite_genres',
            'favorite_genre_ids',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_avatar_url(self, obj):
        """ avatar url"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
Custom serializer for User with Profile
     /api/auth/me/
    """
    profile = UserProfileSerializer(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'username',
            'profile',
        ]


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom Registration Serializer
    Username is auto-generated from email
    """
    username = None  # Hide username from registration form
    
    def save(self, request):
        email = self.validated_data.get('email')
        # Generate username from email 
        username = email.split('@')[0]
        
        # Clean username: remove special characters
        import re
        username = re.sub(r'[^a-zA-Z0-9_]', '', username)
        if not username:
            username = 'user'
        
        # Truncate if too long (max 150 chars)
        if len(username) > 150:
            username = username[:150]
        
        # Set username before calling super().save()
        self.validated_data['username'] = username

        user = super().save(request)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """Validate old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate(self, data):
        """Validate new password match"""
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({
                'new_password2': "The two password fields didn't match."
            })

        # Validate password strength
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(data['new_password1'], self.context['request'].user)
        except Exception as e:
            raise serializers.ValidationError({'new_password1': list(e.messages)})

        return data

    def save(self):
        """Save new password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])
        user.save()
        return user
