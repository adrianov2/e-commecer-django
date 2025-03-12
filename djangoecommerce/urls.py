from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.views import (
    payment_view, 
    pagamento, 
    product_detail, 
    add_to_cart, 
    ProdutoViewSet
)
from rest_framework.routers import DefaultRouter

# Roteador para a API
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.Product, name='product'),
    path('contato/', views.contact, name='contact'),
    path('produto/', views.product, name='product'),
    path('produtos/', views.product_list, name='product_list'),
    path('admin/', admin.site.urls),
    path('acessorios/', views.acessorios, name='acessorios'),
    path('roupas/', views.roupas, name='roupas'),
    path('celulares/', views.celulares, name='celulares'),
    path('software/', views.software, name='software'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('carrinho/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('historico/', views.historico, name='historico'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='user_register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),
    path('payment/', payment_view, name='payment'),
    path('pagamento/', pagamento, name='pagamento'),

    # API
    path('api/', include(router.urls)),
]

# Configuração para servir arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
