from flask import Flask, request, Response
from flask.json import jsonify
import time
from random import choices
from datetime import datetime, timedelta

app = Flask(__name__)

# Lista de todas requisições para controle de throttling
req_list = {}

@app.route('/status/fixed/<status>')
# Retorna o status informado no path
# Opcionalmente aguarda o delay informado no query string
def fixed(status):
    args = request.args
    delay = args.get('delay')
    if delay:
        time.sleep(int(delay))
    return Response("{'Application':'Integra API Tester'}", status=status, mimetype='application/json')

@app.route('/status/random/<status>')
# Retorna o status informado com uma chance de 50%, 200 caso contrário
# Quando rate é informado (número entre 0 e 100) a chance de retorno é rate%
def random(status):
    population = [status, '200']
    args = request.args
    rate = args.get('rate')
    if rate:
        rate = (int(rate))/100
        weights = [rate, 1-rate]
    else:
        weights = [.5, .5]
    status = choices(population, weights)[0]
        
    return Response("{'Application':'Integra API Tester'}", status=status, mimetype='application/json')

@app.route('/status/throttle/<client>')
# Retorna 429 caso limite de requisições tenha sido excedido
# Rate pode ser informado no formato (requisições/min). Caso não informato assumimos 1/min
def throttle(client):
    args = request.args
    rate = args.get('rate')
    if rate:
        rate = int(rate)
    else:
        rate = 1
    grant = throttling (client, rate)
    if grant:
        status = 200
    else:
        status = 429        
    return Response("{'Application':'Integra API Tester'}", status=status, mimetype='application/json')

def throttling (client, rate):    
    reqs = req_list.get(client)
    if not reqs:
        reqs = []
        req_list[client] = reqs
    counter = 0
    now = datetime.now()
    delta = timedelta(seconds = 60)
    threashold = timedelta(minutes = 10)
    for timestamp in reqs:
        if now - timestamp < delta :
            counter += 1
        # Clean timestamps older then threashold
        if now - timestamp > threashold:
            del reqs[reqs.index(timestamp):]
            break
    # Add timestamp always at the beginning
    if counter >= rate:
        return False
    else:
        reqs.insert(0,datetime.now())
        return True

if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    # Set DEBUG as default
    app.run(host="0.0.0.0", port=8000)
