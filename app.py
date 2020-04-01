from flask import Flask, request, jsonify, make_response
from flask import session
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
# TODO: Implement kafka for subscribe global ranking later
# from pykafka import KafkaClient
from service.ranking import find, save, reset
import logging

# Note: I already setup kafka in docker-compose but I still can not connect to kafka
# client = KafkaClient(hosts="0.0.0.0:9092")

app = Flask(__name__)
api = Api(app, version='1.0', title='bluePi memory card service', doc='/api/v1/')
app.config['SECRET_KEY'] = 'bluePi secret key'
CORS(app)

@app.errorhandler(500)
def internal_server_error(e):
	return {
		'status': 500,
		'message': 'Internal Error'
	}

save_ranking_model = api.model('SaveRanking', {
	'clicked': fields.Integer(required=True, description='Clicked amount'),
})
@api.route('/save-ranking')
class SaveRanking(Resource):
	@api.doc(model='SaveRanking', body=save_ranking_model)
	def post(self):
		try:
			data = request.json
			clicked = data["clicked"]
			ranking = save(clicked)
			return {
				'status': 200,
				'data': ranking
			}
		except:
			return {
				'status': 500,
				'message': 'Invalid Input'
			}

@api.route('/find-ranking')
class FindRanking(Resource):
	def get(self):
		return {
			'status': 200,
			'data': {
				'ranking': find(),
			}
		}

@api.route('/reset-ranking')
class ResetRanking(Resource):
	def delete(self):
		try:
			reset()
			return {
				'status': 200,
				'message': 'Success'
			}
		except:
			return {
				'status': 500,
				'message': 'Invalid Input'
			}

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
