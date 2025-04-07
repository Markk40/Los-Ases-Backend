from django.urls import path
from .views import hello_view, index, detail, create, edit, delete

urlpatterns = [
    path('hello/', hello_view, name='hello'),
    path("", index, name="index"),
    path("<int:auction_id>", detail, name="detail"),
    path('new/', create, name='create'),
    path('edit/<int:auction_id>/', edit, name='edit'),
    path('delete/<int:auction_id>/', delete, name='delete'),
]
