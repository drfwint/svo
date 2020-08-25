from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from django.utils import translation
from django import http
from django.conf import settings


class Play(Page):
	form_model = 'player'
	form_fields = [
		'input_self_1','input_other_1',
		'input_self_2','input_other_2',
		'input_self_3','input_other_3',
		'input_self_4','input_other_4',
		'input_self_5','input_other_5',
		'input_self_6','input_other_6',
		'input_self_7','input_other_7',
		'input_self_8','input_other_8',
		'input_self_9','input_other_9',
		'input_self_10','input_other_10',
		'input_self_11','input_other_11',
		'input_self_12','input_other_12',
		'input_self_13','input_other_13',
		'input_self_14','input_other_14',
		'input_self_15','input_other_15']

	def is_displayed(self):
		translation.activate(self.session.vars['django_language'])
		return True

	def vars_for_template(self):
		item_order = [self.player.random_order1,self.player.random_order2,
									self.player.random_order3,self.player.random_order4,
									self.player.random_order5,self.player.random_order6,
									self.player.random_order7,self.player.random_order8,
									self.player.random_order9,self.player.random_order10,
									self.player.random_order11,self.player.random_order12,
									self.player.random_order13,self.player.random_order14, self.player.random_order15]

		return {'scale' : self.subsession.scale,
						'precision': self.subsession.precision,
						'select_items': self.subsession.select_items,
						'item_order': item_order,
						'slider_init': self.subsession.slider_init
						}

class ResultsWaitPage(WaitPage):

	def is_displayed(self):
		translation.activate(self.session.vars['django_language'])
		return True

	def after_all_players_arrive(self):
		self.group.set_payoffs()


class Results(Page):
  pass


page_sequence = [
    Play,
    ResultsWaitPage,
    Results
]
