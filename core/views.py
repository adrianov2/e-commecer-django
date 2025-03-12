from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Product
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm
from django.conf import settings
import mercadopago
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Product
from .serializers import ProdutoSerializer


def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def product_list(request):
    categories = {}
    products = Product.objects.all()
    for product in products:
        if product.category not in categories:
            categories[product.category] = []
        categories[product.category].append(product)
    return render(request, "product_list.html", {"categories": categories})

def product(request):
    return render(request, 'product.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart

    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def minha_conta(request):
    return render(request, 'minha_conta.html')

def editar_perfil(request):
    return render(request, 'editar_perfil.html')

def historico(request):
    return render(request, 'historico.html')

def logout_view(request):
    return render(request, 'logout.html')

def login_view(request):
    if request.method == "POST":
        next_url = request.POST.get('next', '/')
        return redirect(next_url)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def acessorios(request):
    produtos = Product.objects.filter(category="acessorios")  
    return render(request, 'acessorios.html', {'products': produtos})

def roupas(request):
    return render(request, 'roupas.html')

def celulares(request):
    return render(request, 'celulares.html')

def software(request):
    return render(request, 'software.html')

class CustomLoginView(LoginView):
    def get_redirect_url(self):
        return self.request.GET.get('next', '/')

def cadastro_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('index') 
        else:
            return render(request, 'cadastro.html', {'form': form})
    
    form = UserRegistrationForm()
    return render(request, 'cadastro.html', {'form': form})


def update_cart(request, product_id):
    cart = request.session.get('cart', {})  
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1 

    request.session['cart'] = cart  
    messages.success(request, "Carrinho atualizado com sucesso.")
    return redirect('cart')  

def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and quantity.isdigit():
            quantity = int(quantity)
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.quantity = quantity
            cart_item.save()
    return redirect('cart')


def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()  
    except CartItem.DoesNotExist:
        pass 
    return redirect('cart')  

def payment_view(request):
    return render(request, 'payment.html')
  
 
mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

def pagamento(request):
    if request.method == "POST":
        total_price =  871.60

        
        preference_data = {
            "items": [
                {
                    "title": "Produtos",
                    "quantity": 1,
                    "unit_price": float(total_price)
                }
            ],
            "back_urls": {
                "success": "http://www.seusite.com/sucesso",
                "failure": "http://www.seusite.com/falha",
                "pending": "http://www.seusite.com/pendente"
            },
            "auto_return": "approved"
        }

        preference = mp.preference().create(preference_data)  

        if "response" in preference and "init_point" in preference["response"]:
            return redirect(preference["response"]["init_point"])

    return redirect('/')

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProdutoSerializer