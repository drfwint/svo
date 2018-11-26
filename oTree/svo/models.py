from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from math import atan, degrees
from settings import LANGUAGE_CODE
author = 'Abdul Majeed Alkattan, Emad Bahrami'

doc = """
      Social Value Orientation
      """

# Config for the game
class Constants(BaseConstants):
    name_in_url = 'svo'
    players_per_group = 2         # The number should be a multiple of 2 in case the matching is RANDOM_DICTATOR.
    num_rounds = 1
    language = LANGUAGE_CODE      # Sets the language in settings.py
    select_items = 'FULL'         # Determins whether we use the first six items to calculate the payoff (PRIMARY) or the 15 items (FULL)
    items_in_random_order = False  # items are presented in random order or according to Murphy
    scale = 1                     # A scaling factor to display the values to the user
    precision = 'INTEGERS'        # TWO_DIGITS_AFTER_POINT or INTEGERS
    # matching = 'RANDOM_DICTATOR'             # Possible values are either 'RING' or 'RANDOM_DICTATOR'
    matching = 'RING'             # Possible values are either 'RING' or 'RANDOM_DICTATOR'

    slider_init_type = 'LEFT'      # 'LEFT' to initialize the slider with the left most value
                                   # 'RIGHT' to initialize with the right most value
                                   # 'RAND' random value in the range
                                   # 'AVG' to initialize the items using average between min and max

# Defining what configs to be saved
class Subsession(BaseSubsession):
    players_per_group = models.IntegerField()
    language = models.CharField(choices=['EN', 'DE', 'IT'])   # English, Deutsch, Italian
    select_items = models.CharField(choices=['PRIMARY', 'FULL'])
    items_in_random_order = models.BooleanField()
    scale = models.DecimalField(max_digits=5, decimal_places=2)
    precision = models.CharField(choices=['INTEGERS', 'TWO_DIGITS_AFTER_POINT'])
    matching = models.CharField(choices=['RING', 'RANDOM_DICTATOR'])
    random_payoff = models.CharField(choices=['RAND', 'SUM'])
    slider_init_type = models.CharField(choices=['LEFT', 'RIGHT', 'RAND', 'AVG'])


    # Runs at initialization time and saves the configs in the database
    def before_session_starts(self):
        self.players_per_group = Constants.players_per_group
        self.language = Constants.language
        self.select_items = Constants.select_items
        self.items_in_random_order = Constants.items_in_random_order
        self.scale = Constants.scale
        self.precision = Constants.precision
        self.matching = Constants.matching
        self.slider_init_type = Constants.slider_init_type

        if Constants.select_items == 'FULL':
            item_order = list(range(1, 16))
        else:
            item_order = list(range(1, 7))

        self.set_item_orders(item_order)


		# Sets the order of items that is going to be shown to each player
    # it can be random for each player or the fixed order according to the paper
    def set_item_orders(self, item_order):
        players = self.get_players()
        if Constants.items_in_random_order:
            random.shuffle(item_order)
        for player in players:
            player.random_order1 = item_order[0]
            player.random_order2 = item_order[1]
            player.random_order3 = item_order[2]
            player.random_order4 = item_order[3]
            player.random_order5 = item_order[4]
            player.random_order6 = item_order[5]
            if Constants.select_items == 'FULL':
                player.random_order7 = item_order[6]
                player.random_order8 = item_order[7]
                player.random_order9 = item_order[8]
                player.random_order10 = item_order[9]
                player.random_order11 = item_order[10]
                player.random_order12 = item_order[11]
                player.random_order13 = item_order[12]
                player.random_order14 = item_order[13]
                player.random_order15 = item_order[14]



