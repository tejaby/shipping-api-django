from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ShipmentSerializer

from shipments.models import Shipment, Location


class CreateShipmentView(GenericAPIView):
    serializer_class = ShipmentSerializer

    def get(self, request, *args, **kwargs):
        order_number = request.query_params.get('orden')
        recipient = request.query_params.get('destinatario')
        destination = request.query_params.get('destino')
        address = request.query_params.get('direccion')
        store = request.query_params.get('tienda')

        if not all([order_number, recipient, destination, address, store]):
            return Response({"error": "Todos los parámetros son obligatorios."}, status=HTTP_400_BAD_REQUEST)

        destino = Location.objects.get(id=destination)
        if not destino:
            return Response({"error": "Destino no encontrado."}, status=HTTP_400_BAD_REQUEST)

        shipment = Shipment.objects.create(
            order_number=order_number,
            weight=0.0,
            price=0.0,
            status='Pending',
            recipient=recipient,
            department=destino,
            address=address,
            store=store
        )

        serializer = self.get_serializer(shipment)
        return Response(serializer.data, status=HTTP_201_CREATED)


class UpdateShipmentView(GenericAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, *args, **kwargs):
        status = request.data.get('status')

        if not status:
            return Response({"error": "El parámetro status es obligatorio."}, status=HTTP_400_BAD_REQUEST)

        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_200_OK)
