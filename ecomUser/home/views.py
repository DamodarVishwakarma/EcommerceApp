from django.shortcuts import render,HttpResponse
from store.models import Product

# Create your views here.
def home(request):
    products = Product.objects.filter(is_available=True)

    context_data = {
        "products" : products,
    }

    return render(request, "home/home.html", context_data)

def about(request):
    return HttpResponse('<h2>This is about page</h2>')
    