from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login_page),
    url(r'^register$', views.register_page),
    url(r'^process_user$', views.process_user),
    url(r'^logout$', views.logout),
    url(r'^admin/(?P<location>\w+)$', views.admin_page),
    url(r'^process_product$', views.process_product),
    url(r'^success$', views.success_page),
    url(r'^confirm_product$', views.confirm_product),
    url(r'^delete_product/(?P<prod_id>\d+)$',views.delete_product),
    url(r'^account/(?P<user_id>\d+)/(?P<location>\w+)$', views.account_page),
    url(r'^account/(?P<user_id>\d+)/(?P<info>\w+)/edit$', views.edit_info_page),
    url(r'account/edit/(?P<user_id>\d+)$', views.process_edit),
]