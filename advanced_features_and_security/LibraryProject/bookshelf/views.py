from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Book  # Import your Book model
from .forms import ExampleForm
from django.http import HttpResponse


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
  # Logic for editing a book
  if request.method == "POST":
    book = Book.objects.get(id=book_id)
    book.title = request.POST.get("title")
    book.author = request.POST.get("author")
    book.published_date = request.POST.get("published_date")
    book.save()
    return redirect("book_list")
  else:
    book = Book.objects.get(id=book_id)
    return render(request, "bookshelf/edit_book.html", {"book": book})

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
  # Logic for displaying a list of books
  books = Book.objects.all()  # Fetch all books from the database
  return render(request, "bookshelf/book_list.html", {"books": books})

@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        published_date = request.POST.get("published_date")
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect("book_list")
    return render(request, "bookshelf/add_book.html")


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = ExampleForm(instance=book)
    return render(request, "bookshelf/edit_book.html", {"form": form})


@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = ExampleForm()
    return render(request, "bookshelf/add_book.html", {"form": form})


# Temporary view of the current user
def current_user_view(request):
  if request.user.is_authenticated:
    return HttpResponse(f"Logged in as: {request.user.username}")
  else:
    return HttpResponse("Not logged in")
