
import os
import re

from django.core.management.base import BaseCommand
from landez import TilesManager
from landez.sources import DownloadError
#from urllib2 import unquote
from zipfile import ZipFile
from phenology.settings import TILES_SETTINGS
from backend import logger
from backend.models import Area, Individual


class ZipTilesBuilder(object):
    def __init__(self, filepath, **builder_args):
        self.zipfile = ZipFile(filepath, 'w')
        self.tm = TilesManager(**builder_args)
        self.tiles = set()

    def add_coverage(self, bbox, zoomlevels):
        self.tiles |= set(self.tm.tileslist(bbox, zoomlevels))

    def run(self):
        for tile in self.tiles:
            name = '{0}/{1}/{2}.png'.format(*tile)
            try:
                data = self.tm.tile(tile)
            except DownloadError:
                logger.warning("Failed to download tile %s" % name)
            else:
                self.zipfile.writestr(name, data)
        self.zipfile.close()


def format_from_url(url):
    """
    Try to guess the tile mime type from the tiles URL.
    Should work with basic stuff like `http://osm.org/{z}/{x}/{y}.png`
    or funky stuff like WMTS (`http://server/wmts?LAYER=...FORMAT=image/jpeg...)
    """
    m = re.search(r'FORMAT=([a-zA-Z/]+)&', url)
    if m:
        return m.group(1)
    return url.rsplit('.')[-1]


def format_size(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1  # increment the index of the suffix
        size = size / 1024.0  # apply the division
    return "%.*f %s" % (precision, size, suffixes[suffixIndex])


def remove_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


class Command(BaseCommand):
    help = "Build tiles (global + area) for mobile application"

    def execute(self, *args, **options):
        """ Execute command """
        self.output_folder = TILES_SETTINGS['TILES_ROOT']

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.builder_args = {}

        self._build_global_tiles()
        self._build_area_tiles()
        logger.info('Done.')

    def _build_global_tiles(self):
        """ Creates a tiles file on the global extent.
        Builds a temporary file and overwrites the existing one on success.
        """
        self.builder_args['tiles_url'] = TILES_SETTINGS['TILES_URL']
        self.builder_args['tile_format'] = format_from_url(TILES_SETTINGS['TILES_URL'])

        global_file = os.path.join(self.output_folder, 'global.zip')
        tmp_gobal_file = global_file + '.tmp'

        logger.info("Build global tiles file...")
        tiles = ZipTilesBuilder(filepath=tmp_gobal_file, **self.builder_args)
        tiles.add_coverage(bbox=TILES_SETTINGS['GLOBAL_MAP_BBOX'],
                           zoomlevels=TILES_SETTINGS['TILES_GLOBAL_ZOOMS'])
        tiles.run()

        remove_file(global_file)
        os.rename(tmp_gobal_file, global_file)
        logger.info('%s done. size : %s' % (global_file, format_size(os.stat(global_file).st_size)))

    def _build_area_tiles(self):
        """ Creates a tiles file for a specific area
        Builds a temporary file and overwrites the existing one on success.
        """
        for area in Area.objects.all():
            area_file = os.path.join(self.output_folder, 'area_%s.zip' % area.id)
            tmp_area_file = area_file + '.tmp'

            if not (area.lon and area.lat and not(area.lon != 1 and area.lat != -1)):
                inds = Individual.objects.filter(area=area)
                for ind in inds:
                    if ind.lon and ind.lat and ind.lat != 1:
                        coords = [(ind.lon, ind.lon)]
                        break
            else:
                coords = [(area.lon, area.lat)]

            self._build_tiles_along_coords(tmp_area_file, coords)
            remove_file(area_file)
            os.rename(tmp_area_file, area_file)
            logger.info('%s done. %s' % (area_file, format_size(os.stat(area_file).st_size)))

    def _build_tiles_along_coords(self, filepath, coords):
        """ For each point of the specified coordinates, it covers an area
        with a small radius on high zoom levels, and large radius on lower zoom
        levels.
        """
        def _radius2bbox(lng, lat, radius):
            return (lng - radius, lat - radius,
                    lng + radius, lat + radius)

        tiles = ZipTilesBuilder(filepath=filepath, **self.builder_args)

        for (lng, lat) in coords:
            small = _radius2bbox(lng, lat, TILES_SETTINGS['TILES_RADIUS_SMALL'])
            tiles.add_coverage(bbox=small,
                               zoomlevels=TILES_SETTINGS['TILES_AREA_ZOOMS'])

        tiles.run()
