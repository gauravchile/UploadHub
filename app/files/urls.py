from django.urls import path
from .views import FileUploadView, PresignedURLView

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="upload"),
    path("presign/", PresignedURLView.as_view(), name="presign"),
]
