import re, json

from odoo import http
from odoo.exceptions import ValidationError

class APIController(http.Controller):

	@http.route('/api/track', auth='public', methods=['get'])
	def connote_tracking(self, **kw):
		connote_number = kw.get('connote')

		return json.dumps([
			{
				'location': 'BDO1',
				'city': 'Bandung',
				'time': '18/08/2018 13:25',
				'status': 'Weighted',
			},
			{
				'location': 'BDO2',
				'city': 'Padalarang',
				'time': '19/08/2018 09:30',
				'status': 'On the way',
			},
		])

	@http.route('/api/calculate', auth='public', methods=['get'])
	def calculate_shipping(self, **kw):
		city_from = kw.get('from')
		city_to = kw.get('to')
		weight = kw.get('weight')
		dimension = kw.get('dimension')

		return json.dumps([
			{
				'product': 'REGULER',
				'cost': '25000',
				'currency': 'Rp.',
			},
			{
				'product': 'PRIORITAS',
				'cost': '35000',
				'currency': 'Rp.',
			},
		])