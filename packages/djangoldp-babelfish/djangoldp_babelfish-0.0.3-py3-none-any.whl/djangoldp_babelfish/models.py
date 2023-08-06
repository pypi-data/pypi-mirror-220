from django.db import models
from djangoldp.models import Model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
import requests

class BabelfishProfile(Model):
    """ Add a field which associate this model to the user model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='babelfish_profile')

    babelfish_user_id = models.CharField(max_length=255, blank=True)
    organisation_id = models.CharField(max_length=255, blank=True, default="811")
    client_id = models.CharField(max_length=255, blank=True)
    client_secret = models.CharField(max_length=255, blank=True)

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ["inherit"]
        owner_perms = ["view", "change"]
        auto_author = "user"
        serializer_fields = ['@id']

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def register_user_with_sib(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'babelfish_profile'):
        # Retrieve the access token using server-side settings
        token_url = settings.BABELFISH_BASE_URL + '/oauth/token'  # Replace with the actual token API endpoint URL
        data = {
            'client_id': settings.BABELFISH_CLIENT_ID,
            'client_secret': settings.BABELFISH_CLIENT_SECRET,
            'grant_type': 'client_credentials',
            'scope': 'write'
        }
        response = requests.post(token_url, data=data)
        access_token = response.json().get('access_token')

        # Build a request to create the user in BabelFish and retrieve credentials
        create_user_url = settings.BABELFISH_BASE_URL + '/user/'  # Replace with the actual create user endpoint URL
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        data = {
            'name': instance.name(),
            'email': instance.email,
            'organization-id': settings.BABELFISH_ORGANISATION_ID,
        }

        try:
            response = requests.post(create_user_url, headers=headers, data=json.dumps(data))
            babelfish_profile_info = response.json()
        except Exception as e:
            print(e)
            return

        # Save the BabelFish user credentials to the user's profile
        profile = BabelfishProfile(user=instance)
        profile.babelfish_user_id = babelfish_profile_info.get('user-id')
        profile.organisation_id = babelfish_profile_info.get('organization-id')
        profile.client_id = babelfish_profile_info.get('oauth').get('client-id')
        profile.client_secret = babelfish_profile_info.get('oauth').get('client-secret')
        profile.save()