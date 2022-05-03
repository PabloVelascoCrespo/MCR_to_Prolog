#include <iostream>
#include <fstream>
#include <regex>

using namespace std;

string* idiomas = new string[5] { "cat", "eus", "glg","por","spa"};

string do_replace( string const & in, string const & from, string const & to )
{
  return regex_replace( in, regex(from), to );
}

int contar_synsets(int *synsets, int s, size_t size)
{
    int count = 1;

    auto itr = find(synsets, synsets + size, s);

    if(itr == synsets + size)
    {
        return count;
    }

    for (size_t i = distance(synsets, itr); i < size; i++)
    {
        if(synsets[i] == s) count++;
    }
    
    return count;   
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
        string datos [7];
        int synsets[150000];
        fstream ficheroLectura;
        fstream ficheroEscritura;
        size_t i = 0;
        size_t j = 0;

        cout << "Abriendo ficheros...\n";
        
        ficheroLectura.open("../mcr/"+idiomas[idiomaIndex]+"WN/wei_"+idiomas[idiomaIndex]+"-30_variant.tsv", ios::in);    
        ficheroEscritura.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_s.pl", ios::out);
        
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

            string synsetAux = codificacion_categorias(datos[3]) + datos[2].substr(7, 8);
            int synset = stoi(synsetAux);
            ficheroEscritura << "s(" << synset << "," << contar_synsets(synsets, synset, j) << ",'" << do_replace(datos[0], "'", "''") << "'," << datos[3] << "," << datos[1] << ",'')." << endl;
            synsets[j] = synset;
            j++;
        }

        cout << "Idioma "+idiomas[idiomaIndex]+" parseado correctamente.\n";
        ficheroLectura.close();
        ficheroEscritura.close();
    }
    cout << "¡Proceso finalizado!";
    return 0;
}