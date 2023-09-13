from django.shortcuts import redirect
from django.contrib.sessions.middleware import SessionMiddleware

class SessionTimeoutMiddleware(SessionMiddleware):
    def process_request(self, request):
        # Appel de la méthode parent pour gérer la session
        super().process_request(request)

        # Vérifie si la session a expiré
        if request.session.get_expiry_age() <= 0:
            # La session a expiré, redirigez l'utilisateur vers la page login
            return redirect('login') 
        
