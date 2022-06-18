from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('auth/<page>/',views.auth),
    # path('<page>/<action>',views.action),
    path('<page>/<opration>/<int:id>',views.actionId),
    path('<page>/',views.actionId),
    path('',views.index),
]