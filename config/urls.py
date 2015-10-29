from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^matriculas/', include('matriculas.urls')),
    url(r'^', include('matriculas.urls', namespace = "matriculas")),
    url(r'^admin/', include(admin.site.urls)),
    
]
