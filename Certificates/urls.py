from django.urls import path
from . import views

app_name = "certificates"

urlpatterns = [
    path('',views.menu,name='menu'),
    path('login',views.signin,name='login'),
    path("signup",views.signup,name="signup"),
    path('logout',views.logout_view,name='logout'),
    path("add" , views.add , name="add"),
    path('view',views.view,name='view'),
    path('<int:courseid>/details',views.details , name="details"),
    path('<int:courseid>/add',views.detailsAdd , name="detailsadd"),
    path('deleteMyCertificate',views.deleteMyCertificate , name="deleteMyCertificate"),
    path('deleteFromMenu',views.deleteMenuCertificate , name="deleteMenuCertificate"),
    path('updateMyCertificate' , views.updateMyCertificate , name="updateMyCertificate"),
    path('updateMenuCertificate' , views.updateMenuCertificate , name="updateMenuCertificate")
]
