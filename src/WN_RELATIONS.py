import time

idiomas = ['cat', 'eng', 'eus', 'glg', 'por', 'spa']

def codificacionCategoria(c):
    categorias = {
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
        }
    return categorias[c]

# 1: 2 datos del revés

# 2: 4 datos del revés

# 3: 2 datos del derecho

# 4: 4 datos del derecho

def seleccionRelacion(id):
    relaciones = {
        '12':['hyp',1],'33':['ant',2],'31':['der',1],'52':['vgp',4],'47':['per',2],'34':['sim',3],'19':['sub',1],'21':['xphyp',1],'64':['rel',3],
        '63':['cat',1],'61':['rgloss',3],'66':['rterm',3],'68':['uterm',3],'7':['mm',3],'8':['mp',3],'49':['sa',4],'1':['bis',3],
        '2':['cau',3],'3':['fuz',3],'5':['ml',1],'6':['mmof',1],'9':['hp',3],'10':['m',1],'35':['in',1],'36':['ina',1],
        '37':['ind',1],'38':['ini',1],'39':['inl',1],'40':['inp',1],'41':['isd',1],'42':['itd',1],'44':['xpfuz',3],'45':['xpant',3],
        '46':['xpsim',3],'60':['near',3]
        }
    return relaciones[id]

for i in idiomas:
    inicio = time.time()
    ruta = 'mcr\\'+i+'WN\wei_'+i+'-30_relation.tsv'
    print('Abriendo fichero ' + ruta)

    ficheroLectura = open(ruta,'r', encoding='utf-8')
    lineas = ficheroLectura.readlines()

    for linea in lineas:
        linea = linea.split('\t') 
        datos = seleccionRelacion(linea[0])

        ficheroEscritura = open(i+"\Prolog\wn_"+datos[0]+".pl", "a", encoding='utf-8')

        if datos[1] == 1:
            ficheroEscritura.write(datos[0]+'('+codificacionCategoria(linea[4]) + linea[3][7:15]+','+codificacionCategoria(linea[2])+ linea[1][7:15]+').\n')
        elif datos[1] == 2:
            ficheroEscritura.write(datos[0]+'('+codificacionCategoria(linea[4]) + linea[3][7:15]+',0,'+codificacionCategoria(linea[2])+ linea[1][7:15]+',0).\n')
        elif datos[1] == 3:
            ficheroEscritura.write(datos[0]+'('+codificacionCategoria(linea[2]) + linea[3][7:15]+','+codificacionCategoria(linea[4])+ linea[1][7:15]+').\n')
        elif datos[1] == 4:
            ficheroEscritura.write(datos[0]+'('+codificacionCategoria(linea[2]) + linea[3][7:15]+',0,'+codificacionCategoria(linea[4])+ linea[1][7:15]+',0).\n')

        ficheroEscritura.close()
    final = time.time()
    print('Idioma '+i+' finalizado en: '+str(final-inicio)+'.\n')