import time
import pdb
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options


class Scrapper:
    def __init__(self, region, commune, rol_first, rol_second):
        self.region = region
        self.commune = commune
        self.rol_first = rol_first
        self.rol_second = rol_second

    def scrap(self):
        region = self.region
        commune = self.commune
        rol_first = self.rol_first
        rol_second = self.rol_second
        output_data = []

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path='/Users/orlando/Dev/Playground/cobanc/scrapper/webdriver/chromedriver',
                                  chrome_options=chrome_options)
        driver.get('https://www4.sii.cl/cuotaanualbienesraicespubinternetui/#!/buscaRolPagos')
        # select region
        time.sleep(1)
        try:
            region_select = "//select[@ng-model='regionModel']/option[text()='" + region + "']"
            driver.find_element_by_xpath(region_select).click()
        except:
            output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR REGION: {}'.format(region)])
            return output_data
        time.sleep(1)

        # select commune
        try:
            select = Select(driver.find_element_by_id('codigo'))
            select.select_by_visible_text(commune)
        except:
            output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR COMUNA'])
            return output_data


        # set rol
        element = driver.find_element_by_id("manzana")
        element.send_keys(rol_first)

        # set rol digit
        element = driver.find_element_by_id("predio")
        element.send_keys(rol_second)

        #search
        driver.find_element_by_xpath('//button[text()="Buscar"]').click()

        #search
        time.sleep(1)

        no_debt = False
        try:
            if 'Bien Raíz no registra cuotas de contribuciones no pagadas'.lower() in Alert(driver).text.lower():
                no_debt = True

            Alert(driver).accept()
        except:
            pass

        time.sleep(1)

        scrapped_commune = driver.find_elements_by_xpath(
            "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[1]")
        role = driver.find_elements_by_xpath(
            "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[2]")
        overdue_dates = driver.find_elements_by_xpath(
            "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[4]")
        expire_date = driver.find_elements_by_xpath(
            "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[6]")
        amount_in_time = driver.find_elements_by_xpath(
            "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[5]")
        total_amount = driver.find_elements_by_xpath(
            "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[7]")
        instalments_count = len(overdue_dates)

        if instalments_count == 0:
            if no_debt:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'SIN DEUDA'])
            else:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'SIN INFORMACION'])
        else:
            for instament_number in range(instalments_count):
                register = self.format_output(instament_number, scrapped_commune, role, overdue_dates, expire_date, amount_in_time, total_amount)
                output_data.append(register)
        return output_data

    def format_output(self, instalment_number, comune, role, overdue_dates, expire_date, amount_in_time, total_amount):
        comune = comune[instalment_number].text
        role = role[instalment_number].text
        overdue_dates = overdue_dates[instalment_number].text
        expire_date = expire_date[instalment_number].text
        amount_in_time = amount_in_time[instalment_number].text
        total_amount = total_amount[instalment_number].text
        return [comune, role, overdue_dates, expire_date, amount_in_time, total_amount]