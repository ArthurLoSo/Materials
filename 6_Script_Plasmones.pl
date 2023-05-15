#!perl
use strict;
use Getopt::Long;
use MaterialsScript qw(:all);
use IO::Handle;

print "Iniciando Scrip Perl\n";

my @files=<C:/Users/azul_/Escritorio/Proyecto1/Datos/ClasesCIF/OyD/*>;      # Directorio a importar donde se encuentran los archivos
my $exportDir="C:/Users/azul_/Escritorio/Proyecto1/Datos/Plasmones/";		# Directorio a exportar
my $nameFile;				                                                # Almacena el nombre del cif
my $doc;						                                            # Lee el cif
my $export;
my $paramabs;						                                        # Salida de modulo CASTEP
my $abs;                                                                    # Parametro de propiedades opticas
	
foreach my $file (@files){				                                    # Recorre archivos
print "--->Procesando ",$file,"\n";
eval {
$nameFile=substr $file,-11,-4;				                                # Nombre del cif
$export=$exportDir.$nameFile.".csv";			                            # Se define el path de salida
 $doc= Documents->Import($file);			                                # Importa el archivo a procesar
my $paramabs = Modules->CASTEP->Energy->Run($doc,                           # Modulo CASTEP
                          Settings(Quality =>"Coarse",
                          CalculateOptics => "Full",
                          OpticsUnits =>"nm"));

$abs=$paramabs->OpticsAbsorptionChart;                                      # Obtiene las propiedades opticas
$abs->Export($export);                                                      # Exporta las propiedades opticas
print $abs;
};
}
print "fin del programa";