from django.urls import path
from .views import BoxAdd, BoxListAll, BoxUpdate, BoxDelete, MyBoxes

urlpatterns = [
    path("", BoxListAll().as_view(), name="listall"),
    path("add/", BoxAdd.as_view(), name="create"),
    path("update/<int:pk>", BoxUpdate.as_view(), name="update"),
    path("delete/<int:pk>", BoxDelete.as_view(), name="delete"),
    path("myboxes/", MyBoxes.as_view(), name="listmy"),
]
