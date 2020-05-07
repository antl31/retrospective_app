from schema import schema
from django.http import JsonResponse


def download_schema(request):
    introspection_dict = schema.introspect()
    return JsonResponse(introspection_dict)
