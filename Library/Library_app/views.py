from datetime import date
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import Feedback, RentRequest, User, Book
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import BookForm, UserForm 
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
@login_required
def request_form(request):
    return render(request, 'reader/rent_request.html')
@login_required
def feedback_form(request):
    return render(request, 'reader/send_feedback.html')

@login_required
def about(request):
    return render(request, 'reader/about.html')

@login_required
def usearch(request):
    #GET - fetch data from the database
    query = request.GET['query']
    print(type(query))

    data = query
    print(len(data))
    if (len(data) == 0):
        return redirect('reader')
    else:
        a = data

        # searching for data
        qs5 =models.Book.objects.filter(id__iexact=a).distinct()
        qs6 =models.Book.objects.filter(id__exact=a).distinct()
        qs7 =models.Book.objects.all().filter(id__contains=a)
        qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs9 =models.Book.objects.filter(id__startswith=a).distinct()
        qs10 =models.Book.objects.filter(id__endswith=a).distinct()
        qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
        qs12 =models.Book.objects.all().filter(id__icontains=a)
        qs13 =models.Book.objects.filter(id__iendswith=a).distinct()

        files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        # word variable will be shown in html when user click on search button
        word="Searched Result :"
        print("Result")

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request,'reader/result.html',{'files':files,'word':word})

@login_required
def rent_request(request):
    if request.method == 'POST':
        book_id = request.POST['rent_request']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        user_request = username + " wants the book with the id " + book_id + " to be rented"

        a = RentRequest(rent_request=user_request)
        a.save()
        messages.success(request, 'Request was sent')
        return redirect('request_form')
    else:
        messages.error(request, 'Request was not sent')
        return redirect('request_form')

@login_required
def send_feedback(request):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        feedback = username + " " + " says " + " " + feedback

        a = Feedback(feedback=feedback)
        a.save()
        messages.success(request, 'Feedback was sent')
        return redirect('feedback_form')
    else:
        messages.error(request, 'Feedback was not sent')
        return redirect('feedback_form')

class UBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'reader/book_list.html'
    context_object_name = 'books'
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.order_by('-id')


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

@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))


    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashboard')
    else:
        a = data

        # Searching for It
        qs5 =models.Book.objects.filter(id__iexact=a).distinct()
        qs6 =models.Book.objects.filter(id__exact=a).distinct()
        qs7 =models.Book.objects.all().filter(id__contains=a)
        qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs9 =models.Book.objects.filter(id__startswith=a).distinct()
        qs10 =models.Book.objects.filter(id__endswith=a).distinct()
        qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
        qs12 =models.Book.objects.all().filter(id__icontains=a)
        qs13 =models.Book.objects.filter(id__iendswith=a).distinct()

        files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        # word variable will be shown in html when user click on search button
        word="Searched Result :"
        print("Result")

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request,'dashboard/result.html',{'files':files,'word':word})
        return render(request,'dashboard/result.html',{'files':files,'word':word})

def create_user_form(request):
    choice = ['1', '0', 'Reader', 'Admin']
    choice = {'choice': choice}

    return render(request, 'dashboard/add_user.html', choice)

class ListUserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')

class ALViewUser(DetailView):
    model = User
    template_name = 'dashboard/user_detail.html'

class AEditUser(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"

class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"

def create_user(request):
    choice = ['1', '0', 'Reader', 'Admin']
    choice = {'choice': choice}
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        userType=request.POST['userType']
        email=request.POST['email']
        password=request.POST['password']
        password = make_password(password)
        print("User Type")
        print(userType)
        if userType == "Reader":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_reader=True)
            a.save()
            messages.success(request, 'Member was created successfully!')
            return redirect('aluser')
        elif userType == "Admin":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
            a.save()
            messages.success(request, 'Member was created successfully!')
            return redirect('aluser')
        else:
            messages.success('Member was not created')
            return redirect('create_user_form')
    else:
        return redirect('create_user_form')
	
class ARentRequest(LoginRequiredMixin,ListView):
	model = RentRequest
	template_name = 'dashboard/rent_request.html'
	context_object_name = 'feedbacks'
	paginate_by = 3

	def get_queryset(self):
		return RentRequest.objects.order_by('-id')

class AFeedback(LoginRequiredMixin,ListView):
	model = Feedback
	template_name = 'dashboard/feedback.html'
	context_object_name = 'feedbacks'
	paginate_by = 3

	def get_queryset(self):
		return Feedback.objects.order_by('-id')