import os
import twitter
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter']

api = twitter.Api(consumer_key=os.environ['consumer_key'],
                  consumer_secret=os.environ['consumer_secret'],
                  access_token_key=os.environ['access_token'],
                  access_token_secret=os.environ['access_token_secret'])


accounts = [
    'VickyDavilaH',
    'PosconflictoCO',
    'SenadoGovCo',
    'FiscaliaCol',
    'CamaraColombia',
    'Rodrigo_Lara_',
    'JuanLozano_R',
    'CConstitucional',
    'alejogiral',
    'infopresidencia',
    'PoliciaColombia',
    'COL_EJERCITO',
    'mindefensa',
    'TimoFARC',
    'FARC_EPueblo',
    'AlvaroUribeVel',
    'NTN24',
    'ELTIEMPO',
    'elespectador',
    'NoticiasRCN',
    'NoticiasCaracol',
    'Registraduria',
    'lafm',
    'rcnradio',
    'JuanManSantos',
    'CaracolTV',
    'LaNocheNTN24',
    'CGurisattiNTN24',
    'PrensaRural',
    'VocesDePazCo',
    'WRadioColombia',
    'Carlozada_FARC',
    'ComisionadoPaz',
    'SandraFARC',
    'ELN_RANPAL_COL',
    'AlapePastorFARC',
    'ClaudiaLopez',
    'lasillavacia',
    'urnadecristal',
    'petrogustavo',
    'PartidoLiberal',
    'DeLaCalleHum',
    'partidodelaucol',
    'soyconservador',
    'PCambioRadical',
    'CeDemocratico',
    'OIZuluaga',
    'mluciaramirez',
    'CarlosHolmesTru',
    'ClaraLopezObre',
    'PoloDemocratico',
    'IvanCepedaCast',
    'piedadcordoba',
    'PGN_COL',
    'BluRadioCo',
    'CMILANOTICIA',
    'A_OrdonezM',
    'RevistaSemana',
    'jcgalindovacha',
    'moecolombia',
    'CNE_COLOMBIA',
    'PartidoVerdeCoL',
    'EnriquePenalosa',
    'Citytv',
    'Colombiareclama',
    'CancerColombia',
    'COLNoCorrupcion',
    'CamPatColombia',
    'vanguardiacom',
    'GobiernoLimpio',
    'AndresPastrana_',
    'ernestosamperp',
    'HoracioSerpa',
    'CristoBustos',
    'German_Vargas',
    'carlosfgalan',
    'RafaelPardo',
    'RenovacionCo',
    'EquipoPazGob',
    'CNNEE',
    'el_pais',
    'bbcmundo',
    'RestrepoJCamilo',
    'ceballosarevalo',
    'NestorMoralesC',
    'Rodrigo_Rivera',
    'ELN_Paz',
    'ideaspaz',
    'FARC_EPaz',
    'AABenedetti',
    'charoguerra',
    'PalomaValenciaL',
    'IvanDuque',
    'RafaNietoLoaiza',
    'IvanMarquezFARC',
    'JERobledo',
    'RoyBarreras',
    'AidaAvellaE',
    'sergio_fajardo',
    'juanmanuelgalan',
    'PizonBueno',
    'VotareEnBlanco',
    'PosconflictoCO',
    'CesarGaviriaT',
    'Mineducacion',
    'mindefensa',
    'MinMinas',
    'MintrabajoCol',
    'fecode',
    'piedadcordoba',
    'ClaraLopezObre',
    'ManosLimpiasCo'
]

for account in accounts:
    try:
        user = api.GetUser(screen_name=account)
        data_user = {}
        data_user['created_at'] = user.created_at
        data_user['description'] = user.description
        data_user['favourites_count'] = user.favourites_count
        data_user['followers_count'] = user.followers_count
        data_user['friends_count'] = user.friends_count
        data_user['name'] = user.name
        data_user['screen_name'] = user.screen_name
        result = db.accounts.insert_one(data_user)
    except:
        pass
