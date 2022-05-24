from rest_framework.exceptions import AuthenticationFailed
from logging import raiseExceptions
import jwt


def isAuthen(token):
    return jwt.decode(token, 'secret', algorithm=['HS256']) 
#   if not token:
#       raise AuthenticationFailed('Unauthenticated!')
#   try:
#       print(token)
#       payload = jwt.decode(token, 'secret', algorithm=['HS256'])
#       print(payload)
#       return payload
#   except jwt.ExpiredSignatureError:
#       raise AuthenticationFailed('Unauthenticated!')