import unidecode


class LocationHelper:

    def __init__(self):
        self.locations = {
            "name": "Chile",
            "regions": [
                {
                    "name": "Arica y Parinacota",
                    "romanNumber": "XV",
                    "number": "15",
                    "communes": [
                        {"name": "Arica"},
                        {"name": "Camarones"},
                        {"name": "General Lagos"},
                        {"name": "Putre"}
                    ]
                },
                {
                    "name": "Tarapacá",
                    "romanNumber": "I",
                    "number": "1",
                    "communes": [
                        {"name": "Alto Hospicio"},
                        {"name": "Camiña"},
                        {"name": "Colchane"},
                        {"name": "Huara"},
                        {"name": "Iquique"},
                        {"name": "Pica"},
                        {"name": "Pozo Almonte"}
                    ]
                },
                {
                    "name": "Antofagasta",
                    "romanNumber": "II",
                    "number": "2",
                    "communes": [
                        {"name": "Antofagasta"},
                        {"name": "Calama"},
                        {"name": "María Elena"},
                        {"name": "Mejillones"},
                        {"name": "Ollagüe"},
                        {"name": "San Pedro de Atacama"},
                        {"name": "Sierra Gorda"},
                        {"name": "Taltal"},
                        {"name": "Tocopilla"}
                    ]
                },
                {
                    "name": "Atacama",
                    "romanNumber": "III",
                    "number": "3",
                    "communes": [
                        {"name": "Alto del Carmen"},
                        {"name": "Caldera"},
                        {"name": "Chañaral"},
                        {"name": "Copiapó"},
                        {"name": "Diego de Almagro"},
                        {"name": "Freirina"},
                        {"name": "Huasco"},
                        {"name": "Tierra Amarilla"},
                        {"name": "Vallenar"}
                    ]
                },
                {
                    "name": "Coquimbo",
                    "romanNumber": "IV",
                    "number": "4",
                    "communes": [
                        {"name": "Andacollo"},
                        {"name": "Canela"},
                        {"name": "Combarbalá"},
                        {"name": "Coquimbo"},
                        {"name": "Illapel"},
                        {"name": "La Higuera"},
                        {"name": "La Serena"},
                        {"name": "Los Vilos"},
                        {"name": "Monte Patria"},
                        {"name": "Ovalle"},
                        {"name": "Paiguano"},
                        {"name": "Punitaqui"},
                        {"name": "Río Hurtado"},
                        {"name": "Salamanca"},
                        {"name": "Vicuña"}
                    ]
                },
                {
                    "name": "Valparaiso",
                    "romanNumber": "V",
                    "number": "5",
                    "communes": [
                        {"name": "Algarrobo"},
                        {"name": "Cabildo"},
                        {"name": "Calera"},
                        {"name": "Calle Larga"},
                        {"name": "Cartagena"},
                        {"name": "Casablanca"},
                        {"name": "Catemu"},
                        {"name": "Con - cón"},
                        {"name": "El Quisco"},
                        {"name": "El Tabo"},
                        {"name": "Hijuelas"},
                        {"name": "Isla de Pascua"},
                        {"name": "Juan Fernández"},
                        {"name": "La Cruz"},
                        {"name": "La Ligua"},
                        {"name": "Limache"},
                        {"name": "Llaillay"},
                        {"name": "Los Andes"},
                        {"name": "Nogales"},
                        {"name": "Olmué"},
                        {"name": "Panquehue"},
                        {"name": "Papudo"},
                        {"name": "Petorca"},
                        {"name": "Puchuncavi"},
                        {"name": "Putaendo"},
                        {"name": "Quillota"},
                        {"name": "Quilpué"},
                        {"name": "Quintero"},
                        {"name": "Rinconada"},
                        {"name": "San Antonio"},
                        {"name": "San Esteban"},
                        {"name": "San Felipe"},
                        {"name": "Santa Maria"},
                        {"name": "Santo Domingo"},
                        {"name": "Valparaiso"},
                        {"name": "Villa Alemana"},
                        {"name": "Viña del Mar"},
                        {"name": "Zapallar"}
                    ]
                },
                {
                    "name": "Metropolitana de Santiago",
                    "romanNumber": "XIII",
                    "number": "13",
                    "communes": [
                        {"name": "Alhué"},
                        {"name": "Buin"},
                        {"name": "Calera de Tango"},
                        {"name": "Cerrillos"},
                        {"name": "Cerro Navia"},
                        {"name": "Colina"},
                        {"name": "Conchalí"},
                        {"name": "Curacaví"},
                        {"name": "El Bosque"},
                        {"name": "El Monte"},
                        {"name": "Estación Central"},
                        {"name": "Huechuraba"},
                        {"name": "Independencia"},
                        {"name": "Isla de Maipo"},
                        {"name": "La Cisterna"},
                        {"name": "La Florida"},
                        {"name": "La Granja"},
                        {"name": "La Pintana"},
                        {"name": "La Reina"},
                        {"name": "Lampa"},
                        {"name": "Las Condes"},
                        {"name": "Lo Barnechea"},
                        {"name": "Lo Espejo"},
                        {"name": "Lo Prado"},
                        {"name": "Macul"},
                        {"name": "Maipú"},
                        {"name": "María Pinto"},
                        {"name": "Melipilla"},
                        {"name": "ñuñoa"},
                        {"name": "Padre Hurtado"},
                        {"name": "Paine"},
                        {"name": "Pedro Aguirre Cerda"},
                        {"name": "Peñaflor"},
                        {"name": "Peñalolén"},
                        {"name": "Pirque"},
                        {"name": "Providencia"},
                        {"name": "Pudahuel"},
                        {"name": "Puente Alto"},
                        {"name": "Quilicura"},
                        {"name": "Quinta Normal"},
                        {"name": "Recoleta"},
                        {"name": "Renca"},
                        {"name": "San Bernardo"},
                        {"name": "San Joaquín"},
                        {"name": "San José Maipo"},
                        {"name": "San Miguel"},
                        {"name": "San Pedro"},
                        {"name": "San Ramón"},
                        {"name": "Santiago"},
                        {"name": "Talagante"},
                        {"name": "Til til"},
                        {"name": "Vitacura"}
                    ]
                },
                {
                    "name": "Libertador Bernardo O'Higgins",
                    "romanNumber": "VI",
                    "number": "6",
                    "communes": [
                        {"name": "Chimbarongo"},
                        {"name": "Chépica"},
                        {"name": "Codegua"},
                        {"name": "Coinco"},
                        {"name": "Coltauco"},
                        {"name": "Doñihue"},
                        {"name": "Graneros"},
                        {"name": "La Estrella"},
                        {"name": "Las Cabras"},
                        {"name": "Litueche"},
                        {"name": "Lolol"},
                        {"name": "Machalí"},
                        {"name": "Malloa"},
                        {"name": "Marchihue"},
                        {"name": "Nancagua"},
                        {"name": "Navidad"},
                        {"name": "Olivar"},
                        {"name": "Palmilla"},
                        {"name": "Paredones"},
                        {"name": "Peralillo"},
                        {"name": "Peumo"},
                        {"name": "Pichidegua"},
                        {"name": "Pichilemu"},
                        {"name": "Placilla"},
                        {"name": "Pumanque"},
                        {"name": "Quinta de Tilcoco"},
                        {"name": "Rancagua"},
                        {"name": "Rengo"},
                        {"name": "Requínoa"},
                        {"name": "San Fernando"},
                        {"name": "SN. FCO. DE MOSTAZAL"},
                        {"name": "San Vicente"},
                        {"name": "Santa Cruz"}
                    ]
                },
                {
                    "name": "Maule",
                    "romanNumber": "VII",
                    "number": "7",
                    "communes": [
                        {"name": "Cauquenes"},
                        {"name": "Chanco"},
                        {"name": "Colbún"},
                        {"name": "Constitución"},
                        {"name": "Curepto"},
                        {"name": "Curicó"},
                        {"name": "Empedrado"},
                        {"name": "Hualañé"},
                        {"name": "Licantén"},
                        {"name": "Linares"},
                        {"name": "Longaví"},
                        {"name": "Maule"},
                        {"name": "Molina"},
                        {"name": "Parral"},
                        {"name": "Pelarco"},
                        {"name": "Pelluhue"},
                        {"name": "Pencahue"},
                        {"name": "Rauco"},
                        {"name": "Retiro"},
                        {"name": "Romeral"},
                        {"name": "Río Claro"},
                        {"name": "Sagrada Familia"},
                        {"name": "San Clemente"},
                        {"name": "San Javier"},
                        {"name": "San Rafael"},
                        {"name": "Talca"},
                        {"name": "Teno"},
                        {"name": "Vichuquén"},
                        {"name": "Villa Alegre"},
                        {"name": "Yerbas Buenas"}
                    ]
                },
                {
                    "name": "Ñuble",
                    "romanNumber": "XVI",
                    "number": "16",
                    "communes": [
                        {"name": "Bulnes"},
                        {"name": "Chillán Viejo"},
                        {"name": "Chillán"},
                        {"name": "Cobquecura"},
                        {"name": "Coelemu"},
                        {"name": "Coihueco"},
                        {"name": "El Carmen"},
                        {"name": "Ninhue"},
                        {"name": "Ñiquén"},
                        {"name": "Pemuco"},
                        {"name": "Pinto"},
                        {"name": "Portezuelo"},
                        {"name": "Quillón"},
                        {"name": "Quirihue"},
                        {"name": "Ránquil"},
                        {"name": "San Carlos"},
                        {"name": "San Fabián"},
                        {"name": "San Ignacio"},
                        {"name": "San Nicolás"},
                        {"name": "Treguaco"},
                        {"name": "Yungay"}
                    ]
                },
                {
                    "name": "Bio bio",
                    "romanNumber": "VIII",
                    "number": "8",
                    "communes": [
                        {"name": "Alto Biobío"},
                        {"name": "Antuco"},
                        {"name": "Arauco"},
                        {"name": "Cabrero"},
                        {"name": "Cañete"},
                        {"name": "Chiguayante"},
                        {"name": "Concepción"},
                        {"name": "Contulmo"},
                        {"name": "Coronel"},
                        {"name": "Curanilahue"},
                        {"name": "Florida"},
                        {"name": "Hualpén"},
                        {"name": "Hualqui"},
                        {"name": "Laja"},
                        {"name": "Lebu"},
                        {"name": "Los Álamos"},
                        {"name": "Los Ángeles"},
                        {"name": "Lota"},
                        {"name": "Mulchén"},
                        {"name": "Nacimiento"},
                        {"name": "Negrete"},
                        {"name": "Penco"},
                        {"name": "Quilaco"},
                        {"name": "Quilleco"},
                        {"name": "San Pedro de la Paz"},
                        {"name": "San Rosendo"},
                        {"name": "Santa Bárbara"},
                        {"name": "Santa Juana"},
                        {"name": "Talcahuano"},
                        {"name": "Tirúa"},
                        {"name": "Tomé"},
                        {"name": "Tucapel"},
                        {"name": "Yumbel"}
                    ]
                },
                {
                    "name": "Araucania",
                    "romanNumber": "IX",
                    "number": "9",
                    "communes": [
                        {"name": "Angol"},
                        {"name": "Carahue"},
                        {"name": "Cholchol"},
                        {"name": "Collipulli"},
                        {"name": "Cunco"},
                        {"name": "Curacautín"},
                        {"name": "Curarrehue"},
                        {"name": "Ercilla"},
                        {"name": "Freire"},
                        {"name": "Galvarino"},
                        {"name": "Gorbea"},
                        {"name": "Lautaro"},
                        {"name": "Loncoche"},
                        {"name": "Lonquimay"},
                        {"name": "Los Sauces"},
                        {"name": "Lumaco"},
                        {"name": "Melipeuco"},
                        {"name": "Nueva Imperial"},
                        {"name": "Padre las Casas"},
                        {"name": "Perquenco"},
                        {"name": "Pitrufquén"},
                        {"name": "Pucón"},
                        {"name": "Purén"},
                        {"name": "Renaico"},
                        {"name": "Saavedra"},
                        {"name": "Temuco"},
                        {"name": "Teodoro Schmidt"},
                        {"name": "Toltén"},
                        {"name": "Traiguén"},
                        {"name": "Victoria"},
                        {"name": "Vilcún"},
                        {"name": "Villarrica"}
                    ]
                },
                {
                    "name": "Los Ríos",
                    "romanNumber": "XIV",
                    "number": "14",
                    "communes": [
                        {"name": "Corral"},
                        {"name": "Futrono"},
                        {"name": "La Unión"},
                        {"name": "Lago Ranco"},
                        {"name": "Lanco"},
                        {"name": "Los Lagos"},
                        {"name": "Mariquina"},
                        {"name": "Máfil"},
                        {"name": "Paillaco"},
                        {"name": "Panguipulli"},
                        {"name": "Río Bueno"},
                        {"name": "Valdivia"}
                    ]
                },
                {
                    "name": "Los Lagos",
                    "romanNumber": "X",
                    "number": "10",
                    "communes": [
                        {"name": "Ancud"},
                        {"name": "Calbuco"},
                        {"name": "Castro"},
                        {"name": "Chaitén"},
                        {"name": "Chonchi"},
                        {"name": "Cochamó"},
                        {"name": "Curaco de Vélez"},
                        {"name": "Dalcahue"},
                        {"name": "Fresia"},
                        {"name": "Frutillar"},
                        {"name": "Futaleufú"},
                        {"name": "Hualaihué"},
                        {"name": "Llanquihue"},
                        {"name": "Los Muermos"},
                        {"name": "Maullín"},
                        {"name": "Osorno"},
                        {"name": "Palena"},
                        {"name": "Puerto Montt"},
                        {"name": "Puerto Octay"},
                        {"name": "Puerto Varas"},
                        {"name": "Puqueldón"},
                        {"name": "Purranque"},
                        {"name": "Puyehue"},
                        {"name": "Queilén"},
                        {"name": "Quellón"},
                        {"name": "Quemchi"},
                        {"name": "Quinchao"},
                        {"name": "Río Negro"},
                        {"name": "San Juan de la Costa"},
                        {"name": "San Pablo"}
                    ]
                },
                {
                    "name": "Aysén del General Carlos Ibáñez del Campo",
                    "romanNumber": "XI",
                    "number": "11",
                    "communes": [
                        {"name": "Aysén"},
                        {"name": "Chile Chico"},
                        {"name": "Cisnes"},
                        {"name": "Cochrane"},
                        {"name": "Coyhaique"},
                        {"name": "Guaitecas"},
                        {"name": "Lago Verde"},
                        {"name": "O’Higgins"},
                        {"name": "Río Ibáñez"},
                        {"name": "Tortel"}
                    ]
                },
                {
                    "name": "Magallanes y de la Antártica Chilena",
                    "romanNumber": "XII",
                    "number": "12",
                    "communes": [
                        {"name": "Antártica"},
                        {"name": "Cabo de Hornos (Ex Navarino)"},
                        {"name": "Laguna Blanca"},
                        {"name": "Natales"},
                        {"name": "Porvenir"},
                        {"name": "Primavera"},
                        {"name": "Punta Arenas"},
                        {"name": "Río Verde"},
                        {"name": "San Gregorio"},
                        {"name": "Timaukel"},
                        {"name": "Torres del Paine"}
                    ]
                }
            ]
        }
        self.prepositions = {'DE': ['Arica y Parinacota',
                                    'Tarapacá',
                                    'Antofagasta',
                                    'Atacama',
                                    'Coquimbo',
                                    'Valparaiso',
                                    'Ñuble',
                                    'Los Ríos',
                                    'Los Lagos',
                                    'Aysén del General Carlos Ibáñez del Campo'
                                    ],
                             'DEL': ["Libertador Bernardo O'Higgins", 'Maule', 'Bio bio'],
                             'DE LA': ['Araucania'],
                             'FALSE': ['Metropolitana de Santiago']}

    def get_region(self, input_commune):
        regions = self.locations['regions']
        for region in regions:
            communes = region['communes']
            for commune in communes:
                data_commune = unidecode.unidecode(commune['name'])
                input_comune = unidecode.unidecode(input_commune)
                if input_comune.lower() == data_commune.lower():
                    return region['name'].upper()
        return 'Not Found {}'.format(input_commune)

    def solve_region(self, region):
        for preposition in self.prepositions:
            for region_iterator in self.prepositions[preposition]:
                if region.lower() == region_iterator.lower():
                    if preposition == 'FALSE':
                        return 'REGION {}'.format(region)
                    else:
                        return 'REGION {} {}'.format(preposition, region)

    def translate_commune(self, commune):
        communes_translate = {'PUCON': 'PUCÓN',
                              'NUNOA': 'ÑUÑOA',
                              'CURACAVI': 'CURACAVÍ',
                              'CONCEPCION': 'CONCEPCIÓN',
                              'CONCON': 'CONCÓN'}
        if commune in communes_translate.keys():
            return communes_translate[commune]
        else:
            return commune
