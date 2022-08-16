from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('podjetja/<int:pk>', views.CompanyDetailsView.as_view(), name='company-details'),
    path('podjetja/<int:pk>/izbrisi', views.CompanyDeleteConfirmView.as_view(), name='company-delete'),
    path('podjetja/', views.CompanyView.as_view(), name='companies'),
    path('podjetja/dodaj/', views.AddNewCompany.as_view(), name='add-company'),

    path('zgodovina/', views.HistoryView.as_view(), name='history'),
    path('izpis/', views.OutputView.as_view(), name='output'),

    path('<str:pk>/', views.BillDetailsView.as_view(), name='bill-details'),
    path('<str:bill_id>/<int:pk>', views.ProductsDetailsView.as_view(), name='product-details'),
    path('<str:bill_id>/<int:pk>/izbrisi', views.ProductDeleteConfirmView.as_view(), name='product-delete'),
    path('<str:bill_id>/dodaj', views.AddNewProduct.as_view(), name='add-product'),


]