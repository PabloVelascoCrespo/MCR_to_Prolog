=============================
#Conversion of the Spanish WordNet databases into a Prolog-readable format (with Tag-count information)

The Spanish WordNet, like others, does not provide a version compatible with Prolog. This work aims to fill this gap by translating the Multilingual Central Repository (MCR) version of the Spanish WordNet (based on the English WordNet 3.0) into anProlog-compatible format. This goal is motivated by the variety of linguistic applications that can be addressed using WordNet in combination with the declarative features of Prolog (for example, cataloging of texts, analysis of causal relationships,. . ., and generally more intuitive access to information contained in WordNet).

Although we dedicated special attention to the case of the Spanish WordNet, we also performed the conversion of the other European language databases (Catalan, Basque, Galician and Portuguese) in MCR.

Details about this work can be found in the article:
Julián-Iranzo, P. & Rigau, G. & Sáenz-Pérez, F & Velasco-Crespo, V. "Conversion of the Spanish WordNet databases into a Prolog-readable format". Lang Resources & Evaluation (2024). 
https://doi.org/10.1007/s10579-024-09752-w
https://link.springer.com/article/10.1007/s10579-024-09752-w

Finally, it is important to highlight that in this new version we are publishing, the s.pl file of the Spanish version of WordNet has been supplemented with data on word usage stored in its Tag-count field. This important information was missing from the MCR files, and a complex process was required to acquire it (using the limited Spanish corpora available, which also had to be aligned with WordNet version 3.0).
=============================

# Conversion of the Spanish WordNet databases into a Prolog-readable format

## ¿Cómo generar los ficheros prolog? / How to generate prolog files?

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