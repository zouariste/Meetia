from django.conf.urls import url

from Employe import views
# SET THE NAMESPACE!
app_name = 'Employe'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[

    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^changePassword/$', views.change_password, name='change_password'),


]