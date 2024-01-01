from django.contrib import admin
from django.urls import path
from dashboard import views
from django.contrib import admin

admin.site.site_header="Student Study Portal"

urlpatterns = [
   path('', views.home, name='home'),
   path('notes', views.notes, name='notes'),
   path('notesdelete/<int:nid>', views.notesdelete, name='notesdelete'),
   path('notesdetail/<str:name>', views.notesdetail, name='notesdetail'),
   path('homework', views.homework, name='homework'),
   path('updatehomework/<int:hid>', views.updatehomework, name='updatehomework'),
   path('deletehomework/<int:hid>', views.deletehomework, name='deletehomework'),
   path('youtube', views.youtube, name='youtube'),
   path('todo', views.todo, name='todo'),
   path('updatetodo/<int:tid>', views.updatetodo, name='updatetodo'),
   path('deletetodo/<int:tid>', views.deletetodo, name='deletetodo'),
   path('books', views.books, name='books'),
   path('dictionary', views.dictionary, name='dictionary'),
   path('wiki', views.wiki, name='wiki'),
   path('register', views.register, name='register'),
   path('fnlogin', views.fnlogin, name='fnlogin'),
   path('fnlogout', views.fnlogout, name='fnlogout'),
   path('profile', views.profile, name='profile'),
   path('calculation', views.calculation, name='calculation'),
]