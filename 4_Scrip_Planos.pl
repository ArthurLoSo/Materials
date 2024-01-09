#!perl

# Correr programa con servidor
use strict;
use Getopt::Long;
use MaterialsScript qw(:all);
use IO::Handle;

print "Iniciando Scrip Perl\n";
my @files=<C:/Users/azul_/Escritorio/Proyecto/Dstos/COD/*>;                     # Directorio a importar (MS solo corre en Windows)
my $exportDir="C:/Users/azul_/Escritorio/Proyecto/Datos/CSV/";		            # Directorio a exportar
my $nameFile;						                                            # Almacena el nombre del cif
my $doc;						                                                # Lee el cif
my $export;						                                                # Almacena la ruta completa del cif
my $parmReflex;						                                            # Configuracion del reflex
my $reflex;						                                                # Tabla de estudio
#ELIMINAR AUSENTEs
my $row;						                                                # Almacena un dato de la fila
my $i=0;
#EXCEPCIONES 
my @excepcion;						                                            # Almacena Excepciones
foreach my $file (@files){				                                        # Recorre archivos
print "--->Procesando ",$file,"\n";
eval {
$nameFile=substr $file,-11,-4;				                                    # Nombre del cif
$export=$exportDir.$nameFile.".csv";			                                # Se define la ruta de salida
 $doc= Documents->Import($file);			                                    # Importa el archivo para correr el modulo
$parmReflex = Modules->Reflex->PowderDiffraction->Run ($doc,                    # Define los parametros del modulo Pawder difrfaction
                               Settings(ShowDifferencePattern => "Yes",
                                        CreateReflectionsStudyTable => "Yes",
					                    TwoThetaMin=>5,
					                    TwoThetaMax=>85));	                    # Define las Configuraciones

$reflex = $parmReflex->ReflectionsStudyTable;			                        # Obteniendo la tabla de reflexiones
$reflex->DeleteColumn("h");
$reflex->DeleteColumn("k");
$reflex->DeleteColumn("l");
$reflex->DeleteColumn("dhkl");
$reflex->DeleteColumn("Intensity");
$reflex->DeleteColumn("Multiplicity");
$reflex->DeleteColumn("Wavelength");
for ($i=0; $i<$reflex->RowCount; ++$i) {		                                # Eliminar Filas Ausentes
    $row = $reflex->Cell($i, "Absent");			                                # Obtener celda Absent
    if($row eq "Y") {					                                        # Si esta ausente
    $reflex->DeleteRow($i);				                                        # Eliminar columna
    --$i;						                                                # Mantenerse e la misma posicion
     }
}
$reflex->DeleteColumn("Absent");
$reflex->Export($export);				                                        # Exportar tabla modificada
};
if($@){
push(@excepcion,$file."\n");
}

}
print "======= Archivos No Procesados Por Inconsistencia de Datos =======\n";
open(Inconsistencia, ">C:/Users/azul_/Escritorio/Proyecto/Datos/CSV/Inconsistencias.txt");  	# Crea un archivo txt
print Inconsistencia @excepcion;									            # Agrega al archivo las inconsistencias
close(Inconsistencia);											                # Cierra el archivo txt
print "Script Finalizado\n";