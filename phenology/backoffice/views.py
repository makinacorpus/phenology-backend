# from django.shortcuts import render
import datetime
import simplejson as json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from querystring_parser import parser
from .utils import as_workbook
from backend import models
from backoffice.forms import AccountForm, AreaForm, IndividualForm,\
    CreateIndividualForm, SurveyForm, SnowingForm, ResetPasswordForm
from django.db.models import Max, Min
from django.db import connection
from backoffice.utils import MyTimer, json_serial
from django.utils.crypto import get_random_string
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string


@login_required(login_url='login/')
def index(request):
    return redirect('my-surveys')


@login_required(login_url='login/')
def register(request):
    return render(request, 'board.html')

cache_classified = []


def map_all_surveys(request):
    return render_to_response("map_all_surveys.html", {},
                              RequestContext(request))


def week_query():
    if "sqlite" in connection.vendor:
        return 'CAST((strftime("%j", date(date, "-3 days", "weekday 4")) - 1) / 7 + 1 AS INTEGER)'
    else:
        return 'CAST(extract(week from date) AS INTEGER)'


def year_query():
    if "sqlite" in connection.vendor:
        return 'CAST(STRFTIME("%Y", date) AS INTEGER)'
    else:
        return 'CAST(extract(year from date) AS INTEGER)'


def map_viz(request):
    return render_to_response("map_viz.html", {},
                              RequestContext(request))


def viz_all_surveys(request):
    return render_to_response("viz_all_surveys.html", {},
                              RequestContext(request))


def map_all_snowings(request):
    return render_to_response("map_all_snowings.html", {},
                              RequestContext(request))


def viz_area_surveys(request):
    areas = models.Area.objects.all().exclude(individual__survey__isnull=True)
    return render_to_response("viz_area_surveys.html", {"areas": areas},
                              RequestContext(request))


def get_area_data(request):
    area_id = request.GET.get("area_id")
    area = models.Area.objects.get(id=area_id)
    area_dict = {'lon': area.lon, 'lat': area.lat, 'city': area.commune,
                 'altitude': area.altitude, 'name': area.name, 'species': {},
                 'postalcode': area.postalcode}
    surveys = models.Survey.objects.filter(individual__area=area)\
                    .select_related("individual", "stage",
                                    "individual__species")
    for survey in surveys.all():
        species_dict = area_dict["species"].setdefault(
            survey.individual.species_id, {
                "name": survey.individual.species.name, "values": {}})
        stage_dict = species_dict["values"].setdefault(
            survey.stage_id, {
                "name": survey.stage.name, "values": {}})
        individual_dict = stage_dict["values"].setdefault(survey.individual_id,
                                                          [])
        individual_dict.append({
            "year": survey.date.year,
            "date": survey.date})
    return HttpResponse(json.dumps(area_dict, default=json_serial),
                        content_type="application/json")


def get_data_for_viz(request):
    """ get all amount of surveys per month classified as
        species_id/stage_id/year/month
    """
    results = {}
    cursor = connection.cursor()
    cursor.execute('SELECT ' +
                   year_query() +
                   ' as year,' +
                   week_query() +
                   ' as week, COUNT(*),' +
                   'stage_id , species_id ' +
                   'FROM backend_survey, backend_stage ' +
                   'WHERE backend_survey.stage_id=backend_stage.id ' +
                   'GROUP BY stage_id, year, week, species_id;')
    keys = ['year', 'week', 'count', 'stage_id', 'species_id']
    for survey in cursor.fetchall():
        survey_dict = dict(zip(keys, survey))
        species = results.setdefault(survey_dict["species_id"], {})
        stage = species.setdefault(survey_dict["stage_id"], {})
        year = stage.setdefault(survey_dict["year"], {})
        year[survey_dict["week"]] = int(survey_dict["count"])

    return HttpResponse(json.dumps(results, default=json_serial),
                        content_type="application/json")


