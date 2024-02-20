from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[
    path('income', views.index, name="income"),
    path('add-income', views.add_income, name="add-income"),
    path('edit-income/<int:id>', views.income_edit, name="income-edit"),
    path('income-delete/<int:id>', views.delete_income, name="income-delete"),
    path('search-income', csrf_exempt(views.search_income),
         name="search_income"),
    path('income_source_summary', views.income_source_summary,
         name="income_source_summary"),
    path('stats_view_income', views.stats_view_income,
         name="stats_view_income"),
    path('export_csv_csv', views.export_csv_csv,
         name="export-csv-csv"),
    path('export_excel_excel', views.export_excel_excel,
         name="export-excel-excel"),
]