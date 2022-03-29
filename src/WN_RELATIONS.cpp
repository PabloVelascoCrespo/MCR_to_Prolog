#include <iostream>
#include <cstring>
#include <fstream>
#include <string>
#include <climits>
#include <algorithm>
#include <regex>

using namespace std;

//TODO implementar para que lo haga con todos los idiomas
string* idiomas = new string[5] { "cat", "eus", "glg","por","spa"};

string do_replace( string const & in, string const & from, string const & to )
{
  return regex_replace( in, regex(from), to );
}

string codificacion_categorias(string c)
{
    if(c == "n") return "1";
    else if (c == "v") return "2";
    else if (c == "a") return "3";
    else if (c == "r") return "4";
    else return "-1";
}

int main()
{
    for(int idiomaIndex = 0; idiomaIndex < 5; idiomaIndex++)
    {
        fstream ficheroLectura;
        fstream ficheroEscritura_hyp;
        fstream ficheroEscritura_der;
        fstream ficheroEscritura_vgp;
        fstream ficheroEscritura_per;
        fstream ficheroEscritura_ant;
        size_t i;
        string datos[9];
        cout << "Abriendo ficheros...\n";

        ficheroLectura.open("../mcr/"+idiomas[idiomaIndex]+"WN/wei_"+idiomas[idiomaIndex]+"-30_relation.tsv", ios::in);
        ficheroEscritura_hyp.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_hyp.pl", ios::out);
        ficheroEscritura_der.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_der.pl", ios::out);
        ficheroEscritura_vgp.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_vgp.pl", ios::out);
        ficheroEscritura_per.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_per.pl", ios::out);
        ficheroEscritura_ant.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_ant.pl", ios::out);

        if(!ficheroLectura.is_open() || !ficheroEscritura_hyp.is_open() || !ficheroEscritura_der.is_open() || !ficheroEscritura_vgp.is_open() || !ficheroEscritura_per.is_open() || !ficheroEscritura_ant.is_open())
        {
            cout << "No se han abierto correctamente\n";
            return 0;
        }

        cout << "Se han abierto correctamente.\n" << "Parseando a Prolog...\n";

        string line;

        while(getline(ficheroLectura, line))
        {
            i = 0;
            char *cadena = line.data();
            char *token =strtok(cadena, "\t");

            while(token != NULL)
            {
                datos[i] = token;
                token = strtok(NULL, "\t");
                i++;
            }

            if(datos[0] == "12")
            {
                ficheroEscritura_hyp << "hyp(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }

            if(datos[0] == "31")
            {
                ficheroEscritura_der << "der(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }

            if(datos[0] == "52")
            {
                ficheroEscritura_vgp << "vgp(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }

            if(datos[0] == "47")
            {
                ficheroEscritura_per << "per(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }

            if(datos[0] == "33")
            {
                ficheroEscritura_ant << "ant(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }
        }

        cout << "Idioma "+idiomas[idiomaIndex]+" parseado correctamente.\n";
        ficheroLectura.close();
        ficheroEscritura_hyp.close();
    }

    cout << "¡Proceso finalizado!";
    return 0;
}