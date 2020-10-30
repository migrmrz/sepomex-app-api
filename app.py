from flask import Flask, jsonify
from datetime import datetime
import os
import time
from selenium import webdriver
from zipfile import ZipFile
from dotenv import load_dotenv
load_dotenv()

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
    if not file_updated():
        download_file()
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
    return jsonify(results=results, count=len(results))


@app.route('/estados', methods=['GET'])
def get_all_estados():
    '''
    Function that will return the complete catalog of Estados with their Code
    '''
    if not file_updated():
        download_file()
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
    return jsonify(results=results, count=len(results))


@app.route('/municipios/<string:c_estado>', methods=['GET'])
def get_ciudad_by_estado(c_estado):
    '''
    Function that will return all matches for Ciudad based on the Estado Code.
    '''
    if not file_updated():
        download_file()
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
    return jsonify(results=results, count=len(results))


@app.route(
    '/asentamientos/<string:c_estado>/<string:c_mnpio>', methods=['GET']
)
def get_asentamiento_by_estado_and_municipio(c_estado, c_mnpio):
    '''
    Function that will return all the matches for Asentamiento, Tipo
    Asentamiento, Código Postal based on Estado and Municipio
    '''
    if not file_updated():
        download_file()
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
    return jsonify(results=results, count=len(results))


def file_updated():
    """
        Validates if file exists and if it has been less than 24 hours since
        last download. Returns True if both conditions meet, else False.
    """
    if os.path.exists("CPdescarga.txt"):
        modified_date_str = time.ctime(os.path.getmtime('CPdescarga.txt'))
        modified_datetime = datetime.strptime(
            modified_date_str,
            "%a %b %d %H:%M:%S %Y")
        timedelta_diff = datetime.now() - modified_datetime
        if timedelta_diff.total_seconds() < 86400:
            return True

    return False


def download_file():
    """
        Using selenium to download the file on a txt file format.
    """
    print("Downloading latest version of the file...")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    driver = webdriver.Chrome(
        os.environ.get("CHROME_DRIVER_LOC") + 'chromedriver',
        chrome_options=options
    )
    driver.get(
        'https://www.correosdemexico.gob.mx/SSLServicios/'
        'ConsultaCP/CodigoPostal_Exportar.aspx'
    )
    format_button = driver.find_elements_by_xpath(
        "//input[@id='rblTipo_1' and @value='txt']"
    )[0]
    download_button = driver.find_elements_by_xpath(
        "//input[@name='btnDescarga' and @type='image' and @id='btnDescarga']"
    )[0]
    format_button.click()
    download_button.click()
    time.sleep(3)
    driver.quit()

    zipfile = os.environ.get("DOWNLOAD_DIR") + "CPdescargatxt.zip"

    with ZipFile(zipfile, 'r') as zip_obj:
        zip_obj.extractall()

    os.remove(zipfile)


app.run(port=5000)
