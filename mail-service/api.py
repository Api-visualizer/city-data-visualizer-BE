from flask import Flask, request
from .utils import connect_to_smtp_server
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	return json.dumps({'json sagt:': 'hallo i bims, der json'}), 200


@app.route('/mail', methods=['POST'])
def send_mail():
	data = json.loads(request.data.decode('utf-8'))
	print(f'data: {data}')
	status_code = connect_to_smtp_server(data)
	print(f'status_code: {status_code}')
	if status_code == 200:
		return json.dumps({'response': 'success'}), status_code
	else:
		return json.dumps({'response': 'failed'}), status_code


