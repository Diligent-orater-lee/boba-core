import json
from Crypto.Cipher import AES
from django.conf import settings

class DecryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.should_process(request):
            if request.content_type == 'application/json' and request.body:
                try:
                    # Parse the JSON payload
                    data = json.loads(request.body)
                    
                    # Extract metadata
                    device_id = data.get('id')
                    encrypted_payload = data.get('encrypted_payload')
                    
                    if device_id and encrypted_payload:
                        # Fetch the device-specific key (you need to implement this)
                        key = self.get_device_key(device_id)
                        
                        # Decrypt the payload
                        cipher = AES.new(key, AES.MODE_ECB)
                        decrypted_payload = cipher.decrypt(bytes.fromhex(encrypted_payload))
                        
                        # Remove padding
                        decrypted_payload = decrypted_payload.rstrip(b'\0')
                        
                        # Parse the decrypted JSON
                        decrypted_data = json.loads(decrypted_payload)
                        
                        # Replace the request body with decrypted data
                        request._body = json.dumps(decrypted_data).encode('utf-8')
                
                except json.JSONDecodeError:
                    # Handle invalid JSON
                    pass
                except Exception as e:
                    # Handle other exceptions (e.g., decryption errors)
                    pass

        response = self.get_response(request)
        return response
    
    def should_process(self, request):
        return request.GET.get('X-Requires-Decryption') == 'true'

    def get_device_key(self, device_id):
        # Implement a method to fetch the device-specific key
        # This could involve querying a database or using a predefined mapping
        # For example:
        # return settings.DEVICE_KEYS.get(device_id)
        pass