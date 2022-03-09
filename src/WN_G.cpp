#include <iostream>
#include <cstring>
#include <fstream>
#include <string>
#include <climits>
#include <algorithm>
#include <regex>

using namespace std;

string do_replace( string const & in, string const & from, string const & to )
{
  return std::regex_replace( in, std::regex(from), to );
}

int codificacionCategorias(string c)
{
    if(c == "n") return 1;
    else if (c == "v") return 2;
    else if (c == "a") return 3;
    else if (c == "r") return 4;
    else return -1;
}

int main()
{   
    string datos [10];
    fstream ficheroLectura;
    fstream ficheroEscritura;
    size_t i = 0;
    size_t j = 0;

    cout << "Abriendo ficheros...\n";

    ficheroLectura.open("../spaWN/wei_spa-30_synset.tsv", ios::in);
    ficheroEscritura.open("../Prolog/wn_g.pl", ios::out);
    if(!ficheroLectura.is_open() || !ficheroEscritura.is_open())
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
        ficheroEscritura << "g(" << codificacionCategorias(datos[0].substr(16,1)) << datos[0].substr(7, 8) << ",'" << datos[6] << "')." << endl;
    }

    cout << "Parseado correctamente.\n";
    ficheroLectura.close();
    ficheroEscritura.close();
    cout << "¡Proceso finalizado!";

    return 0;
}