def get_species_list(request):
    """ get all species with stages linked
        used to populate combobox
    """
    timer = MyTimer("get_species_list")
    timer.capture()
    cursor = connection.cursor()
    sql = 'SELECT ' + year_query() + ' as year, stage_id, COUNT(*) ' +\
          'FROM backend_survey ' +\
          'GROUP BY year, stage_id;'
    cursor.execute(sql)
    stage_years = {}
    for year, stage_id, count in cursor.fetchall():
        stages = stage_years.setdefault(stage_id, [])
        stages.append({"year": year, "count": count})

    species = [{"id": species.id,
                "label": species.name,
                "stages": [{"id": stage.id,
                            "label": stage.name,
                            "years": stage_years[stage.id],
                            "order": stage.order}
                           for stage in
                           species.stage_set.all().order_by("order")]}
               for species in models.Species.objects.all().order_by("name")]
    timer.capture()
    print timer.output()
    return HttpResponse(json.dumps(species, default=json_serial),
                        content_type="application/json")


def get_min_max_surveys(stage_id):
    cursor = connection.cursor()
    cursor.execute('SELECT ' + year_query() + ' as year,' +
                   'MAX(date) as max, MIN(date) as min ' +
                   'FROM backend_survey ' +
                   'WHERE stage_id=%s ' % stage_id +
                   'GROUP BY year order by year;')
    results = []
    for survey in cursor.fetchall():
            results.append({"min": survey[2],
                            "max": survey[1],
                            "year": survey[0]
                            })
    return results


def search_surveys(request):
    """ get all individuals
        used to get data for map rendering
        can be filtered by species (species_id)
    """
    observers = models.Observer.objects.all()
    timer = MyTimer()
    cursor = connection.cursor()
    timer.capture()
    classified = {}
    results = {}
    species_id = request.GET.get("species_id")
    individuals = models.Individual.objects.all()
    areas = models.Area.objects.all()
    if species_id:
        individuals = individuals.filter(species__id=species_id)
        areas = areas.filter(individual__species__id=species_id)
        observers = observers.filter(areas__individual__species__id=species_id)

    area_organism = {}
    area_org_sql = "SELECT area_id, observer_id, bo.organism " +\
                   "FROM backend_observer_areas as boa, backend_observer as bo " +\
                   "WHERE boa.observer_id=bo.id"
    cursor.execute(area_org_sql)
    for area_id, observer_id, organism in cursor.fetchall():
        area = area_organism.setdefault(area_id, [])
        if not organism:
            organism = "Particulier"
        area.append(organism)

    classified = {a.id: {'lon': a.lon, 'lat': a.lat, 'city': a.commune,
                         'altitude': a.altitude, 'name': a.name,
                         'id': a.id,
                         'nb_individuals': 0,
                         "organisms": ",".join(area_organism.get(a.id, [])),
                         'values': {}, 'postalcode': a.postalcode}
                  for a in areas}

    for ind in individuals:
        tmp = classified[ind.area_id]
        if (tmp['lat'] == 1 or tmp['lat'] == -1) and\
           (ind.lat != 1 and ind.lat != -1):
            tmp['lat'] = ind.lat
            tmp['lon'] = ind.lon
        tmp['nb_individuals'] += 1

    timer.capture()
    survey_sql = 'SELECT ' + year_query() + ' as year, ' +\
                 'COUNT(*), MAX(date), MIN(date), stage_id, species_id, area_id FROM backend_survey, backend_individual ' +\
                 ' WHERE backend_survey.individual_id=backend_individual.id AND ' +\
                 'backend_individual.species_id = %s ' % species_id +\
                 'GROUP BY area_id, species_id, stage_id, year ' +\
                 'ORDER BY area_id, species_id, stage_id,year;'
    cursor.execute(survey_sql)
    keys = ['year', 'count', 'max', 'min', 'stage_id', 'species_id', 'area_id']
    for survey in cursor.fetchall():
        survey_dict = dict(zip(keys, survey))
        area = results.setdefault(survey_dict["area_id"],
                                  classified.get(survey_dict["area_id"]))
        species = area['values'].setdefault(survey_dict["species_id"], {})
        stage = species.setdefault(survey_dict["stage_id"], {})
        stage[survey_dict["year"]] = {
            "minDate": survey_dict["min"],
            "maxDate": survey_dict["max"],
            "count": survey_dict["count"],
            "values": {}
        }

    survey_sql = 'SELECT ' + year_query() + ' as year, ' + week_query() + ' as week, ' +\
                 'COUNT(*), stage_id, species_id, area_id FROM backend_survey, backend_individual ' +\
                 ' WHERE backend_survey.individual_id=backend_individual.id AND ' +\
                 'backend_individual.species_id = %s ' % species_id +\
                 'GROUP BY area_id, species_id, stage_id, year,  week ' +\
                 'ORDER BY area_id, species_id, stage_id,year,week;'
    cursor.execute(survey_sql)
    keys = ['year', 'week', 'count', 'stage_id', 'species_id', 'area_id']
    for survey in cursor.fetchall():
        survey_dict = dict(zip(keys, survey))
        area = classified.get(survey_dict["area_id"])
        species = area['values'].setdefault(survey_dict["species_id"], {})
        stage = species.setdefault(survey_dict["stage_id"], {})
        year = stage.setdefault(survey_dict["year"], {})
        year["values"][survey_dict["week"]] = survey_dict["count"]

    timer.capture()
    print timer.output()

    return HttpResponse(json.dumps(classified, default=json_serial),
                        content_type="application/json")


