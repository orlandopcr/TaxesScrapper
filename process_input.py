import xlrd
import pdb
from selenium import webdriver
from helpers.location_herper import LocationHelper
from scrapper import Scrapper
from process_output import Writer
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import logging
import os
from datetime import datetime


class Reader:
    def __init__(self, filename, max_workers=3):
        self.filename = filename
        self.max_workers = max_workers
        self.progress_lock = Lock()  # Protege el contador de progreso
        self.completed_count = 0
        self.total_count = 0
        
        # Crear directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)
        
        # Configurar logging con timestamp en el nombre
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'logs/scrapper_{timestamp}.log'
        
        # Configurar el logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [Worker-%(thread)d] - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Iniciando procesamiento con {max_workers} workers")
        print(f"📄 Log file: {log_filename}\n")

    def update_progress(self):
        """Actualiza y muestra el progreso en consola"""
        with self.progress_lock:
            self.completed_count += 1
            percentage = (self.completed_count / self.total_count) * 100
            print(f"\r🔄 Progreso: {self.completed_count}/{self.total_count} ({percentage:.1f}%) completados", end='', flush=True)
            if self.completed_count == self.total_count:
                print()  # Nueva línea al final

    def process_row(self, row_data):
        """Procesa una fila individual del Excel"""
        index, rol_first, rol_second, raw_commune = row_data
        
        self.logger.info(f"[Fila {index+1}] Iniciando: {raw_commune} {rol_first}-{rol_second}")
        
        try:
            commune = LocationHelper().translate_commune(raw_commune)
            raw_region = LocationHelper().get_region(commune)
            region = LocationHelper().solve_region(raw_region)
            
            self.logger.info(f"[Fila {index+1}] Región: {region}, Comuna: {commune}")
            
            # Crear un driver para este worker (cada thread tiene su propio navegador)
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
            
            try:
                scrapper = Scrapper(region=region, commune=commune, rol_first=rol_first, rol_second=rol_second, driver=driver)
                data = scrapper.scrap()
                
                self.logger.info(f"[Fila {index+1}] ✅ Completado exitosamente: {commune} {rol_first}-{rol_second}")
                self.update_progress()
                
                return {
                    'index': index,
                    'region': region,
                    'commune': commune,
                    'rol_first': rol_first,
                    'rol_second': rol_second,
                    'data': data,
                    'success': True
                }
            finally:
                driver.quit()
                self.logger.debug(f"[Fila {index+1}] Driver cerrado")
                
        except Exception as e:
            self.logger.error(f"[Fila {index+1}] ❌ Error en {raw_commune} {rol_first}-{rol_second}: {str(e)}", exc_info=True)
            self.update_progress()
            
            return {
                'index': index,
                'region': '',
                'commune': raw_commune,
                'rol_first': rol_first,
                'rol_second': rol_second,
                'data': [[raw_commune, f'{rol_first}-{rol_second}', 'SCRAPPING ERROR']],
                'success': False
            }

    def read(self):
        first_line = True
        location = ('data/{}'.format(self.filename))
        workbook = xlrd.open_workbook(location)
        sheet = workbook.sheet_by_index(0)
        
        # Preparar todas las filas para procesar
        rows_to_process = []
        index = 0
        
        for line in sheet:
            if first_line:
                first_line = False
                continue
            
            rol_first, rol_second = line[0].value.strip().split('-')
            raw_commune = line[1].value.upper().strip()
            rows_to_process.append((index, rol_first, rol_second, raw_commune))
            index += 1
        
        self.total_count = len(rows_to_process)
        self.logger.info(f"Total de propiedades a procesar: {self.total_count}")
        
        print(f"🚀 Procesando {self.total_count} propiedades con {self.max_workers} workers...\n")
        
        # Procesar en paralelo
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Enviar todas las tareas
            future_to_row = {executor.submit(self.process_row, row): row for row in rows_to_process}
            
            # Recoger resultados a medida que se completan
            for future in as_completed(future_to_row):
                result = future.result()
                results.append(result)
        
        print()  # Nueva línea después del progreso
        self.logger.info(f"Procesamiento completado: {len(results)} resultados")
        
        # Ordenar resultados por índice original para mantener el orden
        results.sort(key=lambda x: x['index'])
        
        print(f"\n✅ Procesamiento completado. Escribiendo {len(results)} resultados...\n")
        
        # Escribir todos los resultados en una sola operación
        from openpyxl import load_workbook
        wb = load_workbook("data/output.xlsx")
        ws = wb.worksheets[0]
        
        for idx, result in enumerate(results, 1):
            try:
                writer = Writer(result['data'])
                # Usar el método interno de formateo sin guardar
                if result['data'] is None:
                    ws.append([result['commune'], f"{result['rol_first']}-{result['rol_second']}", 'SIN INFORMACION'])
                else:
                    try:
                        ws.append(writer.format_output(result['data']))
                    except:
                        ws.append([result['data'][0], result['data'][1], 'ERROR ESCRITURA'])
                
                if idx % 10 == 0:
                    self.logger.info(f"Escritas {idx}/{len(results)} filas en Excel")
            except Exception as e:
                error_msg = f"Error escribiendo resultado {idx}: {str(e)}"
                print(f"❌ {error_msg}")
                self.logger.error(error_msg, exc_info=True)
        
        # Guardar una sola vez al final
        wb.save("data/output.xlsx")
        self.logger.info(f"Archivo guardado: data/output.xlsx con {len(results)} resultados")
        print(f"💾 Archivo guardado: data/output.xlsx con {len(results)} resultados\n")

    def solve_region(self, region):
        {}