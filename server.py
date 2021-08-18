from models import Previsao
from flask import render_template
from sqlalchemy import desc
import config

# Lib que permite ler variáveis de ambiente.
from os import environ

# Lê a variável de ambiente HOST e na sua ausência usa o endereço '0.0.0.0'.
# Esse endereço com zeros indica ao Flask para aceitar requisições de outras origens.
# Por default o Flask só aceita requisições da máquina local.
host = environ.get("HOST", '0.0.0.0')

# Lê a variável de ambiente PORT, pois no servidor é um dado dinâmico.
port = environ.get("PORT", 5000)

# Imprime os dados para aparecer no log do Heroku.
print("HOST={} PORT={}".format(host, port))

app = config.connex_app

# Lê arquivo swagger.yml para configurar os endpoints da api
app.add_api("swagger.yml")

# Essa variável "application" será usada pelo Gunicorn para subir o Flask.
application = app.wsgi_app

@app.route('/')
def index():
    """
    Essa função responde a requisição localhost:5000/
    :return:        O template renderizado "index.html"
    """
    # Recupera do banco de dados todas as previsões ordenadas por data
    previsoes = Previsao.query.order_by(desc(Previsao.data_execucao)).all()
    # Retorna a renderização de index.html 
    return render_template('index.html', previsoes=previsoes)

if __name__ == "__main__":
    app.run(debug=False, host=host, port=port)
