from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm

from Employe import views
# SET THE NAMESPACE!
app_name = 'Employe'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[

    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^changePassword/$', views.change_password, name='change_password'),


]