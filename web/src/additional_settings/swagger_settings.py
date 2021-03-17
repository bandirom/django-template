
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'description': 'Value example: Bearer ******************',
            'in': 'header'
        },
        'Api-Key': {
            'type': 'apiKey',
            'name': 'Authorization',
            'description': 'Value example: <API_KEY_HEADER> <API_KEY>',
            'in': 'header'
        },
        'Language': {
            'type': 'apiKey',
            'name': 'Accept-Language',
            'in': 'header',
            'description': 'Your language code. Example: ua,ru,en',
            'default': 'en'
        },
    },
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': False,
    'LOGOUT_URL': 'rest_framework:logout',
}
