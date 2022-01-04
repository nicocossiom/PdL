# PDL Javascript

## Tabla de contenidos
1. [Descripción del proyecto](#Descripción-del-proyecto)
2. [Instalación del procesador:](#Instalación-del-procesador)
   - [Portable](#Portable)
   - [Instalación local](#Instalación-local)  
        - [Desinstalación](#Desinstalación)
3. [Uso](#Uso)
4. [Estructura del código fuente](#Estructura-del-código-fuente)



## Descripción del proyecto
[Aquí](https://github.com/nicocossiom/PdL/blob/main/resources/descripcion.md) se encuentra una descripción detallada del proyecto


## Instalación del procesador
Existen 2 formas de instalar el procesador, mediante un archivo portable o mediante la instalación en un ejecutable. El uso del programa es distinto según la forma que se elija, más abajo se explica cada uno.
> **WARNING**: En caso de no funcionar el la instalación del paquete use el formato portable, es universal y si se usa correctamente no debería dar errores. 

### Portable
Se descarga el código fuente y se ejecuta el archivo usando Python como intérprete. 
Instrucciones:
1. Clonar el repositorio &rarr;``` git clone https://github.com/nicocossiom/PdL```
2. Usar ``` python AbsolutePath/to/processor.py ARCHIVO``` 

### Instalación local
Se descarga el código fuente y se instala un ejecutable que se puede llamar desde cualquier lugar del sistema operativo


**Instalación**:
- MacOS / Linux  
``` 
git clone https://github.com/nicocossiom/PdL && sudo python3 -m pip install -e PdL
```
- Windows (desde una terminal lanzada como administrador): 
```
git clone https://github.com/nicocossiom/PdL && python3 -m pip install -e PdL
```

### Desinstalación
- MacOS / Linux  
``` 
sudo python3 -m pip uninstall -e pdljs -y
```
- Windows (no hace falta que la terminal sea lanzada como administrador) : 
```
python3 -m pip uninstall -e pdljs -y
```

Para comprobar si se ha instalado correctamente use 
```
python3 -m pip show processor
```
Devolverá lo siguiente si no está instalado: 
> WARNING: Package(s) not found: pdljs

Si está instalado devolverá: 
> Name: jspdl
Version: 1.0
Summary: UNKNOWN
Home-page: UNKNOWN
Author:
Author-email:
License: UNKNOWN
Location: /mnt/c/Users/nicol/Documents/prueba
Requires:
Required-by:

Si está instalado 

## Uso
### Comando a lanzar
**Portable**: 
``` python AbsolutePath/to/processor.py ARCHIVO``` 

Ejemplo en Windows:
> 1. Abro terminal y me sitúo en C:\Users\nicol\Downloads\
> 2. Uso comando git clone https://github.com/nicocossiom/PdL
   Se me crea carpeta C:\Users\nicol\Downloads\PdL
> 3. Para ejecutar cualquier archivo uso:  
      C:\Users\nicol\Downloads\PdL\jspdl.py ARCHIVO

Ejemplo en MacOS / Linux:

> 1. Abro terminal y me sitúo en /home/nicol/Downloads/
> 2. Uso comando git clone https://github.com/nicocossiom/PdL  
     Se me crea carpeta /home/nicol/Downloads/PdL/
> 3. Para ejecutar cualquier archivo dentro de cualquier carpeta uso:
     /home/nicol/Downloads/PdL/jspdl.py ARCHIVO
>
**Instalado** (en cualquier OS): 
``` jspdl ARCHIVO```

### Output del programa
Se crea una carepta con el nombre de fichero sin su extensión que contiene los siguientes archivos:  

//TODOs
```
carpetaOutput
|--- tokens.txt -> contiene los 
|--- errors.txt -> contiene 
|--- ts.txt     -> contiene
|--- parse.txt  -> contiene 
```
## Estructura del código fuente
//TODO