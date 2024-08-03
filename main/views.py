from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from .models import Book, Author, Issue, Fine
from main2.models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
import datetime
from .utils import calcFine, getmybooks
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from LMS import settings

# Book
# views.py
from django.shortcuts import render
from .models import Book, Author
from main2.models import Student
from .utils import getmybooks

from django.shortcuts import render
from .models import Book, Author
from main2.models import Student
from .utils import getmybooks

def allbooks(request):
    requestedbooks, issuedbooks = getmybooks(request.user)
    category = request.GET.get('category')  

    if category and category != 'all':
        allbooks = Book.objects.filter(category=category)
    else:
        allbooks = Book.objects.all()  
    
    categories = Book.objects.values_list('category', flat=True).distinct() 
    
    return render(request, 'home.html', {
        'books': allbooks,
        'issuedbooks': issuedbooks,
        'requestedbooks': requestedbooks,
        'categories': categories,  
        'selected_category': category  
    })




def sort(request):
    sort_type = request.GET.get('sort_type')
    sort_by = request.GET.get('sort')
    requestedbooks, issuedbooks = getmybooks(request.user)
    if 'author' in sort_type:
        author_results = Author.objects.filter(name__startswith=sort_by)
        return render(request, 'home.html', {
            'author_results': author_results,
            'issuedbooks': issuedbooks,
            'requestedbooks': requestedbooks,
            'selected': 'author'
        })
    else:
        books_results = Book.objects.filter(name__startswith=sort_by)
        return render(request, 'home.html', {
            'books_results': books_results,
            'issuedbooks': issuedbooks,
            'requestedbooks': requestedbooks,
            'selected': 'book'
        })

def search(request):
    search_query = request.GET.get('search-query')
    search_by_author = request.GET.get('author')
    requestedbooks, issuedbooks = getmybooks(request.user)
    if search_by_author is not None:
        author_results = Author.objects.filter(name__icontains=search_query)
        return render(request, 'home.html', {
            'author_results': author_results,
            'issuedbooks': issuedbooks,
            'requestedbooks': requestedbooks
        })
    else:
        books_results = Book.objects.filter(Q(name__icontains=search_query) | Q(category__icontains=search_query))
        return render(request, 'home.html', {
            'books_results': books_results,
            'issuedbooks': issuedbooks,
            'requestedbooks': requestedbooks
        })

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: u.is_superuser,login_url='/student/login/')
def addbook(request):
    authors = Author.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        category = request.POST['category']
        author = Author.objects.get(id=request.POST['author'])
        image = request.FILES['book-image']
        total_copies = int(request.POST.get('total_copies', 1))  
        if author:
            newbook, created = Book.objects.get_or_create(
                name=name,
                image=image,
                category=category,
                author=author,
                defaults={'total_copies': total_copies, 'available_copies': total_copies}
            )
            if not created:
                
                newbook.total_copies = total_copies
                newbook.available_copies = total_copies
                newbook.save()
            messages.success(request, 'Book - {} Added successfully '.format(newbook.name))
            return redirect('addbook')
        else:
            messages.error(request, 'Author not found!')
            return render(request, 'library/addbook.html', {'authors': authors})
    else:
        return render(request, 'library/addbook.html', {'authors': authors})

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: u.is_superuser,login_url='/student/login/')
def deletebook(request, bookID):
    book = Book.objects.get(id=bookID)
    messages.success(request, 'Book - {} Deleted successfully '.format(book.name))
    book.delete()
    return redirect('/')

# ISSUES
@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser, login_url='/student/login/')
def issuerequest(request, bookID):
    book = get_object_or_404(Book, id=bookID)
    student = Student.objects.filter(student_id=request.user).first()

    if student:
        if book.available_copies > 0:
            issue, created = Issue.objects.get_or_create(book=book, student=student)
            if created:
                book.available_copies -= 1
                book.save()
                messages.success(request, f'Issue requested for book - {book.name}')
            else:
                messages.error(request, 'Issue already requested for this book.')
        else:
            messages.error(request, 'No copies available for this book.')
    else:
        messages.error(request, 'You are not a student.')

    return redirect('home')


@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def myissues(request):
    student = Student.objects.filter(student_id=request.user).first()
    if student:
        if request.GET.get('issued') is not None:
            issues = Issue.objects.filter(student=student, issued=True)
        elif request.GET.get('notissued') is not None:
            issues = Issue.objects.filter(student=student, issued=False)
        else:
            issues = Issue.objects.filter(student=student)
        return render(request, 'myissues.html', {'issues': issues})
    messages.error(request, 'You are Not a Student!')
    return redirect('/')

@login_required(login_url='/admin/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def requestedissues(request):
    if request.GET.get('studentID'):
        try:
            user = User.objects.get(username=request.GET.get('studentID'))
            student = Student.objects.filter(student_id=user).first()
            if student:
                issues = Issue.objects.filter(student=student, issued=False)
                return render(request, 'library/allissues.html', {'issues': issues})
            messages.error(request, 'No Student found')
            return redirect('/all-issues/')
        except User.DoesNotExist:
            messages.error(request, 'No Student found')
            return redirect('/all-issues/')
    else:
        issues = Issue.objects.filter(issued=False)
        return render(request, 'allissues.html', {'issues': issues})

@login_required(login_url='/admin/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def issue_book(request, issueID):
    issue = Issue.objects.get(id=issueID)
    if not issue.issued:
        issue.return_date = timezone.now() + datetime.timedelta(days=15)
        issue.issued_at = timezone.now()
        issue.issued = True
        issue.save()
        issue.book.available_copies -= 1
        issue.book.save()
    return redirect('/all-issues/')




@login_required(login_url='/student/login/')
def return_book(request, issue_id):
    if not request.user.is_superuser:
        
        issue = get_object_or_404(Issue, id=issue_id)
       
        if issue.student.student_id == request.user:
         
            calcFine(issue)
            issue.returned = True
            issue.save()
      
            issue.book.available_copies += 1
            issue.book.save()
            messages.success(request, 'Book returned successfully!')
        else:
            messages.error(request, 'You do not have permission to return this book.')
    else:
        messages.error(request, 'Admins cannot return books through this interface.')
    
    return redirect('myissues')

# FINES
@login_required(login_url='/student/login/')
def myfines(request):
    student = Student.objects.filter(student_id=request.user).first()
    if student:
        issues = Issue.objects.filter(student=student)
        for issue in issues:
            calcFine(issue)
        fines = Fine.objects.filter(student=student)
        return render(request, 'myfines.html', {'fines': fines})
    messages.error(request, 'You are Not a Student!')
    return redirect('/')

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def allfines(request):
    fines = Fine.objects.all()

    return render(request, 'allfines.html', {'fines': fines})

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def deletefine(request, fineID):
    try:
        fine = Fine.objects.get(id=fineID)
        fine.delete()
        return redirect('allfines')
    except Fine.DoesNotExist:
        return HttpResponseNotFound('Fine not found')
