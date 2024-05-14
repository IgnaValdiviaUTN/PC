from flask import Flask, render_template, request
from deepface import DeepFace
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return "No file part"

    file = request.files['image']

    if file.filename == '':
        return "No selected file"

    # Guardar la imagen cargada en la carpeta 'uploads'
    file.save('static/uploads/' + file.filename)

    try:
        # Analizar edad, género, raza y emociones utilizando DeepFace
        result = DeepFace.analyze(img_path='static/uploads/' + file.filename,
                                  actions=('age', 'gender', 'race', 'emotion'))

        # Obtener la edad estimada
        age = result[0]['age']

        # Obtener el género estimado
        gender = result[0]['gender']

        # Obtener la raza estimada
        race = result[0]['dominant_race']

        # Obtener la emoción dominante
        emotion = result[0]['emotion']

        # Eliminar el archivo después de usarlo
        os.remove('static/uploads/' + file.filename)

        return f"Age: {age}, Gender: {gender}, Race: {race}, Emotion: {emotion}"

    except ValueError as e:
        # Eliminar el archivo después de usarlo
        os.remove('static/uploads/' + file.filename)
        return "No se ha podido detectar un rostro en la imagen. Por favor, carga una imagen con un rostro visible."


if __name__ == '__main__':
    app.run()
