
from django.conf.urls import url, include
from core.views import index, classify_image, signup, user_dashboard, my_contributions, project_status, tutorial

app_name = 'core'
urlpatterns = [
    url(r'^classify/?', classify_image, name='classify'),
    url(r'^my_contributions/?', my_contributions, name='my_contributions'),
    url(r'^project_status/?', project_status, name='project_status'),

    url('^accounts/signup/?', signup, name='signup'),
    
    url('^dashboard/?', user_dashboard, name='dashboard'),
    url('^tutorial/?', tutorial, name='tutorial'),
    url(r'^$', index),
]
