from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from deepface import DeepFace
import os


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Guardar la imagen en un archivo temporal
            temp_image_path = 'static/uploads/temp_image.jpg'
            with open(temp_image_path, 'wb') as temp_image_file:
                temp_image_file.write(post_data)

            # Llamar a la función analyze_data()
            result = analyze_data(temp_image_path)
            print(result)

            # Eliminar el archivo después de usarlo
            os.remove(temp_image_path)

            # Enviar la respuesta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')



def analyze_data(path):

    try:
        # Analizar edad, género, raza y emociones utilizando DeepFace
        result = DeepFace.analyze(img_path= path,
                                  actions=('age', 'gender', 'race', 'emotion'))

        # Obtener la edad estimada
        age = result[0]['age']

        # Obtener el género estimado
        gender = result[0]['gender']

        # Obtener la raza estimada
        race = result[0]['dominant_race']

        # Obtener la emoción dominante
        emotion = result[0]['emotion']

        return f"Age: {age}, Gender: {gender}, Race: {race}, Emotion: {emotion}"



    except ValueError as e:
        # Eliminar el archivo después de usarlo
        return "No se ha podido detectar un rostro en la imagen. Por favor, carga una imagen con un rostro visible."


def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    run_server()