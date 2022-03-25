import xlrd
import pdb
from helpers.location_herper import LocationHelper
from scrapper import Scrapper
from process_output import Writer


class Reader:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        first_line = True
        location = ('data/{}'.format(self.filename))
        workbook = xlrd.open_workbook(location)
        sheet = workbook.sheet_by_index(0)
        for line in sheet:
            if first_line:
                first_line = False
                continue
            rol_first, rol_second = line[0].value.strip().split('-')
            raw_commune = line[1].value.upper().strip()
            commune = LocationHelper().translate_commune(raw_commune)
            raw_region = LocationHelper().get_region(commune)
            region = LocationHelper().solve_region(raw_region)
            scrapper = Scrapper(region=region, commune=commune, rol_first=rol_first, rol_second=rol_second)
            try:
                data = scrapper.scrap()
            except:
                data = [commune, '{}-{}'.format(rol_first, rol_second), 'SCRAPPING ERROR']

            writer = Writer(data).write(region, commune, rol_first, rol_second)

    def solve_region(self, region):
        {}