from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Play(Page):
    form_model = models.Player
    form_fields = [
        'you1','others1',
        'you2','others2',
        'you3','others3',
        'you4','others4',
        'you5','others5',
        'you6','others6',
        'you7','others7',
        'you8','others8',
        'you9','others9',
        'you10','others10',
        'you11','others11',
        'you12','others12',
        'you13','others13',
        'you14','others14',
        'you15','others15']

    def vars_for_template(self):
        item_order = [self.player.random_order1,self.player.random_order2,
                      self.player.random_order3,self.player.random_order4,
                      self.player.random_order5,self.player.random_order6,
                      self.player.random_order7,self.player.random_order8,
                      self.player.random_order9,self.player.random_order10,
                      self.player.random_order11,self.player.random_order12,
                      self.player.random_order13,self.player.random_order14, self.player.random_order15]

        return {'scale' : Constants.scale,
                'precision': Constants.precision,
                'select_items': Constants.select_items,
                'item_order': item_order,
                'slider_init_type': Constants.slider_init_type
                }

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [
    Play,
    ResultsWaitPage,
    Results
]
