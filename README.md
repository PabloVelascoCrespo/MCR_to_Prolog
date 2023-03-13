# Conversion of the Spanish WordNet databases into a Prolog-readable format

## ¿Cómo generar los ficheros prolog?
## How to generate prolog files?

### Windows

Para generar todos ficheros y ordenarlos:
To generate all files and sort them:
    Windows\exe.bat

Si se desea traducir y añadir más glosas a wn_g (No se recomienda debido a que tarda alrededor de 5 horas, dependiendo de la conexión):
If you want to translate and add more glosses to wn_g (Not recommended because it takes about 5 hours, depending on the connection):
    Windows\traductor.bat
    
### Linux / MAC OS

Para generar todos los ficheros y ordenarlos, colóquese dentro del directorio Linux-MAC_OS:
To generate all the files and sort them, place them inside the Linux-MAC_OS directory:
    make ejecucion

Si se desea traducir y añadir más glosas a wn_g (No se recomienda debido a que tarda alrededor de 5 horas, dependiendo de la conexión), dentro del directorio mencionado:
If you want to translate and add more glosses to wn_g (not recommended because it takes about 5 hours, depending on the connection), inside the mentioned directory:    
    make traductor