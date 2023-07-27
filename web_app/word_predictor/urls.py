# urls.py
from django.urls import path
from . import predict

urlpatterns = [
    path('my_post_view/', predict.predict_next_word, name='my_post_view'),
]