def get_area_snowings(request):
    """ get all individuals
        used to get data for map rendering
        can be filtered by species (species_id)
    """
    area_id = request.GET.get("area_id")
    area = models.Area.objects.get(id=area_id)
    snowings = list(area.snowing_set.all().
                    filter(height__gt=0).
                    filter(height__lt=999).
                    values("height", "date"))
    timer = MyTimer()
    # cursor = connection.cursor()
    timer.capture()
    max_height = 1
    if snowings:
        max_height = max([float(s["height"]) for s in snowings])

    classified = {"id": area_id,
                  "maxHeight": max_height,
                  "name": area.name,
                  "altitude": area.altitude,
                  "snowings": snowings
                  }
    timer.capture()
    print timer.output()

    return HttpResponse(json.dumps(classified, use_decimal=True,
                                   default=json_serial),
                        content_type="application/json")


def search_snowings(request):
    """ get all individuals
        used to get data for map rendering
        can be filtered by species (species_id)
    """
    # observers = models.Observer.objects.all()
    timer = MyTimer()
    cursor = connection.cursor()
    timer.capture()
    classified = {}

    # species_id = request.GET.get("species_id")
    # individuals = models.Individual.objects.all()
    areas = models.Area.objects.all()

    area_organism = {}
    area_org_sql = "SELECT area_id, observer_id, bo.organism " +\
                   "FROM backend_observer_areas as boa, backend_observer as bo " +\
                   "WHERE boa.observer_id=bo.id"
    cursor.execute(area_org_sql)
    for area_id, observer_id, organism in cursor.fetchall():
        area = area_organism.setdefault(area_id, [])
        if not organism:
            organism = "Particulier"
        area.append(organism)

    classified = {a.id: {'lon': a.lon, 'lat': a.lat, 'city': a.commune,
                         'altitude': a.altitude, 'name': a.name,
                         'nb_individuals': 0,
                         'organisms': ','.join(area_organism.get(a.id, [])),
                         'values': {}, 'postalcode': a.postalcode}
                  for a in areas}

    # for ind in individuals:
    #     tmp = classified[ind.area_id]
    #     if (tmp['lat'] == 1 or tmp['lat'] == -1) and\
    #        (ind.lat != 1 and ind.lat != -1):
    #         tmp['lat'] = ind.lat
    #         tmp['lon'] = ind.lon
    #     tmp['nb_individuals'] += 1

    timer.capture()
    snowing_sql = 'SELECT ' + year_query() + ' as year,  area_id, MAX(height) ' +\
                  'FROM backend_snowing ' +\
                  'WHERE height < 999  AND height > 0 ' +\
                  'GROUP BY area_id, year ' +\
                  'ORDER BY area_id, year;'
    cursor.execute(snowing_sql)
    keys = ['year', 'area_id', 'height']
    for snowing in cursor.fetchall():
        snowing_dict = dict(zip(keys, snowing))
        area = classified.get(snowing_dict["area_id"])
        area['values'][snowing_dict["year"]] = snowing_dict["height"]

    timer.capture()
    print timer.output()

    return HttpResponse(json.dumps(classified,
                                   use_decimal=True,
                                   default=json_serial),
                        content_type="application/json")


def export_surveys(request):
    columns = ['stage', 'date', 'individual.species',
               'individual.area.commune', 'answer']
    if(request.GET.get("id")):
        observer = models.Observer.objects.get(id=int(request.GET.get("id")))
    else:
        observer = request.user.observer
    queryset = models.Survey.objects.\
        filter(individual__area__observer=observer).all()
    years = queryset.aggregate(Min('date'), Max('date'))
    min_year = years["date__min"].year
    max_year = years["date__max"].year
    workbook = None
    for year in range(min_year, max_year + 1):
        queryset_tmp = queryset.filter(date__year=year)
        workbook = as_workbook(queryset_tmp, columns,
                               workbook=workbook, sheet_name=str(year))
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'
    workbook.save(response)
    return response


