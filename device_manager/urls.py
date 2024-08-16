from django.urls import path
from .views import PingMasterView, RegisterSlaveView, SensorStateView

urlpatterns = [
    path('ping', PingMasterView.as_view(), name='ping_master'),
    path('register', RegisterSlaveView.as_view(), name='register_slave'),
    path('set-state', SensorStateView.as_view(), name='sensor_state_changed'),
]