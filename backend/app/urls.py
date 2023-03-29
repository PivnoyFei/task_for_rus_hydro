from app.views import DocumentView
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('documents/', DocumentView.as_view(), name='documents'),
]
