from flask import Flask, request
from flask_cors import CORS, cross_origin
from .utils import connect_to_smtp_server
import json

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
	return json.dumps({'json sagt:': 'hallo i bims, der json'}), 200


@app.route('/mail', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'], methods=['POST'],
			  expose_headers=['Content-Type', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
							  'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'], origins=['*'])
def send_mail():
	print(str(request))
	data = json.loads(request.data)
	print(f'data: {data}')
	status_code = connect_to_smtp_server(data)
	print(f'status_code: {status_code}')
	if status_code == 200:
		return json.dumps({'response': 'sent'}), status_code
	else:
		return json.dumps({'response': 'failed'}), status_code


