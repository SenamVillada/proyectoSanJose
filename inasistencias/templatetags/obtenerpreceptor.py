from django import template
from inasistencias.models import Preceptor

register = template.Library()

@register.simple_tag
def preceptor(preceptor):
    preceptor = Preceptor.objects.get(username=preceptor)
    return preceptor.id
