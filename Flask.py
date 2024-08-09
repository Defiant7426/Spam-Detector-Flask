from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# cargamos el modelo
model = joblib.load('model/model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # obtenemos los datos del body
    data_string = request.get_json(force=True)

    # preparamos los datos
    data = preparar_data(data_string["features"])

    # realizamos la prediccion
    prediction = model.predict(data)

    # retornamos la prediccion
    return jsonify({'prediction': prediction.tolist()})


def preparar_data(data):
    # convertimos el texto en una lista de palabras
    data = data.split(' ')

    # contamos la cantidad de palabras para cada categoria que necesita la entrada de nuestro modelo
    data_count = [data.count('make'),
                  data.count('address'),
                  data.count('all'),
                  data.count('3d'),
                  data.count('our'),
                  data.count('over'),
                  data.count('remove'),
                  data.count('internet'),
                  data.count('order'),
                  data.count('mail'),
                  data.count('receive'),
                  data.count('will'),
                  data.count('people'),
                  data.count('report'),
                  data.count('addresses'),
                  data.count('free'),
                  data.count('business'),
                  data.count('email'),
                  data.count('you'),
                  data.count('credit'),
                  data.count('your'),
                  data.count('font'),
                  data.count('000'),
                  data.count('money'),
                  data.count('hp'),
                  data.count('hpl'),
                  data.count('george'),
                  data.count('650'),
                  data.count('lab'),
                  data.count('labs'),
                  data.count('telnet'),
                  data.count('857'),
                  data.count('data'),
                  data.count('415'),
                  data.count('85'),
                  data.count('technology'),
                  data.count('1999'),
                  data.count('parts'),
                  data.count('pm'),
                  data.count('direct'),
                  data.count('cs'),
                  data.count('meeting'),
                  data.count('original'),
                  data.count('project'),
                  data.count('re'),
                  data.count('edu'),
                  data.count('table'),
                  data.count('conference'),
                  data.count(';'),
                  data.count('('),
                  data.count('['),
                  data.count('!'),
                  data.count('$'),
                  data.count('#')]
    # data.count('capital_run_length_average'),
    # data.count('capital_run_length_longest'),
    # data.count('capital_run_length_total')]

    # convertimos cada cuenta en la frecuencia de cada palabra
    data_new = []
    for i in range(len(data_count)):
        data_new.append((data_count[i] / len(data)) * 100)

    # agregamos las variables que faltan
    # capital_run_length_average significa la longitud promedio de las secuencias de letras mayúsculas
    # capital_run_length_longest significa la longitud de la secuencia más larga de letras mayúsculas
    # capital_run_length_total significa la suma de la longitud de todas las secuencias de letras mayúsculas

    capital_run_length_average = 0
    capital_run_length_longest = 0
    capital_run_length_total = 0

    current_run_length = 0
    num_runs = 0

    for word in data:
        for letter in word:
            if letter.isupper():
                current_run_length += 1
                capital_run_length_total += 1
            else:
                if current_run_length > capital_run_length_longest:
                    capital_run_length_longest = current_run_length
                capital_run_length_average += current_run_length
                current_run_length = 0
                num_runs += 1

    # consideramos la ultima secuencia
    if current_run_length > capital_run_length_longest:
        capital_run_length_longest = current_run_length
        capital_run_length_average += current_run_length
        num_runs += 1

    # calculamos la longitud promedio
    if num_runs > 0:
        capital_run_length_average = (capital_run_length_average / num_runs) * 100

    # agregamos las variables al array
    data_new.append(capital_run_length_average)
    data_new.append(capital_run_length_longest)
    data_new.append(capital_run_length_total)

    # retornamos los datos preparados
    return [data_new]

app.run(host='0.0.0.0')