class Group(BaseGroup):

    # A function to calculate the SVO angle
    def svo_angle(self, player):
        mean_to_self = 0
        mean_to_others = 0

        mean_to_self+= player.you1
        mean_to_self+= player.you2
        mean_to_self+= player.you3
        mean_to_self+= player.you4
        mean_to_self+= player.you5
        mean_to_self+= player.you6
        mean_to_self = mean_to_self / 6

        mean_to_others+= player.others1
        mean_to_others+= player.others2
        mean_to_others+= player.others3
        mean_to_others+= player.others4
        mean_to_others+= player.others5
        mean_to_others+= player.others6
        mean_to_others = mean_to_others / 6

        
        return degrees(atan((mean_to_others-50) / (mean_to_self - 50)))
            

    # A function to calculate the SVO type
    def svo_type(self, angle):
        if angle > 57.15:
            return 'Altruist'
        if 57.15 >= angle > 22.45:
            return 'Prosocial'
        if 22.45 >= angle > -12.04:
            return 'Individualist'
        if angle <= -12.04:
            return 'Competitive'
    
    # Setting the payoff at random item in case of Ring 
    def ring_payoff(self, sender_player, receiver_player):
        # Case we will consider all the items
        if Constants.select_items == 'FULL':
            rand = random.randint(0, 14)

            sender_player.paid_slider = rand+1
            receiver_player.slider_as_receiver = rand+1

            # TODO initialize the players payoff ?
            if rand == 0:
                sender_player.kept_of_sender = sender_player.you1
                receiver_player.received_from_sender = sender_player.others1

                receiver_player.payoff += sender_player.others1
                sender_player.payoff += sender_player.you1
            elif rand == 1:
                sender_player.kept_of_sender = sender_player.you2
                receiver_player.received_from_sender = sender_player.others2

                receiver_player.payoff += sender_player.others2
                sender_player.payoff += sender_player.you2
            elif rand == 2:
                sender_player.kept_of_sender = sender_player.you3
                receiver_player.received_from_sender = sender_player.others3

                receiver_player.payoff += sender_player.others3
                sender_player.payoff += sender_player.you3
            elif rand == 3:
                sender_player.kept_of_sender = sender_player.you4
                receiver_player.received_from_sender = sender_player.others4

                receiver_player.payoff += sender_player.others4
                sender_player.payoff += sender_player.you4
            elif rand == 4:
                sender_player.kept_of_sender = sender_player.you5
                receiver_player.received_from_sender = sender_player.others5

                receiver_player.payoff += sender_player.others5
                sender_player.payoff += sender_player.you5
            elif rand == 5:
                sender_player.kept_of_sender = sender_player.you6
                receiver_player.received_from_sender = sender_player.others6

                receiver_player.payoff += sender_player.others6
                sender_player.payoff += sender_player.you6
            elif rand == 6:
                sender_player.kept_of_sender = sender_player.you7
                receiver_player.received_from_sender = sender_player.others7

                receiver_player.payoff += sender_player.others7
                sender_player.payoff += sender_player.you7
            elif rand == 7:
                sender_player.kept_of_sender = sender_player.you8
                receiver_player.received_from_sender = sender_player.others8

                receiver_player.payoff += sender_player.others8
                sender_player.payoff += sender_player.you8
            elif rand == 8:
                sender_player.kept_of_sender = sender_player.you9
                receiver_player.received_from_sender = sender_player.others9

                receiver_player.payoff += sender_player.others9
                sender_player.payoff += sender_player.you9
            elif rand == 9:
                sender_player.kept_of_sender = sender_player.you10
                receiver_player.received_from_sender = sender_player.others10

                receiver_player.payoff += sender_player.others10
                sender_player.payoff += sender_player.you10
            elif rand == 10:
                sender_player.kept_of_sender = sender_player.you11
                receiver_player.received_from_sender = sender_player.others11

                receiver_player.payoff += sender_player.others11
                sender_player.payoff += sender_player.you11
            elif rand == 11:
                sender_player.kept_of_sender = sender_player.you12
                receiver_player.received_from_sender = sender_player.others12

                receiver_player.payoff += sender_player.others12
                sender_player.payoff += sender_player.you12
            elif rand == 12:
                sender_player.kept_of_sender = sender_player.you13
                receiver_player.received_from_sender = sender_player.others13

                receiver_player.payoff += sender_player.others13
                sender_player.payoff += sender_player.you13
            elif rand == 13:
                sender_player.kept_of_sender = sender_player.you14
                receiver_player.received_from_sender = sender_player.others14

                receiver_player.payoff += sender_player.others14
                sender_player.payoff += sender_player.you14
            elif rand == 14:
                sender_player.kept_of_sender = sender_player.you15
                receiver_player.received_from_sender = sender_player.others15

                receiver_player.payoff += sender_player.others15
                sender_player.payoff += sender_player.you15

            receiver_player.payoff *= Constants.scale # scaling the payoff

        # Only the first six items
        elif Constants.select_items == 'PRIMARY':

            # random int from the set {0, 1, 2, 3, 4, 5}
            rand = random.randint(0, 5)

            sender_player.paid_slider = rand+1
            receiver_player.slider_as_receiver = rand+1

            if rand == 0:
                sender_player.kept_of_sender = sender_player.you1
                receiver_player.received_from_sender = sender_player.others1

                receiver_player.payoff += sender_player.others1
                sender_player.payoff += sender_player.you1
            elif rand == 1:
                sender_player.kept_of_sender = sender_player.you2
                receiver_player.received_from_sender = sender_player.others2

                receiver_player.payoff += sender_player.others2
                sender_player.payoff += sender_player.you2
            elif rand == 2:
                sender_player.kept_of_sender = sender_player.you3
                receiver_player.received_from_sender = sender_player.others3

                receiver_player.payoff += sender_player.others3
                sender_player.payoff += sender_player.you3
            elif rand == 3:
                sender_player.kept_of_sender = sender_player.you4
                receiver_player.received_from_sender = sender_player.others4

                receiver_player.payoff += sender_player.others4
                sender_player.payoff += sender_player.you4
            elif rand == 4:
                sender_player.kept_of_sender = sender_player.you5
                receiver_player.received_from_sender = sender_player.others5

                receiver_player.payoff += sender_player.others5
                sender_player.payoff += sender_player.you5
            elif rand == 5:
                sender_player.kept_of_sender = sender_player.you6
                receiver_player.received_from_sender = sender_player.others6

                receiver_player.payoff += sender_player.others6
                sender_player.payoff += sender_player.you6
            receiver_player.payoff *= Constants.scale # scaling the payoff


    # Setting the payoff at random item in case of random dictator
    def random_dictator_payoff(self, sender_player, receiver_player):
        # Case we will consider all the items
        if Constants.select_items == 'FULL':

            rand = random.randint(0, 14)

            # TODO  receiver_player is always the receiver which is not the case according to set_payoffs function
            sender_player.paid_slider = rand+1
            receiver_player.slider_as_receiver = rand+1

            if rand == 0:
                # receiver payoff
                receiver_player.payoff = sender_player.others1
                # sender payoff
                sender_player.payoff = sender_player.you1
            elif rand == 1:
                receiver_player.payoff = sender_player.others2
                # sender payoff
                sender_player.payoff = sender_player.you2
            elif rand == 2:
                receiver_player.payoff = sender_player.others3
                # sender payoff
                sender_player.payoff = sender_player.you3
            elif rand == 3:
                receiver_player.payoff = sender_player.others4
                # sender payoff
                sender_player.payoff = sender_player.you4
            elif rand == 4:
                receiver_player.payoff = sender_player.others5
                # sender payoff
                sender_player.payoff = sender_player.you5
            elif rand == 5:
                receiver_player.payoff = sender_player.others6
                # sender payoff
                sender_player.payoff = sender_player.you6
            elif rand == 6:
                receiver_player.payoff = sender_player.others7
                # sender payoff
                sender_player.payoff = sender_player.you7
            elif rand == 7:
                receiver_player.payoff = sender_player.others8
                # sender payoff
                sender_player.payoff = sender_player.you8
            elif rand == 8:
                receiver_player.payoff = sender_player.others9
                # sender payoff
                sender_player.payoff = sender_player.you9
            elif rand == 9:
                receiver_player.payoff = sender_player.others10
                # sender payoff
                sender_player.payoff = sender_player.you10
            elif rand == 10:
                receiver_player.payoff = sender_player.others11
                # sender payoff
                sender_player.payoff = sender_player.you11
            elif rand == 11:
                receiver_player.payoff = sender_player.others12
                # sender payoff
                sender_player.payoff = sender_player.you12
            elif rand == 12:
                receiver_player.payoff = sender_player.others13
                # sender payoff
                sender_player.payoff = sender_player.you13
            elif rand == 13:
                receiver_player.payoff = sender_player.others14
                # sender payoff
                sender_player.payoff = sender_player.you14
            elif rand == 14:
                receiver_player.payoff = sender_player.others15
                # sender payoff
                sender_player.payoff = sender_player.you15

            receiver_player.received_from_sender = receiver_player.payoff
            sender_player.kept_of_sender = sender_player.payoff
            receiver_player.payoff *= Constants.scale                      # scaling the payoff
            sender_player.payoff *= Constants.scale


        elif Constants.select_items == 'PRIMARY':

            rand = random.randint(0, 5)

            # TODO  receiver_player is always the receiver which is not the case according to set_payoffs function
            sender_player.paid_slider = rand+1
            receiver_player.slider_as_receiver = rand+1

            if rand == 0:
                receiver_player.payoff = sender_player.others1
                sender_player.payoff = sender_player.you1
            elif rand == 1:
                receiver_player.payoff = sender_player.others2
                sender_player.payoff = sender_player.you2
            elif rand == 2:
                receiver_player.payoff = sender_player.others3
                sender_player.payoff = sender_player.you3
            elif rand == 3:
                receiver_player.payoff = sender_player.others4
                sender_player.payoff = sender_player.you4
            elif rand == 4:
                receiver_player.payoff = sender_player.others5
                sender_player.payoff = sender_player.you5
            elif rand == 5:
                receiver_player.payoff = sender_player.others6
                sender_player.payoff = sender_player.you6

            receiver_player.received_from_sender = receiver_player.payoff
            sender_player.kept_of_sender = sender_player.payoff

            receiver_player.payoff *= Constants.scale
            sender_player.payoff *= Constants.scale



    # Discretize the last 9 items in the paper to ranges and options
    def option_number(self, item_number, you, other):
        # Then this is you option
        if you > 0:
            if item_number == 7:
                if 72 > you:
                    return 9
                elif 76 > you >= 72:
                    return 8
                elif 79.5 > you >= 76:
                    return 7
                elif 83 > you >= 79.5:
                    return 6
                elif 87 > you >= 83:
                    return 5
                elif 91 > you >= 87:
                    return 4
                elif 94.5 > you >= 91:
                    return 3
                elif 98 > you >= 94.5:
                    return 2
                elif you >= 98:
                    return 1

            elif item_number == 8:
                if you > 99.5:
                    return 9
                elif 99.5 >= you > 98.5:
                    return 8
                elif 98.5 >= you > 97:
                    return 7
                elif 97 >= you > 95.5:
                    return 6
                elif 95.5 >= you > 94.5:
                    return 5
                elif 94.5 >= you > 93.5:
                    return 4
                elif 93.5 >= you > 92:
                    return 3
                elif 92 >= you > 90.5:
                    return 2
                elif 90.5 >= you:
                    return 1
                
            elif item_number == 9:
                if 53 > you:
                    return 9
                elif 59.5 > you >= 53:
                    return 8
                elif 66 > you >= 59.5:
                    return 7
                elif 72 > you >= 66:
                    return 6
                elif 78 > you >= 72:
                    return 5
                elif 84.5 > you >= 78:
                    return 4
                elif 91 > you >= 84.5:
                    return 3
                elif 97 > you >= 91:
                    return 2
                elif you >= 97:
                    return 1

            elif item_number == 10:
                if 90.5 >= you:
                    return 9
                elif 92 >= you > 90.5:
                    return 8
                elif 93.5 >= you > 92:
                    return 7
                elif 94.5 >= you > 93.5:
                    return 6
                elif 95.5 >= you > 94.5:
                    return 5
                elif 97 >= you > 95.5:
                    return 4
                elif 98.5 >= you > 97:
                    return 3
                elif 99.5 >= you > 98.5:
                    return 2
                elif you >= 99.5:
                    return 1

            elif item_number == 11:
                if you > 98:
                    return 9
                elif 98 >= you > 94.5:
                    return 8
                elif 94.5 >= you > 91:
                    return 7
                elif 91 >= you > 87:
                    return 6
                elif 87 >= you > 83:
                    return 5
                elif 83 >= you > 79.5:
                    return 4
                elif 79.5 >= you > 76:
                    return 3
                elif 76 >= you > 72:
                    return 2
                elif you <= 72:
                    return 1

            elif item_number == 12:
                if you > 97:
                    return 9
                elif 97 >= you > 91:
                    return 8
                elif 91 >= you > 84.5:
                    return 7
                elif 84.5 >= you > 78:
                    return 6
                elif 78 >= you > 72:
                    return 5
                elif 72 >= you > 66:
                    return 4
                elif 66 >= you > 59.5:
                    return 3
                elif 59.5 >= you > 53:
                    return 2
                elif you <= 53:
                    return 1

            elif item_number == 13:
                if you > 97:
                    return 9
                elif 97 >= you > 91:
                    return 8
                elif 91 >= you > 84.5:
                    return 7
                elif 84.5 >= you > 78:
                    return 6
                elif 78 >= you > 72:
                    return 5
                elif 72 >= you > 66:
                    return 4
                elif 66 >= you > 59.5:
                    return 3
                elif 59.5 >= you > 53:
                    return 2
                elif 53 >= you:
                    return 1

            elif item_number == 14:
                if 72 > you:
                    return 9
                elif 76 > you >= 72:
                    return 8
                elif 79.5 > you >= 76:
                    return 7
                elif 83 > you >= 79.5:
                    return 6
                elif 87 > you >= 83:
                    return 5
                elif 91 > you >= 87:
                    return 4
                elif 94.5 > you >= 91:
                    return 3
                elif 98 > you >= 94.5:
                    return 2
                elif you >= 98:
                    return 1

            elif item_number == 15:
                if you > 99.5:
                    return 9
                elif 99.5 >= you > 98.5:
                    return 8
                elif 98.5 >= you > 97:
                    return 7
                elif 97 >= you > 95.5:
                    return 6
                elif 95.5 >= you > 94.5:
                    return 5
                elif 94.5 >= you > 93.5:
                    return 4
                elif 93.5 >= you > 92:
                    return 3
                elif 92 >= you > 90.5:
                    return 2
                elif 90.5 >= you:
                    return 1

        # Then this is an other option
        elif other > 0:
            if item_number == 7:
                if other > 97:
                    return 9
                elif 97 >= other > 91:
                    return 8
                elif 91 >= other > 84.5:
                    return 7
                elif 84.5 >= other > 78:
                    return 6
                elif 78 >= other > 72:
                    return 5
                elif 72 >= other > 66:
                    return 4
                elif 66 >= other > 59.5:
                    return 3
                elif 59.5 >= other > 53:
                    return 2
                elif other <= 53:
                    return 1

            elif item_number == 8:
                if 90.5 >= other:
                    return 9
                elif 92 >= other > 90.5:
                    return 8
                elif 93.5 >= other > 92:
                    return 7
                elif 94.5 >= other > 93.5:
                    return 6
                elif 95.5 >= other > 94.5:
                    return 5
                elif 97 >= other > 95.5:
                    return 4
                elif 98.5 >= other > 97:
                    return 3
                elif 99.5 >= other > 98.5:
                    return 2
                elif other >= 99.5:
                    return 1

            elif item_number == 9:
                if other > 98:
                    return 9
                elif 98 >= other > 94.5:
                    return 8
                elif 94.5 >= other > 91:
                    return 7
                elif 91 >= other > 87:
                    return 6
                elif 87 >= other > 83:
                    return 5
                elif 83 >= other > 79.5:
                    return 4
                elif 79.5 >= other > 76:
                    return 3
                elif 76 >= other > 72:
                    return 2
                elif other <= 72:
                    return 1

            elif item_number == 10:
                if other > 98:
                    return 9
                elif 98 >= other > 94.5:
                    return 8
                elif 94.5 >= other > 91:
                    return 7
                elif 91 >= other > 87:
                    return 6
                elif 87 >= other > 83:
                    return 5
                elif 83 >= other > 79.5:
                    return 4
                elif 79.5 >= other > 76:
                    return 3
                elif 76 >= other > 72:
                    return 2
                elif other <= 72:
                    return 1

            elif item_number == 11:
                if 72 > other:
                    return 9
                elif 76 > other >= 72:
                    return 8
                elif 79.5 > other >= 76:
                    return 7
                elif 83 > other >= 79.5:
                    return 6
                elif 87 > other >= 83:
                    return 5
                elif 91 > other >= 87:
                    return 4
                elif 94.5 > other >= 91:
                    return 3
                elif 98 > other >= 94.5:
                    return 2
                elif other >= 98:
                    return 1

            elif item_number == 12:
                if 90.5 >= other:
                    return 9
                elif 92 >= other > 90.5:
                    return 8
                elif 93.5 >= other > 92:
                    return 7
                elif 94.5 >= other > 93.5:
                    return 6
                elif 95.5 >= other > 94.5:
                    return 5
                elif 97 >= other > 95.5:
                    return 4
                elif 98.5 >= other > 97:
                    return 3
                elif 99.5 >= other > 98.5:
                    return 2
                elif other >= 99.5:
                    return 1

            elif item_number == 13:
                if 53 > other:
                    return 9
                elif 59.5 > other >= 53:
                    return 8
                elif 66 > other >= 59.5:
                    return 7
                elif 72 > other >= 66:
                    return 6
                elif 78 > other >= 72:
                    return 5
                elif 84.5 > other >= 78:
                    return 4
                elif 91 > other >= 84.5:
                    return 3
                elif 97 > other >= 91:
                    return 2
                elif other >= 97:
                    return 1

            elif item_number == 14:
                if other > 99.5:
                    return 9
                elif 99.5 >= other > 98.5:
                    return 8
                elif 98.5 >= other > 97:
                    return 7
                elif 97 >= other > 95.5:
                    return 6
                elif 95.5 >= other > 94.5:
                    return 5
                elif 94.5 >= other > 93.5:
                    return 4
                elif 93.5 >= other > 92:
                    return 3
                elif 92 >= other > 90.5:
                    return 2
                elif 90.5 >= other:
                    return 1

            elif item_number == 15:
                if 53 > other:
                    return 9
                elif 59.5 > other >= 53:
                    return 8
                elif 66 > other >= 59.5:
                    return 7
                elif 72 > other >= 66:
                    return 6
                elif 78 > other >= 72:
                    return 5
                elif 84.5 > other >= 78:
                    return 4
                elif 91 > other >= 84.5:
                    return 3
                elif 97 > other >= 91:
                    return 2
                elif other >= 97:
                    return 1
            
    def inequality_aversion_score(self, svo_type, player): 
        if svo_type == 'Prosocial':
            item7_option = self.option_number(7, player.you7, 0)
            item8_option = self.option_number(8, player.you8, 0)
            item9_option = self.option_number(9, player.you9, 0)
            item10_option = self.option_number(10, player.you10, 0)
            item11_option = self.option_number(11, player.you11, 0)
            item12_option = self.option_number(12, player.you12, 0)
            item13_option = self.option_number(13, player.you13, 0)
            item14_option = self.option_number(14, player.you14, 0)
            item15_option = self.option_number(15, player.you15, 0)

            avg_dist_to_equality = ((abs(item7_option - 6) / 8.) +
            (abs(item8_option - 5) / 8.) +
            (abs(item9_option - 4) / 8.) +
            (abs(item10_option - 7) / 8.) +
            (abs(item11_option - 5) / 8.) +
            (abs(item12_option - 8) / 8.) +
            (abs(item13_option - 5) / 8.) +
            (abs(item14_option - 3) / 8.) +
            (abs(item15_option - 2) / 8.) ) / 9.

            avg_dist_to_joint = ((abs(item7_option - 9) / 8.) +
            0 +
            (abs(item9_option - 1) / 8.) +
            (abs(item10_option - 9) / 8.) +
            0 +
            (abs(item12_option - 9) / 8.) +
            0 +
            (abs(item14_option - 1) / 8.) +
            (abs(item15_option - 1) / 8.) ) / 6.

            avg_dist_to_altruist = ((abs(item7_option - 9) / 8.) +
            (abs(item8_option - 1) / 8.) +
            (abs(item9_option - 9) / 8.) +
            (abs(item10_option - 9) / 8.) +
            (abs(item11_option - 1) / 8.) +
            (abs(item12_option - 1) / 8.) +
            (abs(item13_option - 1) / 8.) +
            (abs(item14_option - 9) / 8.) +
            (abs(item15_option - 1) / 8.) ) / 9.

            avg_dist_to_indiv = ((abs(item7_option - 1) / 8.) +
            (abs(item8_option - 9) / 8.) +
            (abs(item9_option - 1) / 8.) +
            (abs(item10_option - 1) / 8.) +
            (abs(item11_option - 9) / 8.) +
            (abs(item12_option - 9) / 8.) +
            (abs(item13_option - 9) / 8.) +
            (abs(item14_option - 1) / 8.) +
            (abs(item15_option - 9) / 8.) ) / 9.

            altru_indiv = (avg_dist_to_equality <= avg_dist_to_indiv
                           and avg_dist_to_equality <= avg_dist_to_altruist
                           and avg_dist_to_joint <= avg_dist_to_indiv
                           and avg_dist_to_joint <= avg_dist_to_altruist)

            if altru_indiv:
                inequality_aversion_score = avg_dist_to_equality /(avg_dist_to_equality + avg_dist_to_joint)
                return inequality_aversion_score
            else:
                return -99
        else:
            return -99

    # A function to calculate the payoff for the players
    def set_payoffs(self):
        players = self.get_players()                                        # Get all the players for this game
        for p in players:
            p.svo_angle = self.svo_angle(p)                                 # Calculate the SVO angle
            p.svo_type = self.svo_type(p.svo_angle)                               # Check what is the SVO type of the player
            if Constants.select_items == 'FULL':                            # Calculate the inequality_aversion_score
                p.inequality_aversion_score = self.inequality_aversion_score(p.svo_type, p)

            
        # Case of RING matching 
        if Constants.matching == 'RING':
            for i, p in enumerate(players):
                self.ring_payoff(p, players[(i+1)%len(players)])                    
        
        # Case of RANDOM_DICTATOR matching
        elif Constants.matching == 'RANDOM_DICTATOR':
                for i in range(0, len(players),2):                          # for all possible groups
                    rand_first_group = random.randint(0, 1)                 # A random value to choose either player A or B
                    if rand_first_group == 0:                               # Choose member A as the sender and B as the receiver.
                        sender_player = players[i]
                        receiver_player = players[i+1]
                        self.random_dictator_payoff(sender_player, receiver_player)         # Set the payoff
                    else:                                                   # Choose member B as the sender and A as the receiver
                        receiver_player = players[i+1]
                        sender_player = players[i]
                        self.random_dictator_payoff(sender_player, receiver_player)         # Set the payoff

                    # TODO it seems that this is not correct
                    # self.random_dictator_payoff(a_player, b_player)         # Set the payoff

