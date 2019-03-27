from os import environ
from django.utils.translation import gettext_lazy as _

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}


SESSION_CONFIGS = [
{
    'name': 'svo',
    'display_name': "Social Value Orientation",
    'num_demo_participants': 4,
    'app_sequence': ['svo'],
		'matching': 'RING',
		'select_items': 'FULL',
		'items_in_random_order': False,
		'scale': 0.1 ,
		'slider_init': 'LEFT',
		'random_payoff': 'RAND',
		'precision': 'INTEGERS',
		'language': 'de',
		'doc': """
    	Edit the 'matching' parameter to select RING matching or 
    	RANDOM_DICTATOR matching.</br>
    	Edit the 'select_items' parameter to whether we use the first six items 
    	to calculate the payoff (PRIMARY) or the 15 items (FULL).</br>
    	Edit the 'scale' parameter to scale the slider values.</br>
    	Edit the 'slider_init' parameter with LEFT, RIGHT, RAND or AVG to initialize the slider.</br>
    	Edit the 'random_payoff' parameter with RAND or SUM to determine the way to calculate the payoff.</br>
    	Edit the 'precision' parameter with TWO_DIGITS_AFTER_POINT or INTEGERS.
    """
  }
]


# ISO-639 code
# for example: de, fr, it, en
# LANGUAGE_CODE = 'en'


# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False
# POINTS_DECIMAL_PLACES = 2

ROOMS = []


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = '(5m5%_xax9c^vi95ztd7*h0-8*1w*^v2&=y*m_2&ncuss)cut8'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
