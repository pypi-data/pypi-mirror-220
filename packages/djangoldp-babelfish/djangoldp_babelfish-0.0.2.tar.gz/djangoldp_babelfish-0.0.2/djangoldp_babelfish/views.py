from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests


@login_required
def call_babelfish(request):
    # Retrieve the user-specific access token
    token_url = settings.BABELFISH_BASE_URL + '/oauth/token'
    data = {
        'client_id': request.user.babelfishprofile.client_id,
        'client_secret': request.user.babelfishprofile.client_secret,
        'grant_type': 'client_credentials',
        'scope': 'write'
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')

    # Call the service registration endpoint with the proper info
    service_registration_url = settings.BABELFISH_BASE_URL + '/service/'  # Replace with the actual registration endpoint URL
    headers = {'Authorization': f'Bearer {access_token}'}
    json = {
        "interface": {
            "info": { "title": request.data.get('service_title') },
            "servers": [{"url": request.data.get('service_url')}],
            "party": request.data.get('service_party'),
            "paths": {
                "/api/validate": {
                    "post": {
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {} 
                                }
                            }
                        }
                    }
                }
            }
        },
        "data": {
            "description": request.data.get('service_description')
        },
        "governance": {
            "dpv:hasProcessing": ["dpv:Use"],
            "dpv:hasPurpose": "dpv:Purpose",
            "dpv:hasExpiryTime": "6 months"
        }
    }

    response = requests.post(registration_url, headers=headers, json=json)
    # Refresh the list of services to display the new one

    if response.status_code != 201:
        return JsonResponse({'message': 'Service registration failed'}, status=500)

    return JsonResponse({'message': 'Service properly registered'})