from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from django.contrib.auth import views as auth_views
from app.views import ResetPasswordView
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home_view, name='home'),
    path('', company, name='company'),
    path('shop/<int:company_id>/', company_mobile, name='shop'),
    path('cart/', cart_page, name='cart'),
    # path('', search_mobile, name='searchmobile'),
    path('pluscart/', plus_cart, name='pluscart'),
    path('minuscart/', minus_cart, name='minuscart'),
    path('showcart/', showcart, name='showcart'),
    path('removecart/', remove_cart, name='removecart'),
    path('mobile/', mobile, name='mobile'),
    path('checkout/', checkout, name='checkout'),
    path('singleproduct/<int:mobile_id>/', single_product, name='singleproduct'),

    # authentication urls
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout', user_logout, name='logout'),
    # password reset urls
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),name='password_reset_complete'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)