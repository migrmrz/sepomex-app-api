# SEPOMEX App API

Python app that would go through a txt file to get Postal Codes from SEPOMEX.

It currently supports the following methods:

- GET All by Zip Code (/all/<codigo_postal>). Returns: Asentamiento,
Tipo Asentamiento, Municipio, Estado, Ciudad)
- GET All Estados (/estados). Returns: Estado and Estado Code
- GET Ciudad by Estado (/municipios/<c_estado>). Returns: Municipio and
Municipio Code
- GET Asentamientos (/asentamientos/<c_estado>/<c_municipio>). Returns:
Zip Code, Asentamiento and Id Asentamiento, Tipo Asentamiento
