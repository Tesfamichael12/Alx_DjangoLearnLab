from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

# Create your views here.

def list_books(request):
  books = Book.objects.all()
  return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
  model = Library
  template_name = 'relationship_app/library_detail.html'
  context_object_name = 'library'

class CustomLoginView(LoginView):
  template_name = 'relationship_app/login.html'
  redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
  template_name = 'relationship_app/logout.html'

class RegisterView(CreateView):
  form_class = UserCreationForm
  template_name = 'relationship_app/register.html'
  success_url = reverse_lazy('login')

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('list_books')
    else:
      form = UserCreationForm()
  return render(request, 'relationship_app/register.html', {'form': form})

def is_admin(user):
  return user.userprofile.role == "Admin"

def is_librarian(user):
  return user.userprofile.role == "Librarian"

def is_member(user):
  return user.userprofile.role == "Member"

@user_passes_test(is_admin)
def admin_view(request):
  return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian)
def librarian_view(request):
  return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# Add book view with permission check
@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book_view(request):
  if request.method == "POST":
    form = BookForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("book_list")  # Replace 'book_list' with your book list URL
  else:
    form = BookForm()
  return render(request, "relationship_app/add_book.html", {"form": form})


# Edit book view with permission check
@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book_view(request, book_id):
  book = get_object_or_404(Book, id=book_id)
  if request.method == "POST":
    form = BookForm(request.POST, instance=book)
    if form.is_valid():
      form.save()
      return redirect("book_list")
  else:
      form = BookForm(instance=book)
  return render(request, "relationship_app/edit_book.html", {"form": form})


# Delete book view with permission check
@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book_view(request, book_id):
  book = get_object_or_404(Book, id=book_id)
  if request.method == "POST":
    book.delete()
    return redirect("book_list")
  return render(request, "relationship_app/delete_book.html", {"book": book})