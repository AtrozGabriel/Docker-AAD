
import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

PORTA = int(os.getenv("PORTA", "8080"))
NIVEL_LOG = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, NIVEL_LOG, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/")
def inicio():
    app.logger.info("Pagina inicial acessada")
    return """
    <html>
        <head>
            <title>Trabalho Docker AAD</title>
        </head>
        <body style="font-family: Arial; text-align: center;
                     margin-top: 100px;">
            <h1>Docker!</h1>
            <p>Trabalho de Sistemas Operacionais</p>
            <p>Professor: Guibson Krause</p>
            <p>Alunos: Atos Gabriel, Amy Galvão, Dymylle charis/p>
            <h2 style="color: green;">Servidor funcionando!</h2>
        </body>
    </html>
    """

@app.route("/status")
def status():
    app.logger.info("Status do servico consultado")
    return jsonify({
        "servico": "Docker AAD",
        "status": "online",
        "porta": PORTA
    })

if __name__ == "__main__":
    app.logger.info("Iniciando servidor na porta %s", PORTA)
    app.run(host="0.0.0.0", port=PORTA)