from django.urls import path


from shipments.api.api import CreateShipmentView, UpdateShipmentView

urlpatterns = [
    path('shipments/', CreateShipmentView.as_view(), name='create_shipment'),
    path('shipments/<int:pk>/', UpdateShipmentView.as_view(), name='update_shipment'),
]
