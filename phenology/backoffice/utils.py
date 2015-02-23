import xlwt
import datetime
import time
from django.forms.forms import pretty_name
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

HEADER_STYLE = xlwt.easyxf('font: bold on')
DEFAULT_STYLE = xlwt.easyxf()
CELL_STYLE_MAP = (
    (datetime.date, xlwt.easyxf(num_format_str='DD/MM/YYYY')),
    (datetime.time, xlwt.easyxf(num_format_str='HH:MM')),
    (bool, xlwt.easyxf(num_format_str='BOOLEAN')),
)


class MyTimer:
    def __init__(self, name=""):
        self.times = []
        self.name = name

    def capture(self):
        self.times.append(str(time.clock()))

    def content(self):
        return self.times

    def output(self):
        return """### %s ### \n%s \n ######""" % (self.name,
                                                  "\n".join(self.times))
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return (datetime.datetime.min + obj).time().isoformat()

def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj


def get_column_head(obj, name):
    name = name.rsplit('.', 1)[-1]
    return pretty_name(name)


def get_column_cell(obj, name):
    try:
        attr = multi_getattr(obj, name)
    except ObjectDoesNotExist:
        return None
    if hasattr(attr, '_meta'):
        # A Django Model (related object)
        return unicode(attr).strip()
    elif hasattr(attr, 'all'):
        # A Django queryset (ManyRelatedManager)
        return ', '.join(unicode(x).strip() for x in attr.all())
    return attr


def as_workbook(queryset, columns,
                header_style=None, default_style=None,
                cell_style_map=None, workbook=None, sheet_name=""):
    if not workbook:
        workbook = xlwt.Workbook()
    report_date = datetime.date.today()
    if not sheet_name:
        sheet_name = 'Export {0}'.format(report_date.strftime('%Y-%m-%d'))
    sheet = workbook.add_sheet(sheet_name)

    if not header_style:
        header_style = HEADER_STYLE
    if not default_style:
        default_style = DEFAULT_STYLE
    if not cell_style_map:
        cell_style_map = CELL_STYLE_MAP

    obj = queryset.first()
    for y, column in enumerate(columns):
        value = get_column_head(obj, column)
        sheet.write(0, y, _(value), header_style)

    for x, obj in enumerate(queryset, start=1):
        for y, column in enumerate(columns):
            value = get_column_cell(obj, column)
            style = default_style
            for value_type, cell_style in cell_style_map:
                if isinstance(value, value_type):
                    style = cell_style
            sheet.write(x, y, value, style)

    return workbook
