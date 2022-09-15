from consult_umls import *

# PARA HACER PRUEBAS DE CONSULTA
def test_consult(word):
    for i in range(len(my_vocabulary)):
        if my_vocabulary['STR'].values[i] == word:#'{}'.format(ngram_exam[j][0]):
            #print(i)
            #print(my_vocabulary.values[i])
            return print(my_vocabulary.values[i][1], '->', my_vocabulary.values[i][-1], '->', Etiqueta(i))
        
#%% ETIQUETADO EHR
def ehr_process(path):
    
    a,b = 'áéíóúüñÁÉÍÓÚÜ','aeiouunAEIOUU'
    trans = str.maketrans(a,b)
    # example = 'sangrado vaginal sangre examen para dolor de cabeza analisis de embarazo utero contraido dolor de cabeza'

    with open(path, encoding = 'utf-8') as f:
        data = f.read().translate(trans)
        
    return data

data = ehr_process('C:/Users/Acer/Desktop/umls python/100 notas/1134979')


A = etiquetado(data)


# Etiquetado de prueba
with open('prueba_historia.pkl', 'wb') as file:
    pickle.dump(A, file)
    
    
###############
with open('prueba_historia.pkl', 'rb') as file:
    prueba = pickle.load(file)

for i in range(len(prueba)):
    if prueba[:,3][i] == 'O':
        prueba[i, 3] = prueba[i,2]
        
for j in range(len(prueba)):
    if prueba[:,3][j] == 'O':
        prueba[j, 3] = prueba[j,1]

prueba = np.delete(prueba, [1,2], 1)