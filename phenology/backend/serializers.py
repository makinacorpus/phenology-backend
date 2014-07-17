from django.contrib.auth.models import User, Group
from rest_framework import serializers
from backend import models
from django.db.models import Q
import datetime
from dateutil.relativedelta import relativedelta


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #groups = serializers.RelatedField()

    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stage


class SnowingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Snowing


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Survey


class IndividualSerializer(serializers.ModelSerializer):
    surveys = SurveySerializer(source="survey_set")

    class Meta:
        model = models.Individual
        exclude = ('species', 'observer', 'area')


class SpeciesSerializer(serializers.ModelSerializer):
    individuals = IndividualSerializer(source="individual_set")
    stages = StageSerializer(source="stage_set")

    class Meta:
        model = models.Species
        fields = ('id', 'name', 'description',
                  'pictures', 'individuals', 'stages')


class SpeciesNestedSerializer(serializers.ModelSerializer):
    individuals = serializers.SerializerMethodField('get_individuals')

    def get_individuals(self, *args, **kwargs):
        species = args[0]
        indiv_q = models.Individual\
                        .objects\
                        .filter(Q(observer=self.context["user_target"])
                                & Q(species=species)
                                & Q(area=self.context["area_target"]))\
                        .select_related()
        serializer = IndividualSerializer(instance=indiv_q,
                                          many=True, context=self.context)
        return serializer.data

    class Meta:
        model = models.Species


class AreaNestedSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField('get_species')

    def get_species(self, *args, **kwargs):
        area = args[0]
        species_q = models.Species\
                          .objects\
                          .filter(Q(individual__observer=self.parent.object)
                                  & Q(individual__area=args[0])
                                  & Q(area=area)).distinct().select_related()
        self.context["user_target"] = self.parent.object
        self.context["area_target"] = area
        serializer = SpeciesNestedSerializer(instance=species_q,
                                             many=True, context=self.context)
        return serializer.data

    class Meta:
        model = models.Area


class ObserverSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="user", read_only=True)
    areas = AreaNestedSerializer(many=True, source="areas", read_only=True)
    
    class Meta:
        model = models.Observer
