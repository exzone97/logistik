import re, requests, json

from odoo import http
from odoo.exceptions import ValidationError

class Controller(http.Controller):

	BASE_API_URL = 'http://localhost:8069/api/'

	TRACK_API = {
		'url': 'track',
		'params': ['connote']
	}

	CALCULATE_API = {
		'url': 'calculate',
		'params': ['from', 'to', 'weight', 'dimension']
	}

	# butuh parameter namanya connote (nama inputnya connote)
	@http.route('/track', auth='public', methods=['get'])
	def track(self, connote, **kw):
		if not connote:
			raise ValidationError('Connote number is empty')

		connote_regex = re.compile("^[A-Za-z0-9]{5}-[A-Za-z0-9]+-[0-9]{5}$")
		if not connote_regex.match(connote):
			raise ValidationError('Connote number is invalid')

		response = self._getAPIResponse('track', {
			'connote': connote,
		})

		# ganti, ngereturn web sama ngasih responsenya
		# response sama kayak di doc bagian track
		return response

	# butuh parameter city_from, city_to, weight, dimension
	@http.route('/calculate', auth='public', methods=['get'])
	def calculate(self, city_from, city_to, weight, dimension, **kw):
		if not city_from:
			raise ValidationError('City from is empty')
		if not city_to:
			raise ValidationError('City to is empty')
		if not weight:
			raise ValidationError('Weight is empty')
		if not dimension:
			raise ValidationError('Dimension is empty')

		try:
			weight = float(weight)
		except ValueError:
			raise ValidationError('Weight is invalid')

		dimension_regex = re.compile("^[0-9]+x[0-9]+x[0-9]+$")
		if not dimension_regex.match(dimension):
			raise ValidationError('Dimension is invalid')

		response = self._getAPIResponse('calculate', {
			'from': city_from,
			'to': city_to,
			'weight': weight,
			'dimension': dimension,
		})

		# ganti, ngereturn web sama ngasih responsenya
		# response sama kayak di doc bagian calculate
		return response

	def _getAPIResponse(self, api, params):
		api_info = {
			'track': self.TRACK_API,
			'calculate': self.CALCULATE_API,
		}

		if not api in api_info:
			raise Exception(('Invalid API: \'%s\'' % api))

		_api = api_info[api]

		for param in _api['params']:
			if params.get(param) == None:
				raise Exception(('Parameter \'%s\' is not exists when sending API \'%s\'' % (param, api)))

		response = requests.get(('%s%s' % (self.BASE_API_URL, _api['url'])), params=params)
		content = json.loads(response.content)

		return content