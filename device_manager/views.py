from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .mongo_models import Slave
from datetime import datetime
import json
import uuid

class PingMasterView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if data.get("reason"):
            return JsonResponse({"success": True}, status=200)
        return JsonResponse({}, status=404)

class RegisterSlaveView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        slave_data = json.loads(request.body)
        if 'id' not in slave_data:
            slave_data['id'] = str(uuid.uuid4())
        slave, created = Slave.objects.update_or_create(
            id=slave_data['id'],
            defaults={
                'ip': slave_data['ip'],
                'name': slave_data['name'],
                'description': slave_data['description'],
                'component_type': slave_data['componentType']
            }
        )
        print(f"{'Registered' if created else 'Updated'} slave {slave.id} with IP {slave.ip}. Details: {slave.name}, {slave.description}, {slave.component_type}")
        return JsonResponse({"message": "Registration successful"}, status=200)

class SensorStateView(View):
    current_state = "false"
    timer = datetime.now()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        prev_state = self.current_state
        self.current_state = data["sensorState"]
        print(f"Prev state: {prev_state}, Current state: {self.current_state}. Time taken = {datetime.now() - self.timer}")
        self.timer = datetime.now()
        return JsonResponse({"message": "State change recorded"}, status=200)