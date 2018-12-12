from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('',views.index,name='index'),
	path('cadastro/', views.cadastro, name='cadastro'),
	path('login/',views.do_login, name='login'),
 	path('logout/',views.do_logout, name='logout'),
 	path('perfil/',views.get_perfil, name='perfil'),
 	path('add/',views.add_car, name='add'),
 	path('detalhes/<int:carro_id>', views.detalhes, name='detalhes'),
 	path('editar/<int:carro_id>',views.editar, name='editar'),
 	path('apagar/<int:carro_id>',views.apagar, name='apagar'),
 	path('comprar/<int:carro_id>', views.comprar, name='comprar'),
 	path('search/',views.search,name='search'),
 	path('venda/<int:carro_id>', views.venda, name='venda'),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)