from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Info
from .serializers import InfoSerializer

@api_view(['GET'])
def info_detail(request, slug):
    if request.method == 'GET' and request.user.is_authenticated:
        info = get_object_or_404(Info, slug=slug)
        serializer = InfoSerializer(info)
        return Response(serializer.data)


from .models import ExampleLanguage, Examples
from .serializers import ExamplesSerializer


@api_view(['GET'])
def examples_by_language(request, language_id):
    try:
        language = ExampleLanguage.objects.get(id=language_id)
    except ExampleLanguage.DoesNotExist:
        return Response(status=404)

    examples = Examples.objects.filter(language=language)
    serializer = ExamplesSerializer(examples, many=True)
    return Response(serializer.data)