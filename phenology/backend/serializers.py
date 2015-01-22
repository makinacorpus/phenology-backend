from django.contrib.auth.models import User, Group
from rest_framework import serializers
from backend import models
from django.db.models import Q
import datetime
from dateutil.relativedelta import relativedelta
from django.db import models as django_db_models
from django import forms
from rest_framework import serializers as rest_fields


class TranslatedModelSerializer(serializers.ModelSerializer):
    class Meta:
        pass

    def get_field(self, model_field):
        kwargs = {}
        #print model_field
        #print dir(self)
        if issubclass(
                model_field.__class__, (django_db_models.CharField, django_db_models.TextField)):
            if model_field.null:
                kwargs['allow_none'] = True
            kwargs['max_length'] = getattr(model_field, 'max_length')
            return rest_fields.CharField(**kwargs)
        return super(TranslatedModelSerializer, self).get_field(model_field)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #groups = serializers.RelatedField()

    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class StageSerializer(TranslatedModelSerializer):
    class Meta:
        model = models.Stage
        fields = ("id", "name", "species",
                  "day_start", "month_start",
                  "day_end", "month_end",
                  "order", "picture_before",
                  "picture_current", "picture_after",
                  "is_active")


class SnowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Snowing
        exclude = ('observer',)


class SurveySerializer(serializers.ModelSerializer):
    #date = serializers.DateField(format="YYYY-MM-DD", source="date")
    species = serializers.SerializerMethodField('get_species')
    area = serializers.SerializerMethodField('get_area')

    class Meta:
        model = models.Survey

    def get_species(self, obj):
        return obj.individual.species.id

    def get_area(self, obj):
        return obj.individual.area.id


class IndividualSerializer(serializers.ModelSerializer):
    surveys = SurveySerializer(source="survey_set")

    class Meta:
        model = models.Individual
        exclude = ('species', 'area')


class SpeciesSerializer(TranslatedModelSerializer):
    #individuals = IndividualSerializer(source="individual_set")
    stages = StageSerializer(source="stage_set")

    class Meta:
        model = models.Species
        fields = ('id', 'name', 'description',
                  'picture', 'stages')


class SimpleStageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stage
        fields = ('id',)


# used in observers endpoint
class IndividualNestedSerializer(serializers.ModelSerializer):
    stages = serializers.SerializerMethodField('get_stages')

    def get_stages(self, *args, **kwargs):
        individual = args[0]
        survey_date_minimum = datetime.date.today() - relativedelta(months=9)
        # stages that we have surveys for this individual
        #surveys date can't be lower than today - 9 months
        indiv_q = models.Stage\
                        .objects\
                        .filter(Q(species__individual=individual) &
                                Q(survey__individual=individual))\
                        .exclude(survey__date__lt=survey_date_minimum)\
                        .select_related()
        serializer = SimpleStageSerializer(instance=indiv_q,
                                           many=True,
                                           context=self.context)
        return serializer.data

    class Meta:
        model = models.Individual
        exclude = ('species', 'observer', 'area')


# used in observers endpoint
class SpeciesNestedSerializer(serializers.ModelSerializer):
    individuals = serializers.SerializerMethodField('get_individuals')

    def get_individuals(self, *args, **kwargs):
        species = args[0]
        indiv_q = models.Individual\
                        .objects\
                        .filter(Q(species=species)
                                & Q(area=self.context["area_target"]))\
                        .select_related()
        serializer = IndividualNestedSerializer(instance=indiv_q,
                                                many=True,
                                                context=self.context)
        return serializer.data

    class Meta:
        model = models.Species
        fields = ('id', 'individuals',)


# used in observers endpoint
class AreaNestedSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField('get_species_for_area')

    def get_species_for_area(self, *args, **kwargs):
        area = args[0]
        species_q = models.Species\
                          .objects\
                          .filter(Q(area__observer=self.parent.object)
                                  & Q(individual__area=args[0])
                                  & Q(area=area)).distinct().select_related()
        self.context["user_target"] = self.parent.object
        self.context["area_target"] = area
        serializer = SpeciesNestedSerializer(instance=species_q,
                                             many=True, context=self.context)
        return serializer.data

    def get_geojson(self, *args, **kwargs):
        area = args[0]
        return area.geojson

    class Meta:
        model = models.Area


class ObserverSerializer(serializers.ModelSerializer):
    # his user account
    user = UserSerializer(source="user", read_only=True)
    # his areas
    areas = AreaNestedSerializer(many=True, source="areas", read_only=True)
    # his list of species related to his individuals found
    species = serializers.SerializerMethodField('get_species_for_observer')

    def get_species_for_observer(self, *args, **kwargs):
        observer = args[0]
        species_q = models.Species\
                          .objects\
                          .filter(Q(area__observer=observer))\
                          .distinct()
        serializer = SpeciesSerializer(instance=species_q,
                                       many=True, context=self.context)
        return serializer.data

    class Meta:
        model = models.Observer
