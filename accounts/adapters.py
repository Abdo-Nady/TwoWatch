from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social account login
    Handles user creation from social providers (Google, etc.)
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Called just before a social account is logged in.
        """
        # If the social account is already connected to a user, we're done
        if sociallogin.is_existing:
            return
        
        # Check if a user with this email already exists
        if sociallogin.email_addresses:
            email = sociallogin.email_addresses[0].email
            User = get_user_model()  # Get User model inside the method
            try:
                user = User.objects.get(email=email)
                # If user exists, connect the social account to it
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
    
    def populate_user(self, request, sociallogin, data):
        """
        Populate user fields from social account data
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Generate username from email if not provided
        if not user.username and user.email:
            username = user.email.split('@')[0]
            # Clean username
            import re
            username = re.sub(r'[^a-zA-Z0-9_]', '', username)
            if not username:
                username = 'user'
            # Truncate if too long
            if len(username) > 150:
                username = username[:150]
            user.username = username
        
        return user


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for regular account operations
    """
    pass

