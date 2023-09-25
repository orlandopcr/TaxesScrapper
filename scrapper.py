import time
import pdb
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


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

        detalle_vigentes = False
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        service = Service(executable_path='/Users/orlando/Dev/Playground/cobanc/scrapper/webdriver/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get('https://www4.sii.cl/cuotaanualbienesraicespubinternetui/#!/buscaRolPagos')
        # select region
        time.sleep(1)
        try:
            #pdb.set_trace()
            if region == "REGION DEL LIBERTADOR BERNARDO O'HIGGINS":
                region_select = "//select[@ng-model='regionModel']/option[contains(text(), 'BERNARDO')]"
            elif region == "REGION DE AYSÉN DEL GENERAL CARLOS IBÁÑEZ DEL CAMPO":
                region_select = "//select[@ng-model='regionModel']/option[contains(text(), 'DEL CAMPO')]"
            else:
                region_select = "//select[@ng-model='regionModel']/option[text()='" + region + "']"
            driver.find_element("xpath", region_select).click()

        except:
            output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR REGION: {}'.format(region)])
            return output_data
        time.sleep(1)

        # select commune
        try:
            select = Select(driver.find_element('id', 'codigo'))
            select.select_by_visible_text(commune)
        except:
            output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR COMUNA'])
            return output_data


        # set rol

        element = driver.find_element("id", 'manzana')
        element.send_keys(rol_first)

        # set rol digit
        element = driver.find_element("id", 'predio')
        element.send_keys(rol_second)

        #search
        driver.find_element("xpath", '//button[text()="Buscar"]').click()

        #search
        time.sleep(1)

        no_debt = False
        exempt = False
        auto_payment = False
        try:
            if 'Bien Raíz no registra cuotas de contribuciones no pagadas.'.lower() == Alert(driver).text.lower():
                exempt = True
                Alert(driver).accept()
            if 'bien raíz no registra cuotas de contribuciones no pagadas. si ud. ha efectuado algún pago de contribuciones para este predio a través de internet sii, puede consultar los comprobantes de dichos pagos presionando el botón aceptar, en caso contrario presione cancelar' == Alert(driver).text.lower():
                no_debt = True
                Alert(driver).accept()
            if 'La propiedad posee convenio de pago automático (PAC) con Tesorería General de la República, Si desea continuar con el pago, entonces presione Aceptar, en caso contrario, presione Cancelar'.lower() == Alert(driver).text.lower():
                auto_payment = True
                Alert(driver).accept()
            else:
                Alert(driver).accept()
        except:
            pass

        time.sleep(1)

        scrapped_commune = driver.find_elements('xpath', "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[1]")
        role = driver.find_elements('xpath', "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[2]")
        overdue_dates = driver.find_elements('xpath', "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[4]")
        expire_date = driver.find_elements('xpath', "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[6]")
        amount_in_time = driver.find_elements('xpath', "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[5]")
        total_amount = driver.find_elements('xpath', "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[7]")
        vigentes = driver.find_elements('xpath', "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']")
        instalments_count = len(overdue_dates)
        active_instalments_count = None

        if detalle_vigentes:
            vigentes_commune = driver.find_elements('xpath', "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[1]")
            vigentes_role = driver.find_elements('xpath', "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[2]")
            vigentes_dates = driver.find_elements('xpath', "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[5]")
            vigentes_expire_date = driver.find_elements('xpath', "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[7]")
            vigentes_amount_in_time = driver.find_elements('xpath', "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[9]")
            active_instalments_count = len(vigentes_dates)
            vigentes_total_amount_state = ['VIGENTE'] * active_instalments_count #Se usará para definir el estado

        if instalments_count == 0:
            if vigentes:
                if detalle_vigentes and active_instalments_count:
                    for active_instament_number in range(active_instalments_count):
                        register = self.format_output(active_instament_number, vigentes_commune, vigentes_role, vigentes_dates, vigentes_expire_date, vigentes_amount_in_time, vigentes_total_amount_state)
                        output_data.append(register)
                    return output_data
                else:
                    output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'SIN DEUDA (CUOTAS VIGENTES)'])
            elif no_debt:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'SIN DEUDA'])
            elif exempt:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'REVISAR EXENTO'])
            elif auto_payment:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'PAGO AUTOMATICO'])
            else:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'SIN INFORMACION'])
        else:
            if detalle_vigentes and active_instalments_count:
                for active_instament_number in range(active_instalments_count):
                        register = self.format_output(active_instament_number, vigentes_commune, vigentes_role, vigentes_dates, vigentes_expire_date, vigentes_amount_in_time, vigentes_total_amount_state)
                        output_data.append(register)
                return output_data
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
        total_amount =  total_amount[instalment_number] if total_amount[0] == 'VIGENTE' else total_amount[instalment_number].text 
        return [comune, role, overdue_dates, expire_date, amount_in_time, total_amount]