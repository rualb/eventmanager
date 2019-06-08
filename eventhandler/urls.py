from django.urls import path

from . import views

from .forms import EventRecordForm
from .models import EventRecord


from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

urlpatterns = [

    path("list/",
         views.EventRecordListView.as_view(),
         name='eventrecord_list'),
 
    path("<int:pk>/detail",
        views.EventRecordDetail.as_view(),
        name="eventrecord_detail"),
    path("<int:pk>/copy",
        views.EventRecordCopy.as_view(),
        name="eventrecord_copy"),

    path("create",
         views.EventRecordCreate.as_view(),
         name="eventrecord_create"),
 

    path("<int:pk>/edit",
         views.EventRecordUpdate.as_view(),
         name="eventrecord_edit"),
]
