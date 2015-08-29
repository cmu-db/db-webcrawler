import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import logging
import json

from crawler.models import *
import utils

## =====================================================================
## LOGGING CONFIGURATION
## =====================================================================

## =====================================================================
## DRIVER
## =====================================================================
class Driver(object):
	
	def __init__(self):
		pass
	
	def drive(self, deployer):
		# get main page
		main_page = deployer.get_main_page()
		
		# recursively crawl all pages and extract the forms
		out = utils.run_command('cd {} && {}'.format(
			os.path.join(os.path.dirname(__file__), 'extract'),
			'scrapy crawl form -o forms.json -a start_url="{}"').format(main_page))

		with open(os.path.join(os.path.dirname(__file__), 'extract', 'forms.json')) as json_forms:
			forms = json.load(json_forms)
		print forms

		# generate input for the forms and submit them
		for form in forms:
			pass
		