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
	@http.route('/track', auth='public', methods=['get'], website=True)
	def track(self, connote, **kw):
		if not connote:
			message = 'Connote number is empty'
			return self._checkMessage(message, 'website_legapaket.tracking')

		connote_regex = re.compile("^[A-Za-z0-9]{5}-[A-Za-z0-9]+-[0-9]{5}$")
		if not connote_regex.match(connote):
			message = 'Connote number is invalid'
			return self._checkMessage(message, 'website_legapaket.tracking')

		response = self._getAPIResponse('track', {
			'connote': connote,
		})

		if not response:
			return self._checkMessage(message, 'website_legapaket.tracking')

		return http.request.render('website_legapaket.tracking', {
			'responses' : response,
			'connote' : connote.replace("-",""),
		})

	# butuh parameter city_from, city_to, weight, dimension
	@http.route('/calculate', auth='public', methods=['get'], website=True)
	def calculate(self, city_from, city_to, weight, dimension, **kw):
		if not city_from:
			message = 'City from is empty'
			return self._checkMessage(message, 'website_legapaket.calculate')

		if not city_to:
			message = 'City to is empty'
			return self._checkMessage(message, 'website_legapaket.calculate')

		if not weight:
			message = 'Weight is empty'
			return self._checkMessage(message, 'website_legapaket.calculate')

		if not dimension:
			message = 'Dimension is empty'
			return self._checkMessage(message, 'website_legapaket.calculate')

		try:
			weight = float(weight)
		except ValueError:
			message = 'Weight is Invalid'
			return self._checkMessage(message, 'website_legapaket.calculate')

		if weight<0:
			message = 'Weight < 0'
			return self._checkMessage(message, 'website_legapaket.calculate')

		# dimension_regex = re.compile("^[0-9]+x[0-9]+x[0-9]+$")
		dimension_regex = re.compile("^[-+]?[0-9]*\.?[0-9]+x[-+]?[0-9]*\.?[0-9]+x[-+]?[0-9]*\.?[0-9]+$")
		if not dimension_regex.match(dimension):
			message = 'Dimension is Invalid'
			return self._checkMessage(message, 'website_legapaket.calculate')

		response = self._getAPIResponse('calculate', {
			'from': city_from,
			'to': city_to,
			'weight': weight,
			'dimension': dimension,
		})

		if not response:
			return self._checkMessage(message, 'website_legapaket.calculate')

		return http.request.render('website_legapaket.calculate', {
			'responses' : response,
			'city_from' : city_from,
			'city_to' : city_to,
			'weight' : weight,
			'dimension' : dimension,

		})

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

		try:
			content = json.loads(response.content)
			return content
		except Exception:
			return False

	def _checkMessage(self, message, view):
		if message:
			return http.request.render(view, {
				'message': message
			})