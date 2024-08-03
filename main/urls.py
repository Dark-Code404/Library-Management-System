from django.urls import path
from .views import *
urlpatterns = [
    path('',allbooks,name='home'),
    path('search/',search),
    path('sort/',sort),
    path('addbook/',addbook,name='addbook'),
    path('deletebook/<int:bookID>/',deletebook),
    path('request-book-issue/<int:bookID>/', issuerequest, name='request-book-issue'),

    path('my-issues/',myissues,name='myissues'),
    path('my-fines/',myfines),
    path('all-issues/',requestedissues),
    path('all-fines/',allfines,name='allfines'),
    path('issuebook/<int:issueID>/',issue_book),
    path('deletefine/<int:fineID>/',deletefine,name='deletefine'),
     path('returnbook/<int:issue_id>/', return_book, name='return_book'),
     
]
