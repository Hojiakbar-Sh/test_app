from django.contrib import admin
from django.urls import path

from variant.views import subject_list_view, subject_view, variant_view, result_view, VariantCreateView

app_name = 'test'
urlpatterns = [
    path('subjects/', subject_list_view, name='subject_list'),
    path('subjects/<int:pk>/', subject_view, name='subject'),
    path('variant/<int:pk>/', variant_view, name='variant'),
    path('variant/edit/<int:pk>/', variant_view, name='variant_edit'),
    path('variant/delete/<int:pk>/', variant_view, name='variant_delete'),
    path('results/<int:pk>/', result_view, name='result'),

    # for teachers
    path('variant/create/', VariantCreateView.as_view(), name='variant_create'),
]
