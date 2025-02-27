from django.shortcuts import redirect
from django.urls import reverse

class DeliveryLoginRequiredMiddleware:
    """ यह Middleware डिलीवरी पर्सन को सही Login Page पर Redirect करेगा """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/delivery/') and not request.user.is_authenticated:
            return redirect(reverse('delivery:login'))  # डिलीवरी पर्सन का लॉगिन पेज

        response = self.get_response(request)
        return response
