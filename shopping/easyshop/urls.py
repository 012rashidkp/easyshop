from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . views import RegisterView,LoginAPIView







urlpatterns = [
    # Leave as empty string for base url
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('upload/',views.upload,name="upload"),
    path('maintain/',views.maintain,name="maintain"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('show_prod/<str:pk>/', views.show, name="show"),
    path('logoutuser/',views.logoutpage,name="logoutpage"),
    path('api/products/',views.show_list),
    path('api/register/', RegisterView.as_view(),name="registerapi"),
    path('api/login/', LoginAPIView.as_view(), name="loginapi"),
    path('addtocart/<str:pk>/',views.addtocart, name="addtocart"),
    path('dialog/',views.dialog, name="dialog"),
    path('removecart/<str:pk>/',views.cart_remove,name="removeitem"),
    path('removecartdialog/',views.cart_remove_alert,name="cartremovedialog"),
    path('addqty/<str:pk>/',views.cart_add_q,name="cart_add_q"),
    path('alert/',views.alert,name="alert"),
    path('placeorder',views.placeorder,name="placeorder")
    # path('dashboard/',views.dashboard,name="dashboard"),
    # path('adminlogin/',views.Admin_login,name="adminlogin"),
    # path('adminlogout/',views.logoutadmin,name="adminlogout")
    #path('placeorder/',views.placeorder,name="placeorder"),
        
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)