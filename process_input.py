import xlrd
import pdb
from selenium import webdriver
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
        
        # Crear un único navegador para todos los registros
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        
        try:
            for line in sheet:
                if first_line:
                    first_line = False
                    continue
                rol_first, rol_second = line[0].value.strip().split('-')
                raw_commune = line[1].value.upper().strip()
                commune = LocationHelper().translate_commune(raw_commune)
                raw_region = LocationHelper().get_region(commune)
                region = LocationHelper().solve_region(raw_region)
                
                # Pasar el driver compartido al scrapper
                scrapper = Scrapper(region=region, commune=commune, rol_first=rol_first, rol_second=rol_second, driver=driver)
                try:
                    data = scrapper.scrap()
                except Exception as e:
                    print(f"Error scrapeando {commune} {rol_first}-{rol_second}: {str(e)}")
                    data = [[commune, '{}-{}'.format(rol_first, rol_second), 'SCRAPPING ERROR']]

                writer = Writer(data).write(region, commune, rol_first, rol_second)
        finally:
            # Cerrar el navegador al final de procesar todos los registros
            driver.quit()
            print("Navegador cerrado correctamente")

    def solve_region(self, region):
        {}