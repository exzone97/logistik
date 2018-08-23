import re, requests, json

from odoo import http
from odoo.exceptions import ValidationError

class Controller(http.Controller):

	base_url = 'http://localhost:8069'

	@http.route('/track', auth='public', methods=['get'])
	def track(self, connote, **kw):
		connote_regex = re.compile("^[A-Za-z0-9]{5}-[A-Za-z0-9]+-[0-9]{5}$")

		if not connote_regex.match(connote):
			raise ValidationError('Connote number is invalid.')

		response = requests.get(('%s/api/track' % self.base_url), params={
			'connote': connote,
		})
		content = json.loads(response.content)