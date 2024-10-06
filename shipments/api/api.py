from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

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

        try:
            destino = Location.objects.get(code=destination)
        except Location.DoesNotExist:
            return Response({"error": "Destino no encontrado."}, status=HTTP_400_BAD_REQUEST)

        shipment = Shipment.objects.create(
            order_number=order_number,
            weight=0.0,
            price=0.0,
            status='Pendiente',
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


class ShippingCostView(APIView):
    def get(self, request, *args, **kwargs):
        destination_code = request.query_params.get('destino')

        if not destination_code:
            return Response({"error": "Se requiere código de destino"}, status=HTTP_400_BAD_REQUEST)

        try:
            location = Location.objects.get(code=destination_code)
        except Location.DoesNotExist:
            return Response({"consultaprecio": {
                            "courrier": '',
                            'destino': '',
                            'cobertura': False,
                            'costo': ''
                            }}, status=HTTP_404_NOT_FOUND)

        return Response({'consultaprecio': {
            "courrier": '',
            'destino': location.name,
            'cobertura': True,
            'costo': location.price
        }}, status=HTTP_200_OK)


class OrderStatusView(APIView):
    def get(self, request, *args, **kwargs):
        order_number = request.query_params.get('orden')
        store = request.query_params.get('tienda')

        if not all([order_number, store]):
            return Response({"error": "Se requieren los parámetros orden y tienda"}, status=HTTP_400_BAD_REQUEST)

        try:
            shipment = Shipment.objects.get(
                order_number=order_number, store=store)
        except Shipment.DoesNotExist:
            return Response({'orden': {
                'courrier': '',
                'orden': '',
                'status': '',
            }}, status=HTTP_404_NOT_FOUND)

        return Response({'orden': {
            'courrier': '',
            'orden': shipment.id,
            'status': shipment.status,
        }}, status=HTTP_200_OK)


class ShipmentListView (ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
