from rest_framework.exceptions import AuthenticationFailed
from logging import raiseExceptions
import jwt


def isAuthen(token):
  if not token:
      raise AuthenticationFailed('Unauthenticated!')
  try:
      payload = jwt.decode(token, 'secret', algorithm=['HS256'])
      return payload
  except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated!')