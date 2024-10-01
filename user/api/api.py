from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


'''
Vista basada en clase TokenObtainPairView para la autenticacion de usuarios y creacion de tokens con simplejwt

'''


class TokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'tokens': serializer.validated_data, 'message': 'inicio de sesion exitoso'})


'''
Vista basada en clase GenericAPIView para la validación del usuario y revocación del token de refresco.

'''


class LogoutView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')

        if refresh is None:
            return Response({'error': 'se requiere el token de actualización'}, status=HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({'message': 'revocacion exitosa'}, status=HTTP_200_OK)
        except TokenError:
            return Response({'error': 'token de actualización inválido'}, status=HTTP_400_BAD_REQUEST)
