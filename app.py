# Python app that would go through a txt file to get Postal Codes from SEPOMEX

# Function for getting Asentamiento, Tipo de Asentamiento, Municipio, Estado
# y Ciudad based on Postal Code from the CPDescarga.txt file
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/all/<string:postal_code>', methods=['GET'])
def get_data_by_cp(postal_code):
    '''
    Function that will return the following parameters:
    - Asentamiento (Nombre)
    - Tipo Asentamiento (Colonia, Barrio, Pueblo)
    - Municipio
    - Estado
    - Ciudad
    The result will be in a list form, and might contain more than one line
    '''
    # Open file for read
    sepomex_file = open("CPdescarga.txt", encoding="ISO-8859-1")
    # List definition for the resulting lines
    results = []
    # Loop that will search for the provided Postal Code
    for line in sepomex_file:
        result = line.split('|')
        if postal_code == result[0]:
            info = {
                'asentamiento': result[1],
                'tipo_asentamiento': result[2],
                'municipio': result[3],
                'estado': result[4],
                'ciudad': result[5],
            }
            results.append(info)
    # Close the file
    sepomex_file.close()
    return jsonify(results=results)


@app.route('/estados', methods=['GET'])
def get_all_estados():
    '''
    Function that will return the complete catalog of Estados with their Code
    '''
    # Open file for read
    sepomex_file = open("CPdescarga.txt", encoding="ISO-8859-1")
    # List definition for the resulting lines
    results = []
    # Unique list definition for Estado
    c_estados = []
    # Loop that will get all the Estados and Estados' codes
    for index, line in enumerate(sepomex_file):
        result = line.split('|')
        if index < 2:
            pass
        else:
            c_estado = result[7]
            if c_estado not in c_estados:
                c_estados.append(c_estado)
                info = {
                    'estado': result[4],
                    'c_estado': c_estado
                }
                results.append(info)
    # CLose the file
    sepomex_file.close()
    return jsonify(results=results)


@app.route('/municipios/<string:c_estado>', methods=['GET'])
def get_ciudad_by_estado(c_estado):
    '''
    Function that will return all matches for Ciudad based on the Estado Code.
    '''
    # Open file for read
    sepomex_file = open("CPdescarga.txt", encoding="ISO-8859-1")
    # List definition for the resulting lines
    results = []
    c_mnpios = []
    # Loop that will search for the provided Postal Code
    for index, line in enumerate(sepomex_file):
        result = line.split('|')
        if index < 2:
            pass
        else:
            c_mnpio = result[11]
            if c_estado == result[7] and c_mnpio not in c_mnpios:
                c_mnpios.append(c_mnpio)
                info = {
                    'c_mnpio': result[11],
                    'municipio': result[3],
                }
                results.append(info)
    # Close the file
    sepomex_file.close()
    return jsonify(results=results)


@app.route(
    '/asentamientos/<string:c_estado>/<string:c_mnpio>', methods=['GET']
)
def get_asentamiento_by_estado_and_municipio(c_estado, c_mnpio):
    '''
    Function that will return all the matches for Asentamiento, Tipo
    Asentamiento, Código Postal based on Estado and Municipio
    '''
    # Open file for read
    sepomex_file = open("CPdescarga.txt", encoding="ISO-8859-1")
    # List definition for the resulting for the resulting lines iterated
    results = []
    # Loop that will search for the provided Estado and Municipio
    for index, line in enumerate(sepomex_file):
        result = line.split('|')
        if index < 2:
            pass
        else:
            if c_estado == result[7] and c_mnpio == result[11]:
                info = {
                    'codigo_postal': result[0],
                    'asentamiento': result[1],
                    'id_asenta_cpcons': result[12],
                    'tipo_asentamiento': result[2]
                }
                results.append(info)
    # Close file
    sepomex_file.close()
    return jsonify(results=results)


app.run(port=5000)
