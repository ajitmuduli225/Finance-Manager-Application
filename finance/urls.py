
from django.urls import path
from finance.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('delete-transaction/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
    path('generate_report/',generate_report,name='generate_report'),
    path('set_budget/',set_budget,name='set_budget'),
    path('check_budget/',check_budget,name='check_budget')

]
