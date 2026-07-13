from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f"¡Hola desde Python en Kubernetes! Respondido por el Pod: {hostname}\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)