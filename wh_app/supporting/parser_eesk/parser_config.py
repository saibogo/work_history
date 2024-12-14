url_eesk = "https://eesk.ru/upload/site1/info_shutdown.xlsm"
url_eens = "https://www.eens.ru/api/home/PhonosWithDate?dateTime"

street_patterns = ['Малышева', 'Ленина', 'Вайнера', 'Либкнехта', 'Карла', 'Калиновский', 'Луначарского', 'Исеть',
                   'Культуры', 'Морозный']
objects_patterns = ['4317', '1001', '1018']
adress_patterns = ['62/2']

separated = "========"

pattern_list = list(set(street_patterns) | set(objects_patterns) | set(adress_patterns))

