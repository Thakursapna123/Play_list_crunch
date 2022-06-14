"""playlistcrunch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    # With Out Login Screen
    path('', home,name='home' ),
    path('signup/', signup,name='signup' ),
    path('sigin/', sigin,name='sigin' ),
    path('term_and_condition/', term_and_condition,name='term_and_condition' ),
    path('privacy_policy/', privacy_policy,name='privacy_policy' ),
    path('forgot_password/', forgot_password,name='forgot_password' ),
    path('verify_email/', verify_email,name='verify_email' ),
    path('verify_account/<str:token>/<str:email>', verify_account, name='verify_account'),

    path('verify_user_to_reset_password/<str:token>/<str:email>', verify_user_to_reset_password, name='verify_user_to_reset_password'),
    path('auth_change_password/<str:validate>', auth_change_password, name='auth_change_password'),
    

    # With Login Screen
    path('search/', search,name='search' ),
    path('user_profile/', user_profile,name='user_profile' ),
    path('payment/', payment,name='payment' ),
    path('search/search_results',search_results,name='search_results'),
    path('resetpassword/',resetpassword,name='resetpassword'),
    path('logout_home',logout_home,name='logout_home'),
    path('thankyou/',thankyou_page,name='thankyou_page'),
    path('user_profile/cancel_subscription/<str:ref>',cancel_subscription,name='cancel_subscription'),


    # Admin Theme Login
    path('admin_home', admin_home, name='admin_home'),
    path('admin_edit_user/<int:id>', admin_edit_user, name='admin_edit_user'),
    path('admin_delete_user/<int:id>', admin_delete_user, name='admin_delete_user'),
    path('admin_view_user/<int:id>', admin_view_user, name='admin_view_user'),
    path('admin-cms', admin_cms, name='admin-cms'),
    path('people-comments', people_comments, name='people-comments'),
    
    path('admin_edit_banner/<int:id>', admin_edit_banner, name='admin_edit_banner'),
    path('add_people_comments', add_people_comments, name='add_people_comments'),
    path('admin_people_edit/<int:id>', admin_people_edit, name='admin_people_edit'),
    path('admin_people_delete/<int:id>', admin_people_delete, name='admin_people_delete'),
]
