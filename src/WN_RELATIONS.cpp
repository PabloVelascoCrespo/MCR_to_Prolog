#include <iostream>
#include <cstring>
#include <fstream>
#include <string>
#include <climits>
#include <algorithm>
#include <regex>

using namespace std;

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
        fstream ficheroEscritura_sim;
        fstream ficheroEscritura_sub;
        fstream ficheroEscritura_xphyp;
        fstream ficheroEscritura_rel;
        fstream ficheroEscritura_cat;
        fstream ficheroEscritura_rgloss;
        fstream ficheroEscritura_rterm;
        fstream ficheroEscritura_uterm;
        fstream ficheroEscritura_mm;
        fstream ficheroEscritura_mp;
        fstream ficheroEscritura_sa;

        size_t i;
        string datos[9];
        cout << "Abriendo ficheros...\n";

        ficheroLectura.open("../mcr/"+idiomas[idiomaIndex]+"WN/wei_"+idiomas[idiomaIndex]+"-30_relation.tsv", ios::in);
        ficheroEscritura_hyp.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_hyp.pl", ios::out);
        ficheroEscritura_der.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_der.pl", ios::out);
        ficheroEscritura_vgp.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_vgp.pl", ios::out);
        ficheroEscritura_per.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_per.pl", ios::out);
        ficheroEscritura_ant.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_ant.pl", ios::out);
        ficheroEscritura_sim.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_sim.pl", ios::out);
        ficheroEscritura_sub.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_sub.pl", ios::out);
        ficheroEscritura_xphyp.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_xphyp.pl", ios::out);
        ficheroEscritura_rel.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_rel.pl", ios::out);
        ficheroEscritura_cat.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_cat.pl", ios::out);
        ficheroEscritura_rgloss.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_rgloss.pl", ios::out);
        ficheroEscritura_rterm.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_rterm.pl", ios::out);
        ficheroEscritura_uterm.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_uterm.pl", ios::out);
        ficheroEscritura_mm.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_mm.pl", ios::out);
        ficheroEscritura_mp.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_mp.pl", ios::out);
        ficheroEscritura_sa.open("../"+idiomas[idiomaIndex]+"/Prolog/wn_sa.pl", ios::out);


        if(!ficheroLectura.is_open() || !ficheroEscritura_hyp.is_open() || !ficheroEscritura_der.is_open() || !ficheroEscritura_vgp.is_open() || !ficheroEscritura_per.is_open() || !ficheroEscritura_sub.is_open() || !ficheroEscritura_xphyp.is_open() || !ficheroEscritura_ant.is_open() || !ficheroEscritura_sim.is_open() || !ficheroEscritura_rel.is_open() || !ficheroEscritura_cat.is_open() || !ficheroEscritura_rgloss.is_open() || !ficheroEscritura_rterm.is_open() || !ficheroEscritura_uterm.is_open() || !ficheroEscritura_mm.is_open() || !ficheroEscritura_mp.is_open() || !ficheroEscritura_sa.is_open())
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
            }else if(datos[0] == "33")
            {
                ficheroEscritura_ant << "ant(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ",0," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ",0)." << endl;
            }else if(datos[0] == "47")
            {
                ficheroEscritura_per << "per(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ",0," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ",0)." << endl;
            }else if(datos[0] == "19")
            {
                ficheroEscritura_sub << "sub(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }else if(datos[0] == "31")
            {
                ficheroEscritura_der << "der(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }else if(datos[0] == "52")
            {
                ficheroEscritura_vgp << "vgp(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ",0," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ",0)." << endl;
            }else if(datos[0] == "34")
            {
                ficheroEscritura_sim << "sim(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << "," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ")." << endl;
            }else if(datos[0] == "21")
            {
                ficheroEscritura_xphyp << "xphyp(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }else if(datos[0] == "63")
            {
                ficheroEscritura_cat << "cat(" << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << "," << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ")." << endl;
            }else if(datos[0] == "64")
            {
                ficheroEscritura_rel << "rel(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << "," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ")." << endl;
            }else if(datos[0] == "61")
            {
                ficheroEscritura_rgloss << "rgloss(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << "," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ")." << endl;
            }else if(datos[0] == "66")
            {
                ficheroEscritura_rterm << "rterm(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << "," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ")." << endl;
            }else if(datos[0] == "68")
            {
                ficheroEscritura_uterm << "uterm(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << "," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ")." << endl;
            }else if(datos[0] == "7")
            {
                ficheroEscritura_mm << "mm(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << "," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ")." << endl;
            }else if(datos[0] == "8")
            {
                ficheroEscritura_mp << "mp(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << "," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ")." << endl;
            }else if(datos[0] == "49")
            {
                ficheroEscritura_sa << "sa(" << codificacion_categorias(datos[2]) << datos[1].substr(7,8) << ",0," << codificacion_categorias(datos[4]) << datos[3].substr(7,8) << ",0)." << endl;
            }
        }

        cout << "Idioma "+idiomas[idiomaIndex]+" parseado correctamente.\n";
        ficheroLectura.close();
        ficheroEscritura_hyp.close();
    }

    cout << "¡Proceso finalizado!";
    return 0;
}