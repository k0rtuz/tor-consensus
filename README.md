# tor-consensus

Este proyecto tiene como finalidad recopilar el top 100 de nodos de la red TOR
por ancho de banda, en base a una instalación del navegador Tor en una máquina
que puede ser local o un servidor tal como un VPS.

La información se extrae del archivo **cached-microdesc-consensus** que generalmente
se encuentra en la carpeta **/var/lib/tor** en varias distribuciones Linux.

### Requisitos

Se ha comprobado su funcionamiento en distribuciones Linux (concretamente Debian 11),
por lo que los requisitos necesarios para sistemas con gestores de paquetes de tipo DEB
son los siguientes:

- python3-virtualenv
- python3-pip
- tor

La versión de Python con la que se han hecho las pruebas es la 3.9 (por defecto en Debian 11),
por lo que cualquiera igual o superior a ésta no debería dar problemas.

### Uso

Se incluye un archivo ejecutable llamado `consensus-top` que idealmente ha de dejarse como tarea
periódica en un servidor con *systemd*, gracias a los archivos incluidos en la carpeta `systemd`,
los cuales sólo hay que modificar en la parte de las rutas, según dónde coloquemos este ejecutable.

Los archivos de esta carpeta `systemd` tienen la programación para ejecutar `consensus-top` cada hora,
guardando archivos CSV con información relativa a los 100 nodos con mayor ancho de banda encontrados.

### Alternativa
Otro modo de uso **NO REQUIERE TOR**, puesto que se basa en el histórico de archivos disponible para datos
desde 2014 hasta la fecha en [**CollecTor**](https://metrics.torproject.org/collector.html).

Se justifica esta aproximación debido a que muy frecuentemente el archivo de consenso no se actualiza
con la frecuencia necesaria o bien deja de hacerlo a partir de un momento (se sospecha que es en cuanto
deja de cambiarse de circuito, entre otras razones).

Para ello, para recopilar en un único archivo CSV la información dentro del mes que deseemos, limitada a un
número de días y al top *n* de nodos según ancho de banda, basta ejecutar el siguiente comando desde
la carpeta del repositorio:

```
./consensus load --year <YYYY> --month {1..12} --days dd-dd [--top N=100]
```

Por ejemplo, si quisiéramos extraer un archivo que contuviese por cada día el top 50 de nodos con mayor ancho
de banda entre el 6 y el 12 de diciembre de 2021, ejecutaríamos:

```
./consensus load --year 2021 --month 12 --days 6-12 --top 50
```

Como resultado, se creará una carpeta temporal `tmp` en la cual se guardará el archivo comprimido con los datos
descargados de [**CollecTor**](https://metrics.torproject.org/collector.html) y como resultado el CSV que nos interesa,
que se llamará `top_50_nodes_20211206_to_20211212.csv`

### Gráficas

Por otra parte, el archivo `start` permite levantar en la interfaz de red pública de la máquina
donde se descargue este repositorio un servidor de [**Jupyter Notebook**](https://jupyter.org/try) en
el puerto 1337.

Se trata de un script en Bash que en el mismo directorio donde está, comprueba que exista un entorno
virtual de Python llamado *venv*, creándolo si no es así y descargando las dependencias especificadas
en el archivo de texto *requirements.txt*. Por último, se levanta el servidor y se muestra el token de
autenticación necesario para acceder a los archivos.

Al navegar hacia `http://<IP_PÚBLICA>:1337` se pedirá dicho token y tras navegar hacia la carpeta
`notebooks` se encontrará un *notebook* con el cuál se generan diversas estadísticas partiendo del
archivo CSV generado, que se encuentra en la carpeta `tmp`.