@login_required(login_url='login/')
def area_detail(request, area_id=-1):
    area = models.Area.objects.filter(id=area_id).first()
    if not area:
        area = models.Area()
        area.observer = request.user.observer

    if area_id == -1 or request.user.observer in area.observer_set.all():
        if request.POST:
            form = AreaForm(request.POST, instance=area)
            if form.is_valid():
                messages.add_message(request,
                                     messages.SUCCESS,
                                     _('Form is successifully updated'))
                form.save()
                return redirect('area-detail', area_id=form.instance.id)
        else:
            form = AreaForm(instance=area)
        return render_to_response("profile_area.html", {
            "form": form,
        }, RequestContext(request))
    else:
        return redirect(index)


@login_required(login_url='login/')
def individual_detail(request, ind_id=-1):
    individual = models.Individual.objects.filter(id=ind_id).first()
    if not individual:
        individual = models.Individual()
        area_id = request.GET.get("area_id")
        area = models.Area.objects.get(id=area_id)
        individual.area = area
        individual.lat = area.lat
        individual.lon = area.lon

    surveys = sorted(individual.survey_set.all(),
                     key=lambda survey: survey.date,
                     reverse=True)
    surveys = surveys[:8]

    if individual.id:
        if request.user.observer in individual.area.observer_set.all():
            if request.POST:
                form = IndividualForm(request.POST, instance=individual)
                if form.is_valid():
                    messages.add_message(request,
                                         messages.SUCCESS,
                                         _('Form is successifully updated'))
                    form.save()
            else:
                form = IndividualForm(instance=individual)
        else:
            messages.add_message(request,
                                 messages.WARNING,
                                 _('Your are not allowed to see this form'))
            return redirect(index)
    else:
        if request.POST:
            form = CreateIndividualForm(request.POST, instance=individual)
            if form.is_valid():
                messages.add_message(request,
                                     messages.SUCCESS,
                                     _('Form is successifully updated'))
                form.save()
                return redirect('individual-detail', ind_id=form.instance.id)

        else:
            form = CreateIndividualForm(instance=individual)

    return render_to_response("profile_individual.html", {
        "form": form,
    }, RequestContext(request))


@login_required(login_url='login/')
def survey_detail(request, survey_id=-1):
    survey = models.Survey.objects.filter(id=survey_id).first()
    if not survey:
        survey = models.Survey()
        ind_id = request.GET.get("ind_id")
        individual = models.Individual.objects.get(id=ind_id)
        if individual:
            survey.individual = individual
            survey.date = datetime.date.today()
            # TODO : improve how we get stage
            stage = models.Stage.objects.get(id=request.GET.get("stage_id"))
            if not stage:
                stage = individual.species.stage_set.\
                    filter(is_active=True).all().first()
            survey.stage = stage

    if request.POST:
        form = SurveyForm(request.POST,
                          instance=survey)

        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _('Form is successifully updated'))
            form.save()
            return redirect('survey-detail', survey_id=form.instance.id)
        else:
            print form.errors
    else:
        form = SurveyForm(instance=survey)
    return render_to_response("survey.html", {
        "form": form,
    }, RequestContext(request))


@login_required(login_url='login/')
def snowing_detail(request, area_id, snowing_id=-1):
    timer = MyTimer()
    timer.capture()
    snowing = models.Snowing.objects.filter(id=snowing_id).first()
    snowings = []
    if not snowing:
        snowing = models.Snowing()
        area = models.Area.objects.get(id=area_id)
        if area:
            snowing.observer = request.user.observer
            snowing.area = area
            snowing.date = datetime.date.today()
    timer.capture()
    if request.POST:
        snowing.observer = request.user.observer
        form = SnowingForm(request.POST,
                           instance=snowing)

        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _('Form is successifully updated'))
            form.save()
            return redirect('snowing-detail', area_id=form.instance.area.id, snowing_id=form.instance.id)
        else:
            print form.errors
    else:
        form = SnowingForm(instance=snowing)
    timer.capture()
    query = models.Snowing.objects.all().filter(area=snowing.area.id)
    if(snowing.id):
        query = query.exclude(id=snowing.id)
    snowings = [{"date": s.date.strftime("%Y-%m-%d"),
                 "id": s.id,
                 "height": s.height}
                for s in query]
    #snowings = []
    timer.capture()
    print timer.output()
    return render_to_response("snowing.html", {
        "form": form,
        "snowings": snowings
    }, RequestContext(request))


