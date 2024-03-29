from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

# Shared URL's
 path('', views.login_form, name='home'),
 path('login/', views.loginView, name='login'),
 path('logout/', views.logoutView, name='logout'),
 path('regform/', views.register_form, name='regform'),
 path('register/', views.registerView, name='register'),


 # Reader URL's
path('reader/', views.UBookListView.as_view(), name='reader'),
path('request_form/', views.request_form, name='request_form'),
path('rent_request/', views.rent_request, name='rent_request'),
path('feedback_form/', views.feedback_form, name='feedback_form'),
path('send_feedback/', views.send_feedback, name='send_feedback'),
path('about/', views.about, name='about'),
path('usearch/', views.usearch, name='usearch'),


 # Admin URL's
 path('dashboard/', views.dashboard, name='dashboard'),
 path('aabook_form/', views.aabook_form, name='aabook_form'),
 path('aabook/', views.aabook, name='aabook'),
 path('albook/', views.ABookListView.as_view(), name='albook'),
 path('ambook/', views.AManageBook.as_view(), name='ambook'),
 path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),
 path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
 path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
 path('adbookk/<int:pk>', views.ADeleteBookk.as_view(), name='adbookk'),
 path('asearch/', views.asearch, name='asearch'),
 path('create_user_form/', views.create_user_form, name='create_user_form'),
 path('aluser/', views.ListUserView.as_view(), name='aluser'),
 path('create_user/', views.create_user, name='create_user'),
 path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
 path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
 path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
 path('arrequest/', views.ARentRequest.as_view(), name='arrequest'),
 path('afeedback/', views.AFeedback.as_view(), name='afeedback'),

]