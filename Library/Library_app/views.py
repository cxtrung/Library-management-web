from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import User, Book
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import BookForm 
from . import models
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

#Shared views
def login_form(request):
	return render(request, 'Library_app/login.html')

def logoutView(request):
	logout(request)
	return redirect('home')

def loginView(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			if user.is_admin or user.is_superuser:
				return redirect('dashboard')
			else:
				return redirect('reader')
		else:
			messages.info(request, "Invalid username or password")
			return redirect('home')
		

def register_form(request):
	return render(request, 'Library_app/register.html')


def registerView(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password = make_password(password)

		a = User(username=username, email=email, password=password)
		a.save()
		messages.success(request, 'Account was created successfully')
		return redirect('home')
	else:
		messages.error(request, 'Registration fail, try again later')
		return redirect('regform')


#Reader views
@login_required
def reader(request):
	return render(request, 'reader/home.html')







#Admin views
def dashboard(request):
	return render(request, 'dashboard/home.html')

def dashboard(request):
	book = Book.objects.all().count()
	user = User.objects.all().count()

	context = {'book':book, 'user':user}

	return render(request, 'dashboard/home.html', context)

@login_required
def aabook_form(request):
	return render(request, 'dashboard/add_book.html')

@login_required
def aabook(request):
	if request.method == 'POST':
		title = request.POST['title']
		author = request.POST['author']
		year = request.POST['year']
		publisher = request.POST['publisher']
		desc = request.POST['desc']
		cover = request.FILES['cover']
		pdf = request.FILES['pdf']
		current_user = request.user
		user_id = current_user.id
		username = current_user.username

		a = Book(title=title, author=author, year=year, publisher=publisher, 
			desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
		a.save()
		messages.success(request, 'Book was uploaded successfully')
		return redirect('albook')
	else:
		messages.error(request, 'Book was not uploaded successfully')
		return redirect('aabook_form')


class ABookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/book_list.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')

class AManageBook(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')


class ADeleteBook(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete2.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was delete successfully'


class ADeleteBookk(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete.html'
	success_url = reverse_lazy('dashboard')
	success_message = 'Data was delete successfully'


class AViewBook(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'dashboard/book_detail.html'

class AEditView(LoginRequiredMixin,UpdateView):
	model = Book
	form_class = BookForm
	template_name = 'dashboard/edit_book.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was updated successfully'
