import time
import pdb
import unicodedata
import logging
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


def normalize_text(text):
    """
    Normaliza texto para comparación agnóstica:
    - Elimina tildes (á→a, é→e, í→i, ó→o, ú→u, ñ→n)
    - Convierte a mayúsculas
    - Elimina espacios, guiones y caracteres especiales
    
    Ejemplos:
    - "Con-Con" → "CONCON"
    - "Concón" → "CONCON"
    - "Viña del Mar" → "VINADELMAR"
    - "REGIÓN METROPOLITANA" → "REGIONMETROPOLITANA"
    """
    if not text:
        return ""
    
    # Paso 1: Convertir a mayúsculas
    text = text.upper()
    
    # Paso 2: Eliminar tildes (descomposición NFD y filtrar marcas diacríticas)
    text = ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )
    
    # Paso 3: Eliminar espacios, guiones, puntos y caracteres especiales (solo alfanuméricos)
    text = ''.join(char for char in text if char.isalnum())
    
    return text


class Scrapper:
    def __init__(self, region, commune, rol_first, rol_second, driver=None):
        self.region = region
        self.commune = commune
        self.rol_first = rol_first
        self.rol_second = rol_second
        self.driver = driver
        self.owns_driver = False  # Flag para saber si debe cerrar el driver

    def scrap(self):
        region = self.region
        commune = self.commune
        rol_first = self.rol_first
        rol_second = self.rol_second
        output_data = []

        detalle_vigentes = False

        # Si no se pasó un driver, crear uno (modo legacy)
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
            self.owns_driver = True  # Este scrapper es dueño del driver y debe cerrarlo
        else:
            driver = self.driver  # Usar el driver compartido

        # Función para realizar todo el proceso de búsqueda y scraping
        def perform_search_and_scrap():
            logger.info(f"Procesando: Región={region}, Comuna={commune}, ROL={rol_first}-{rol_second}")
            
            driver.get('https://www4.sii.cl/cuotaanualbienesraicespubinternetui/#!/buscaRolPagos')
            
            # select region con normalización
            time.sleep(2)
            try:
                normalized_region = normalize_text(region)
                logger.info(f"Buscando región: '{region}' (normalizado: '{normalized_region}')")
                
                # Buscar la opción de región que coincida
                found = False
                region_options = driver.find_elements(By.XPATH, "//select[@ng-model='regionModel']/option")
                for option in region_options:
                    if normalize_text(option.text) == normalized_region:
                        option.click()
                        logger.info(f"Región seleccionada: {option.text}")
                        found = True
                        break
                
                if not found:
                    logger.warning(f"No se encontró coincidencia para región '{region}'")
                    output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR REGION: {}'.format(region)])
                    return None, None, None, None, None, None, None, None, None, None, None, True

            except Exception as e:
                logger.error(f"Error seleccionando región '{region}': {e}")
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR REGION: {}'.format(region)])
                return None, None, None, None, None, None, None, None, None, None, None, True

            # select commune con normalización
            time.sleep(2)  # Esperar a que el dropdown de comunas cargue
            try:
                commune_select = Select(driver.find_element(By.ID, 'codigo'))
                normalized_commune = normalize_text(commune)
                logger.info(f"Buscando comuna: '{commune}' (normalizado: '{normalized_commune}')")
                
                # Buscar la opción que coincida con la normalización
                found = False
                for option in commune_select.options:
                    if normalize_text(option.text) == normalized_commune:
                        commune_select.select_by_visible_text(option.text)
                        logger.info(f"Comuna seleccionada: {option.text}")
                        found = True
                        break
                
                if not found:
                    logger.warning(f"No se encontró coincidencia para comuna '{commune}'")
                    logger.info(f"Opciones disponibles: {[opt.text for opt in commune_select.options[:5]]}...")
                    output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR COMUNA'])
                    return None, None, None, None, None, None, None, None, None, None, None, True
                    
            except Exception as e:
                logger.error(f"Error seleccionando comuna '{commune}': {e}")
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ERROR COMUNA'])
                return None, None, None, None, None, None, None, None, None, None, None, True

            # set rol - IMPORTANTE: limpiar campos antes de escribir
            logger.info(f"Ingresando ROL: {rol_first}-{rol_second}")
            element = driver.find_element(By.ID, 'manzana')
            element.clear()  # Limpiar campo antes de escribir
            element.send_keys(rol_first)

            # set rol digit
            element = driver.find_element(By.ID, 'predio')
            element.clear()  # Limpiar campo antes de escribir
            element.send_keys(rol_second)

            # search
            driver.find_element(By.XPATH, '//button[text()="Buscar"]').click()
            logger.info("Búsqueda enviada, esperando respuesta...")

            # Esperar tiempo fijo para que carguen ambas tablas (morosas y vigentes)
            time.sleep(4)

            # Detectar alertas con textos EXACTOS del SII
            no_debt = False
            exempt = False
            auto_payment = False
            no_role = False
            
            try:
                alert = Alert(driver)
                alert_text = alert.text.lower()
                
                # Importante: el orden importa, verificar el texto más específico primero
                if alert_text == 'bien raíz no registra cuotas de contribuciones no pagadas. si ud. ha efectuado algún pago de contribuciones para este predio a través de internet sii, puede consultar los comprobantes de dichos pagos presionando el botón aceptar, en caso contrario presione cancelar':
                    no_debt = True
                    logger.info("Alerta detectada: SIN DEUDA")
                    alert.accept()
                elif alert_text == 'bien raíz no registra cuotas de contribuciones no pagadas.':
                    exempt = True
                    logger.info("Alerta detectada: EXENTO")
                    alert.accept()
                elif alert_text == 'la propiedad posee convenio de pago automático (pac) con tesorería general de la república, si desea continuar con el pago, entonces presione aceptar, en caso contrario, presione cancelar':
                    auto_payment = True
                    logger.info("Alerta detectada: PAGO AUTOMATICO (PAC)")
                    alert.accept()
                elif alert_text == 'no existe una propiedad asociada a este nro de rol de avalúo.':
                    no_role = True
                    logger.info("Alerta detectada: ROL NO EXISTE")
                    alert.accept()
                else:
                    logger.warning(f"Alerta desconocida: '{alert.text}'")
                    alert.accept()
            except:
                # No hay alerta
                pass

            time.sleep(1)

            # Scrapear los elementos de deudas morosas
            scrapped_commune = driver.find_elements(By.XPATH, "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[1]")
            role = driver.find_elements(By.XPATH, "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[2]")
            overdue_dates = driver.find_elements(By.XPATH, "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[4]")
            expire_date = driver.find_elements(By.XPATH, "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[6]")
            amount_in_time = driver.find_elements(By.XPATH, "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[5]")
            total_amount = driver.find_elements(By.XPATH, "//div[@ng-repeat='vencidas  in resultado']/table[@class='tabla']/tbody/tr/td[7]")
            vigentes = driver.find_elements(By.XPATH, "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']")
            
            cuotas_morosas = len(overdue_dates)
            cuotas_vigentes = len(vigentes)
            logger.info(f"Cuotas encontradas: {cuotas_morosas} morosas, {cuotas_vigentes} vigentes")
            
            return scrapped_commune, role, overdue_dates, expire_date, amount_in_time, total_amount, vigentes, no_debt, exempt, auto_payment, no_role, False

        # Primer intento de búsqueda y scrapeo
        scrapped_commune, role, overdue_dates, expire_date, amount_in_time, total_amount, vigentes, no_debt, exempt, auto_payment, no_role, has_error = perform_search_and_scrap()
        
        # Si hubo error, retornar inmediatamente (sin cerrar el driver compartido)
        if has_error:
            if self.owns_driver:
                driver.quit()
            return output_data
        
        instalments_count = len(overdue_dates)
        vigentes_count = len(vigentes)
        
        # Retry logic mejorado: casos sospechosos merecen más intentos
        # Caso sospechoso: No hay cuotas morosas Y no hay alertas claras
        # (sin importar si hay vigentes, porque la tabla de morosas pudo no cargar)
        is_suspicious = instalments_count == 0 and not (no_debt or auto_payment or no_role or exempt)
        max_retries = 2 if is_suspicious else 1
        retry_count = 0
        should_retry = instalments_count == 0 and not (no_debt or auto_payment or no_role)
        
        while should_retry and retry_count < max_retries:
            retry_count += 1
            logger.warning(f"Reintento {retry_count}/{max_retries} - Sin cuotas morosas y sin alertas claras, recargando página...")
            scrapped_commune, role, overdue_dates, expire_date, amount_in_time, total_amount, vigentes, no_debt, exempt, auto_payment, no_role, has_error = perform_search_and_scrap()
            
            if has_error:
                break
                
            instalments_count = len(overdue_dates)
            vigentes_count = len(vigentes)
            should_retry = instalments_count == 0 and not (no_debt or auto_payment or no_role)
        
        active_instalments_count = None

        if detalle_vigentes:
            vigentes_commune = driver.find_elements(By.XPATH, "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[1]")
            vigentes_role = driver.find_elements(By.XPATH, "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[2]")
            vigentes_dates = driver.find_elements(By.XPATH, "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[5]")
            vigentes_expire_date = driver.find_elements(By.XPATH, "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[7]")
            vigentes_amount_in_time = driver.find_elements(By.XPATH, "//div[@ng-repeat='vigentes  in resultado']/div/table[@class='tabla']/tbody/tr/td[9]")
            active_instalments_count = len(vigentes_dates)
            vigentes_total_amount_state = ['VIGENTE'] * active_instalments_count #Se usará para definir el estado

        if instalments_count == 0:
            if vigentes:
                if detalle_vigentes and active_instalments_count:
                    for active_instalment_number in range(active_instalments_count):
                        register = self.format_output(active_instalment_number, vigentes_commune, vigentes_role, vigentes_dates, vigentes_expire_date, vigentes_amount_in_time, vigentes_total_amount_state)
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
            elif no_role:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'ROL NO EXISTE'])
            else:
                output_data.append([commune, '{}-{}'.format(rol_first, rol_second), 'SIN INFORMACION'])
        else:
            if detalle_vigentes and active_instalments_count:
                for active_instalment_number in range(active_instalments_count):
                        register = self.format_output(active_instalment_number, vigentes_commune, vigentes_role, vigentes_dates, vigentes_expire_date, vigentes_amount_in_time, vigentes_total_amount_state)
                        output_data.append(register)
                return output_data
            else:
                for instalment_number in range(instalments_count):
                    register = self.format_output(instalment_number, scrapped_commune, role, overdue_dates, expire_date, amount_in_time, total_amount)
                    output_data.append(register)
        
        # Solo cerrar el driver si este scrapper lo creó
        if self.owns_driver:
            driver.quit()
        
        return output_data

    def format_output(self, instalment_number, comune, role, overdue_dates, expire_date, amount_in_time, total_amount):
        comune = comune[instalment_number].text
        role = role[instalment_number].text
        overdue_dates = overdue_dates[instalment_number].text
        expire_date = expire_date[instalment_number].text
        amount_in_time = amount_in_time[instalment_number].text
        total_amount =  total_amount[instalment_number] if total_amount[0] == 'VIGENTE' else total_amount[instalment_number].text 
        return [comune, role, overdue_dates, expire_date, amount_in_time, total_amount]