# Player base class which contains the values for a single player per game
class Player(BasePlayer):
    # you1 represents the amount of money that the user has chosen for himself for the first item 
    # others1 represents the amount of money that the user has chosen for others for the first item.
    you1 = models.DecimalField(max_digits=5, decimal_places=2)
    others1 = models.DecimalField(max_digits=5, decimal_places=2)

    # Same as above but for item 2 in the paper
    you2 = models.DecimalField(max_digits=5, decimal_places=2)
    others2 = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Same as above but for item 3 in the paper
    you3 = models.DecimalField(max_digits=5, decimal_places=2)
    others3 = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Same as above but for item 2 in the paper and so on.
    you4 = models.DecimalField(max_digits=5, decimal_places=2)
    others4 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you5 = models.DecimalField(max_digits=5, decimal_places=2)
    others5 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you6 = models.DecimalField(max_digits=5, decimal_places=2)
    others6 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you7 = models.DecimalField(max_digits=5, decimal_places=2)
    others7 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you8 = models.DecimalField(max_digits=5, decimal_places=2)
    others8 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you9 = models.DecimalField(max_digits=5, decimal_places=2)
    others9 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you10 = models.DecimalField(max_digits=5, decimal_places=2)
    others10 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you11 = models.DecimalField(max_digits=5, decimal_places=2)
    others11 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you12 = models.DecimalField(max_digits=5, decimal_places=2)
    others12 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you13 = models.DecimalField(max_digits=5, decimal_places=2)
    others13 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you14 = models.DecimalField(max_digits=5, decimal_places=2)
    others14 = models.DecimalField(max_digits=5, decimal_places=2)
    
    you15 = models.DecimalField(max_digits=5, decimal_places=2)
    others15 = models.DecimalField(max_digits=5, decimal_places=2)

    # order of item 1 in RANDOM order
    random_order1 = models.IntegerField(initial=-1)
    random_order2 = models.IntegerField(initial=-1)
    random_order3 = models.IntegerField(initial=-1)
    random_order4 = models.IntegerField(initial=-1)
    random_order5 = models.IntegerField(initial=-1)
    random_order6 = models.IntegerField(initial=-1)
    random_order7 = models.IntegerField(initial=-1)
    random_order8 = models.IntegerField(initial=-1)
    random_order9 = models.IntegerField(initial=-1)
    random_order10 = models.IntegerField(initial=-1)
    random_order11 = models.IntegerField(initial=-1)
    random_order12 = models.IntegerField(initial=-1)
    random_order13 = models.IntegerField(initial=-1)
    random_order14 = models.IntegerField(initial=-1)
    random_order15 = models.IntegerField(initial=-1)

    svo_angle = models.DecimalField(max_digits=7, decimal_places=2)
    svo_type = models.CharField(choices=['Altruist', 'Prosocial', 'Individualist', 'Competitive'])
    inequality_aversion_score = models.DecimalField(max_digits=7, decimal_places=2)

    # slider selected for payment as sender
    paid_slider = models.IntegerField(initial=-1)

    # slider selected for payment as receiver for matching=RING
    slider_as_receiver = models.IntegerField(initial=-1)

    # amount kept by the sender
    kept_of_sender = models.DecimalField(max_digits=5, decimal_places=2)

    # amount received from the sender
    received_from_sender = models.DecimalField(max_digits=5, decimal_places=2)