@login_required(login_url='login/')
def user_detail(request):
    if not request.user.observer:
        request.user.observer = models.Observer()
        request.user.save()
    if request.POST:
        form = AccountForm(request.POST,
                           instance=request.user.observer)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _('Form is successifully updated'))
            form.save()
        else:
            print form.errors
    else:
        form = AccountForm(instance=request.user.observer)

    return render_to_response("profile.html", {
        "form": form,
    }, RequestContext(request))


def register_user(request):
    if request.user and request.user.username:
        return redirect(index)

    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _('Form is successifully updated'))
            form.save()
        else:
            print form.errors
    else:
        instance = models.Observer()
        instance.user = User()
        form = AccountForm(instance=instance)

    return render_to_response("generic_form.html", {
        "form": form,
    }, RequestContext(request))


@login_required(login_url='login/')
def dashboard(request):
    return render_to_response("profile_display.html", RequestContext(request))


@login_required(login_url='login/')
def all_surveys(request):
    surveys = models.Survey.objects.all()[:100]
    return render_to_response("all_surveys.html", {
        "surveys": surveys}, RequestContext(request))


def get_surveys(request):
    mapping = {
        "id": "id",
        "observer": "observer",
        "date": "date",
        "species": "individual__species__name",
        "individual": "individual__name",
        "area": "individual__area__name",
        "stage": "stage__name",
        "answer": "answer"
    }
    parsed = parser.parse(request.GET.urlencode())
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search = request.GET.get("search[value]", "")
    draw = request.GET.get("draw", 1)
    query = models.Survey.objects
    query = query.filter(Q(individual__name__icontains=search)
                         | Q(individual__area__name__icontains=search)
                         | Q(individual__species__name__icontains=search)
                         | Q(individual__species__name__icontains=search))

    for ord in parsed["order"].values():
        col = parsed["columns"][ord["column"]]["data"]
        query_1 = mapping.get(col, col)
        if ord["dir"] == "desc":
            query_1 = "-" + query_1
        query = query.order_by(query_1)

    filtered_total = query.count()
    filtered_data = query.select_related('individual').all()[start:
                                                             start + length]
    response_data = {
        "draw": int(draw),
        "data": [{"id": o.id,
                  "date": str(o.date),
                  "area": o.individual.area.name,
                  "species": o.individual.species.name,
                  "individual": "",
                  "organisms": ",".join([a.organism
                                         for a in
                                         o.individual.area.observer_set.all()]
                                        ),
                  "stage": o.stage.name,
                  "answer": o.answer,
                  "categorie": ",".join([a.category
                                         for a in
                                         o.individual.area.observer_set.all()]
                                        )
                  }
                 for o in filtered_data],
        "recordsTotal": models.Survey.objects.count(),
        "recordsFiltered": filtered_total
    }
    return HttpResponse(json.dumps(response_data, default=json_serial),
                        content_type="application/json")
from django.db.models import Count


def viz_snowings(request):
    query = models.Snowing.objects.filter(height__gt=0).\
        filter(height__lt=999).values("area").annotate(count=Count('id'))

    area_ids = {s["area"]: s["count"] for s in query if int(s["count"]) > 50}
    areas = list(models.Area.objects.filter(pk__in=area_ids.keys()))
    areas = sorted(areas, key=lambda a: (int(area_ids[a.id])), reverse=True)
    return render_to_response("viz_snowings.html", {"areas": areas},
                              RequestContext(request))


def password_reset(request):
    template = "password_new_form.html"
    if request.POST:
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.data["email"]
            password = get_random_string()
            user = User.objects.get(email=email)
            if user:
                user.set_password(password)
                message = render_to_string('password_new_email.html',
                                           {'user': user,
                                            'password': password})
                user.save()
                mail.send_mail(
                    subject=_(u"New password"),
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False)

                template = "password_new_done.html"
    else:
        form = ResetPasswordForm()
    return render_to_response(template, {
        "form": form
    }, RequestContext(request))
