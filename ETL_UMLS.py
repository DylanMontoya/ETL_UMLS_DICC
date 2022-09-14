import mysql.connector
import pandas as pd
import pickle

#%% Conexion DataBase
<<<<<<< HEAD

conn = mysql.connector.connect(user = 'root', 
                                    password = '', 
                                    host = 'localhost',
                port = '3306',
                                    db = 'snomed_spa')

if conn:
    print('Conectado  correctamente')

#%%
""" Extraccion y Transformacion de datos
                1ER METODO """
                
                
""" Columnas de MRCONSO -> 'CUI','LAT','TS','LUI','STT','SUI','ISPREF',
                                'AUI','SAUI','SCUI','SDUI','SAB','TTY','CODE',
                                'STR','SRL','SUPPRESS','CVF' """
concept = conn.cursor()
concept.execute("SELECT * FROM mrconso")

r1 = concept.fetchall()

mrconso = pd.DataFrame(r1)
mrconso.columns = ['CUI','LAT','TS','LUI','STT','SUI','ISPREF',
                   'AUI','SAUI','SCUI','SDUI','SAB','TTY','CODE',
                   'STR','SRL','SUPPRESS','CVF']

with open('mrconso.pkl', 'wb') as file:
    pickle.dump(mrconso, file)

""" Columnas de MRSTY -> 'CUI','TUI','STN','STY','ATUI','CVF'  """

semantic_type = conn.cursor()
semantic_type.execute("SELECT * FROM mrsty")

r2 = semantic_type.fetchall()

mrsty = pd.DataFrame(r2)
mrsty.columns = ['CUI','TUI','STN','STY','ATUI','CVF']

with open('mrsty.pkl', 'wb') as file:
    pickle.dump(mrsty, file)

#%%
# Cargo archivos de las tablas a usar
# Dejo columnas a usar
    
with open('mrconso.pkl', 'rb') as file:
    mrconso = pickle.load(file)
    
with open('mrsty.pkl', 'rb') as file:
    mrsty = pickle.load(file)
##### Termino de procesar lo que necesito

mrconso = mrconso[['CUI', 'STR']]

mrsty = mrsty[['CUI', 'TUI', 'STY']]

# Preprocesamiento de texto para mrconso -> STR

mrconso['STR'] = mrconso['STR'].str.lower()

a,b = 'áéíóúüñÁÉÍÓÚÜ','aeiouunAEIOUU'
trans = str.maketrans(a,b)

mrconso['STR'] = mrconso['STR'].str.translate(trans)

# Preprocesamiento de texto para mrconso -> STR

mrsty['STY'] = mrsty['STY'].str.lower()

with open('new_conso.pkl', 'wb') as file:
    pickle.dump(mrconso, file)

with open('new_sty.pkl', 'wb') as file:
    pickle.dump(mrsty, file)

#%% Extraigo informacion de las tablas procesadas en los pkl

# Cargo tablas
import pickle
with open('new_conso.pkl', 'rb') as file:
    mrconso = pickle.load(file)
    
with open('new_sty.pkl', 'rb') as file:
    mrsty = pickle.load(file)

#%% Preprocesamiento

from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
import pandas as pd


with open('C:/Users/Acer/Desktop/umls python/100notas/1134878',
          encoding = 'utf-8') as f:
  data = f.read().translate(trans)
  tokens = [ t.lower() for t in word_tokenize(data) ]


# Hago consultas en mrconso y mrsty para saber tipo semantico
palabra, grupo = [], []

for w in range(len(tokens)):
    
    for i in range(len(mrconso)):
        if mrconso['STR'].values[i] == '{}'.format(tokens[w]):
            palabra.append(mrconso.values[i][1])
            
            for k in range(len(mrsty)):
                if mrsty['CUI'].values[k] == mrconso.values[i][0]:
                    grupo.append(mrsty.values[k][2])


dicc = pd.DataFrame(columns=['palabra', 'grupo'])

dicc['palabra'] = palabra
dicc['grupo'] = grupo


#%%
from collections import Counter
# bow_simple = Counter(lower_tokens)
# print(bow_simple.most_common(10))

bow = Counter(mrsty['STY'])
keys = list(bow.keys())

cuis = Counter(mrsty['CUI'])
=======
def connectdatabase():
    
    conn = mysql.connector.connect(user = 'root', 
                                   password = '', 
                                   host = 'localhost', 
                                   port = '3306', 
                                   db = 'snomed_spa')
    
    if conn:
        print('Conectado  correctamente')
        
    return conn

