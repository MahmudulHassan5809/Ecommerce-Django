from .models import Category


def categories(request):
    categories = Category.objects.filter(active=True)
    return {'categories': categories}
