from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ads import views

app_name = 'ads'

ads_patterns = [
    path('<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('create/', views.create_ad, name='create_ad'),
    path('<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
]

proposals_patterns = [
    path('', views.proposal_list, name='proposal_list'),
    path('create/<int:ad_id>', views.create_proposal, name='create_proposal'),
    path('<int:proposal_id>/status/<str:new_status>/', views.update_proposal_status, name='update_proposal_status'),
]

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('admin/', admin.site.urls),
    path('ads/', include(ads_patterns)),
    path('proposals/', include(proposals_patterns)),

    # Вход и выход
    path("accounts/register/", views.register, name="register"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='ad_list'), name='logout'),
]