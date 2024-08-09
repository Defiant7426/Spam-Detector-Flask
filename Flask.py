from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# cargamos el modelo
model = joblib.load('model/model.pkl')

@app.route('/prueba', methods=['GET'])
def prueba():
    return jsonify({'message': 'Hola Mundo'})

@app.route('/prueba2', methods=['POST'])
def prueba2():
    data = request.get_json(force=True)
    return jsonify({'message': 'Esto es algo adicional ;) ' + data['message']})

@app.route('/predict', methods=['POST'])
def predict():
    # obtenemos los datos del body
    data = request.get_json(force=True)

    # preparamos los datos
    #data = prepare_data(data)

    # realizamos la prediccion
    prediction = model.predict([data['features']])

    # retornamos la prediccion
    return jsonify({'prediction': prediction.tolist()})

def prepare_data(data):
    return [[data['features']]]

if __name__ == '__main__':
    app.run(port=5000, debug=True)