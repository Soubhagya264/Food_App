from django.urls import path
from rest_proj_app  import views
from django.conf.urls import url


urlpatterns = [
     path('',views.main_home,name='main_home'),
     path('menu',views.menu,name='menu'),
     url(r'^chatbot/$',views.chatbot,name='chatbot')
     # path('itemhandle',views.itemhandle,name='itemhandle')

]
