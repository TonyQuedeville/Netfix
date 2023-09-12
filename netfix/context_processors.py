from users.models import Company

def companies(request):
    # Récupérez la liste des entreprises et retournez-la dans le contexte.
    companies = Company.objects.all()
    return {'companies': companies}