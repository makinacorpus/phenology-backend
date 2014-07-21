#from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from backend import models, serializers as serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def user_settings(request):
    serializer = serializers.ObserverSerializer(request.user.observer)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT'])
def user_surveys(request):
    surveys = models.Survey.objects.filter(observer__user=request.user)
    serializer = serializers.SurveySerializer(surveys)
    return Response(serializer.data)


#@api_view(['GET'])
class ObserverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows areas to be viewed or edited.
    """
    serializer_class = serializers.ObserverSerializer
    model = models.Observer


class AreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows areas to be viewed or edited.
    """
    model = models.Area


class IndividualViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows areas to be viewed or edited.
    """
    serializer_class = serializers.IndividualSerializer
    model = models.Individual


class SpeciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows areas to be viewed or edited.
    """
    serializer_class = serializers.SpeciesSerializer
    model = models.Species


class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows areas to be viewed or edited.
    """
    serializer_class = serializers.SurveySerializer
    model = models.Survey
