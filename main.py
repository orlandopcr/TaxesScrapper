from process_input import Reader
from helpers.location_herper import LocationHelper

# Número de workers paralelos (ajusta según tu necesidad)
# Recomendado: 2-3 workers para empezar y evitar rate limiting del SII
MAX_WORKERS = 7

reader = Reader('data.xls', max_workers=MAX_WORKERS)
reader.read()