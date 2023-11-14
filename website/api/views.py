from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from accounts.managers import UserManager

@csrf_exempt
def obtainAuthToken(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            purpose = request.POST['purpose']
            user = None
            if purpose == "Login":
                user = authenticate(request, email=email, password=password)
            elif purpose == "Signup":
                user = UserManager.create_user(email, password)
            if user is not None:
                login(request, user)
                # Generate or retrieve an authentication token
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': 'Login successful', 'token': token.key})
            else:
                return JsonResponse({f'message': '{purpose} failed'}, status=400) 
        except Exception as e:
            return JsonResponse({f'message': 'Internal Server Error'}, status=500)
    
    if request.method == 'GET':
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)
    