from django.urls import path


from shipments.api.api import CreateShipmentView, UpdateShipmentView, ShippingCostView, OrderStatusView

urlpatterns = [
    path('envio', CreateShipmentView.as_view(), name='create_shipment'),
    path('envio/<int:pk>', UpdateShipmentView.as_view(), name='update_shipment'),
    path('consulta', ShippingCostView.as_view(), name='shipping_cost'),
    path('status', OrderStatusView.as_view(), name='order-status')
]
