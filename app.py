
import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Configuracoes externas por variaveis de ambiente
PORTA = int(os.getenv("PORTA", "8080"))
NIVEL_LOG = os.getenv("LOG_LEVEL", "INFO").upper()

# Configuracao dos logs
logging.basicConfig(
    level=getattr(logging, NIVEL_LOG, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Pagina inicial
@app.route("/")
def inicio():
    app.logger.info("Pagina inicial acessada")

    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Docker AAD</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f4f8;
                text-align: center;
                padding: 60px 20px;
                color: #263238;
            }

            .container {
                background-color: white;
                max-width: 600px;
                margin: auto;
                padding: 35px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }

            h1 {
                color: #1976d2;
            }

            p {
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Docker!</h1>
            <h2>Projeto Docker AAD</h2>
            <p>Aplicacao Flask executada em um container Docker.</p>
            <p><strong>Integrantes:</strong></p>
            <p>Atos Gabriel, Amy Galvao e Dymylle Charis</p>
            <p>Servico funcionando corretamente!</p>
        </div>
    </body>
    </html>
    """


# Rota para verificar se o servico esta funcionando
@app.route("/status")
def status():
    app.logger.info("Status do servico consultado")

    return jsonify({
        "servico": "Docker AAD",
        "status": "online",
        "porta": PORTA
    })


# Rota para simular uma falha controlada
# Usada para demonstrar o reinicio automatico do Docker
@app.route("/falha-teste", methods=["POST"])
def falha_teste():
    app.logger.error(
        "Falha controlada para testar o reinicio do Docker"
    )

    # Encerra o processo principal com codigo de erro 1
    os._exit(1)


# Inicializacao do servidor
if __name__ == "__main__":
    app.logger.info(
        "Iniciando servidor na porta %s", PORTA
    )

    app.run(
        host="0.0.0.0",
        port=PORTA,
        debug=False
    )