#%% ETL

def Extract():
    """ 
    Extraccion de todos los datos mrconso y mrsty
    """
                    
    """ Columnas de MRCONSO -> 'CUI','LAT','TS','LUI','STT','SUI','ISPREF',
                                    'AUI','SAUI','SCUI','SDUI','SAB','TTY','CODE',
                                    'STR','SRL','SUPPRESS','CVF' """
    conn = connectdatabase()

    concept = conn.cursor()
    concept.execute("SELECT * FROM mrconso")

    r1 = concept.fetchall()

    mrconso = pd.DataFrame(r1)
    mrconso.columns = ['CUI','LAT','TS','LUI','STT','SUI','ISPREF',
                       'AUI','SAUI','SCUI','SDUI','SAB','TTY','CODE',
                       'STR','SRL','SUPPRESS','CVF']

    """ Columnas de MRSTY -> 'CUI','TUI','STN','STY','ATUI','CVF'  """

    semantic_type = conn.cursor()
    semantic_type.execute("SELECT * FROM mrsty")

    r2 = semantic_type.fetchall()

    mrsty = pd.DataFrame(r2)
    mrsty.columns = ['CUI','TUI','STN','STY','ATUI','CVF']
    
    return mrconso, mrsty

#%%
def Transform(mrconso, mrsty):
    """
    De los datos obtenidos los transformamos a los requeridos para hacer las consultas
    """
    ##### Procesar las columnas necesarias
    
    new_mrconso = mrconso[['CUI', 'STR']]
    
    new_mrsty = mrsty[['CUI', 'TUI', 'STY']]

    # Preprocesamiento de texto para mrconso -> STR
    
    new_mrconso['STR'] = new_mrconso['STR'].str.lower()

    a,b = 'áéíóúüñÁÉÍÓÚÜ','aeiouunAEIOUU'
    trans = str.maketrans(a,b)

    new_mrconso['STR'] = new_mrconso['STR'].str.translate(trans)

    # Preprocesamiento de texto para mrsty -> STY
    
    new_mrsty['STY'] = new_mrsty['STY'].str.lower()
    
    return new_mrconso, new_mrsty

# Backup de las tablas procesadas
# with open('new_mrconso.pkl', 'wb') as file:
#     pickle.dump(Transform(Extract()[0], Extract()[1])[0], file)

# with open('new_mrsty.pkl', 'wb') as file:
#     pickle.dump(Transform(Extract()[0], Extract()[1])[1], file)

#%% Cargo los datos con los tipos semanticos de preferencia
def Load(new_mrconso, new_mrsty):
    """
    Organizo tipos semanticos a utilizar
    """
    
    semantic_type = ['anatomical structure', 'congenital abnormality', 'body system', 'body part, organ, or organ component', 'body location or region', 'body space or junction', 'body substance', 'finding', 'laboratory or test result', 'injury or poisoning', 'physiologic function', 'pathologic function', 'disease or syndrome', 'mental or behavioral dysfunction', 'health care activity', 'laboratory procedure', 'diagnostic procedure', 'therapeutic or preventive procedure', 'research activity', 'temporal concept', 'qualitative concept', 'quantitative concept', 'spatial concept', 'chemical', 'pharmacologic substance', 'biologically active substance', 'hazardous or poisonous substance', 'substance', 'sign or symptom', 'anatomical abnormality', 'antibiotic', 'clinical drug', 'organism function']

    my_sty = pd.DataFrame()

    for w in range(len(semantic_type)):
        my_sty = my_sty.append(new_mrsty[new_mrsty['STY'] == '{}'.format(semantic_type[w])])

    """
    Oganizo vocabulario a utilizar
    Uno los CUI que sean iguales de my_sty en mrconso
    """
    my_vocabulary = new_mrconso.merge(my_sty, on='CUI', suffixes=('_voc','_tip'))

    # Elimino valores duplicados en la columna STR
    my_vocabulary = my_vocabulary.drop_duplicates(subset=['STR'])
    
    print('Vocabulario creado con exito')
    
    return my_vocabulary

# Cargo tablas
# mrconso, mrsty = Extract()[0], Extract()[1]
my_vocabulary = Load(Transform(Extract()[0], Extract()[1])[0], 
                     Transform(Extract()[0], Extract()[1])[1])

with open('my_vocabulary.pkl', 'wb') as file:
    pickle.dump(my_vocabulary, file)
