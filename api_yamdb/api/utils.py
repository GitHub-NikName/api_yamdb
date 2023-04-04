from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken


def send_token(user):
    confirmation_code = default_token_generator.make_token(user)
    user.email_user('yamdb', f'confirmation_code: {confirmation_code}')


def get_jwt_for_user(user):
    token = AccessToken.for_user(user)
    return {'access': str(token)}
