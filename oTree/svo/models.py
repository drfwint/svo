from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.utils import translation
from django import http
from django.conf import settings

import random
from math import atan, degrees, sqrt, tan, pi
from .utils import compute_line, intersection_point, distance, max_tuple

author = 'Abdul Majeed Alkattan, Emad Bahrami'

doc = """
      Social Value Orientation
      """

# Config for the game
class Constants(BaseConstants):
    name_in_url = 'svo'
    players_per_group = None         # The number should be a multiple of 2 in case the matching is RANDOM_DICTATOR.
    num_rounds = 1


    slider_end_points = {
        'item7':  [(100, 50), (70, 100)],
        'item8':  [(90, 100), (100, 90)],
        'item9':  [(100, 70), (50, 100)],
        'item10': [(100, 70), (90, 100)],
        'item11': [(70, 100), (100, 70)],
        'item12': [(50, 100), (100, 90)],
        'item13': [(50, 100), (100, 50)],
        'item14': [(100, 90), (70, 100)],
        'item15': [(90, 100), (100, 50)]}

    # representing line y=x using Ax+By=C by A, B, C
    identity_line = (1, -1, 0)


    line = compute_line
    id_line = identity_line

    # intersection point of the slider line and y=x line
    mid_points = {}

    # store the joint max of each item
    joint_max = {}

    # points that always maximize other
    altruist_points = {}

    # points that always maximize self
    individualist_points = {}

    secondary_items = []

    for item, points in slider_end_points.items():
        mid_points[item] = intersection_point(id_line, line(*points))

        joint_max[item] = max_tuple(*points, sum)

        altruist_points[item] = max_tuple(*points, lambda x: x[1])

        individualist_points[item] = max_tuple(*points, lambda x: x[0])

        secondary_items.append(item)


# Defining what configs to be saved
class Subsession(BaseSubsession):
    players_per_group = models.IntegerField()
    language = models.StringField(choices=['EN', 'DE', 'IT', 'FR'])   # English, Deutsch, Italian
    select_items = models.StringField(choices=['PRIMARY', 'FULL'])
    items_in_random_order = models.BooleanField()
    scale = models.FloatField()
    precision = models.StringField(choices=['INTEGERS', 'TWO_DIGITS_AFTER_POINT'])
    matching = models.StringField(choices=['RING', 'RANDOM_DICTATOR'])
    random_payoff = models.StringField(choices=['RAND', 'SUM'])
    slider_init = models.StringField(choices=['LEFT', 'RIGHT', 'RAND', 'AVG'])


    def creating_session(self):
        group_matrix = []
        players = self.get_players()
        num_players = len(self.get_players())
        if self.session.config['matching'] == 'RING':
            ppg = num_players
            if ppg<2:
                raise ValueError("Number of player for RING matching should be at least 2")

        elif self.session.config['matching'] == 'RANDOM_DICTATOR':
            ppg = 2

        if num_players%ppg != 0:
            raise ValueError("Number of player must be multiple of {}".format(ppg))


        for i in range(0, len(players), ppg):
            group_matrix.append(players[i:i + ppg])
        self.set_group_matrix(group_matrix)
        
        # Runs at initialization time and saves the configs in the database
        self.players_per_group = Constants.players_per_group
        self.language = self.session.config['language'].lower()
        # self.select_items = Constants.select_items
        self.select_items = self.session.config['select_items'].upper()

        # self.items_in_random_order = Constants.items_in_random_order
        self.items_in_random_order = self.session.config['items_in_random_order']

        self.scale = float(self.session.config['scale'])

        self.precision = self.session.config['precision'].upper()
        # self.matching = Constants.matching
        self.matching = self.session.config['matching'].upper()
        self.slider_init = self.session.config['slider_init'].upper()
        self.random_payoff = self.session.config['random_payoff'].upper()

        if self.language in ('de', 'en', 'fr', 'it'):
            user_language = self.language
        else:
            raise ValueError("{} is not a valid language code.")


        self.session.vars['django_language'] = user_language

        translation.activate(user_language)

        if self.select_items == 'FULL':
            item_order = list(range(1, 16))
        else:
            item_order = list(range(1, 7))

        self.set_item_orders(item_order)

	# Sets the order of items that is going to be shown to each player
    # it can be random for each player or the fixed order according to the paper
    def set_item_orders(self, item_order):
        players = self.get_players()

        for player in players:
            if self.items_in_random_order:
                random.shuffle(item_order)
            player.random_order1 = item_order[0]
            player.random_order2 = item_order[1]
            player.random_order3 = item_order[2]
            player.random_order4 = item_order[3]
            player.random_order5 = item_order[4]
            player.random_order6 = item_order[5]
            if self.select_items == 'FULL':
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

        mean_to_self+= player.input_self_1
        mean_to_self+= player.input_self_2
        mean_to_self+= player.input_self_3
        mean_to_self+= player.input_self_4
        mean_to_self+= player.input_self_5
        mean_to_self+= player.input_self_6
        mean_to_self = mean_to_self / 6

        mean_to_others+= player.input_other_1
        mean_to_others+= player.input_other_2
        mean_to_others+= player.input_other_3
        mean_to_others+= player.input_other_4
        mean_to_others+= player.input_other_5
        mean_to_others+= player.input_other_6
        mean_to_others = mean_to_others / 6


        return degrees(atan((float(mean_to_others) - self.subsession.scale*50) / (float(mean_to_self) - self.subsession.scale*50)))

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

        if self.subsession.random_payoff == 'SUM':
            # sum of the amount received from the sender player (slider 1 to 6)
            receiver_player.payoff += sender_player.input_other_1 + sender_player.input_other_2 + \
                                      sender_player.input_other_3 + sender_player.input_other_4 + \
                                      sender_player.input_other_5 + sender_player.input_other_6

            receiver_player.received_from_sender = sender_player.input_other_1 + sender_player.input_other_2 + \
                                                   sender_player.input_other_3 + sender_player.input_other_4 + \
                                                   sender_player.input_other_5 + sender_player.input_other_6
            receiver_player.received_from_sender = float(receiver_player.received_from_sender)

            sender_player.payoff += sender_player.input_self_1 + sender_player.input_self_2 + \
                                    sender_player.input_self_3 + sender_player.input_self_4 + \
                                    sender_player.input_self_5 + sender_player.input_self_6

            sender_player.kept_of_sender = sender_player.input_self_1 + sender_player.input_self_2 + \
                                           sender_player.input_self_3 + sender_player.input_self_4 + \
                                           sender_player.input_self_5 + sender_player.input_self_6
            sender_player.kept_of_sender = float(sender_player.kept_of_sender)


        # Only the first six items
        if self.subsession.select_items == 'PRIMARY':

            if self.subsession.random_payoff == 'RAND':

                # random int from the set {0, 1, 2, 3, 4, 5}
                rand = random.randint(0, 5)
                sender_player.paid_slider = rand + 1
                receiver_player.slider_as_receiver = rand + 1

                if rand == 0:
                    sender_player.kept_of_sender = sender_player.input_self_1
                    receiver_player.received_from_sender = sender_player.input_other_1

                    receiver_player.payoff += sender_player.input_other_1
                    sender_player.payoff += sender_player.input_self_1
                elif rand == 1:
                    sender_player.kept_of_sender = sender_player.input_self_2
                    receiver_player.received_from_sender = sender_player.input_other_2

                    receiver_player.payoff += sender_player.input_other_2
                    sender_player.payoff += sender_player.input_self_2
                elif rand == 2:
                    sender_player.kept_of_sender = sender_player.input_self_3
                    receiver_player.received_from_sender = sender_player.input_other_3

                    receiver_player.payoff += sender_player.input_other_3
                    sender_player.payoff += sender_player.input_self_3
                elif rand == 3:
                    sender_player.kept_of_sender = sender_player.input_self_4
                    receiver_player.received_from_sender = sender_player.input_other_4

                    receiver_player.payoff += sender_player.input_other_4
                    sender_player.payoff += sender_player.input_self_4
                elif rand == 4:
                    sender_player.kept_of_sender = sender_player.input_self_5
                    receiver_player.received_from_sender = sender_player.input_other_5

                    receiver_player.payoff += sender_player.input_other_5
                    sender_player.payoff += sender_player.input_self_5
                elif rand == 5:
                    sender_player.kept_of_sender = sender_player.input_self_6
                    receiver_player.received_from_sender = sender_player.input_other_6

                    receiver_player.payoff += sender_player.input_other_6
                    sender_player.payoff += sender_player.input_self_6

                # receiver_player.payoff *= Constants.scale # scaling the payoff


        # Case we will consider all the items
        elif self.subsession.select_items == 'FULL':

            if self.subsession.random_payoff == 'RAND':

                rand = random.randint(0, 14)
                sender_player.paid_slider = rand+1
                receiver_player.slider_as_receiver = rand+1

                if rand == 0:
                    sender_player.kept_of_sender = sender_player.input_self_1
                    receiver_player.received_from_sender = sender_player.input_other_1

                    receiver_player.payoff += sender_player.input_other_1
                    sender_player.payoff += sender_player.input_self_1
                elif rand == 1:
                    sender_player.kept_of_sender = sender_player.input_self_2
                    receiver_player.received_from_sender = sender_player.input_other_2

                    receiver_player.payoff += sender_player.input_other_2
                    sender_player.payoff += sender_player.input_self_2
                elif rand == 2:
                    sender_player.kept_of_sender = sender_player.input_self_3
                    receiver_player.received_from_sender = sender_player.input_other_3

                    receiver_player.payoff += sender_player.input_other_3
                    sender_player.payoff += sender_player.input_self_3
                elif rand == 3:
                    sender_player.kept_of_sender = sender_player.input_self_4
                    receiver_player.received_from_sender = sender_player.input_other_4

                    receiver_player.payoff += sender_player.input_other_4
                    sender_player.payoff += sender_player.input_self_4
                elif rand == 4:
                    sender_player.kept_of_sender = sender_player.input_self_5
                    receiver_player.received_from_sender = sender_player.input_other_5

                    receiver_player.payoff += sender_player.input_other_5
                    sender_player.payoff += sender_player.input_self_5
                elif rand == 5:
                    sender_player.kept_of_sender = sender_player.input_self_6
                    receiver_player.received_from_sender = sender_player.input_other_6

                    receiver_player.payoff += sender_player.input_other_6
                    sender_player.payoff += sender_player.input_self_6
                elif rand == 6:
                    sender_player.kept_of_sender = sender_player.input_self_7
                    receiver_player.received_from_sender = sender_player.input_other_7

                    receiver_player.payoff += sender_player.input_other_7
                    sender_player.payoff += sender_player.input_self_7
                elif rand == 7:
                    sender_player.kept_of_sender = sender_player.input_self_8
                    receiver_player.received_from_sender = sender_player.input_other_8

                    receiver_player.payoff += sender_player.input_other_8
                    sender_player.payoff += sender_player.input_self_8
                elif rand == 8:
                    sender_player.kept_of_sender = sender_player.input_self_9
                    receiver_player.received_from_sender = sender_player.input_other_9

                    receiver_player.payoff += sender_player.input_other_9
                    sender_player.payoff += sender_player.input_self_9
                elif rand == 9:
                    sender_player.kept_of_sender = sender_player.input_self_10
                    receiver_player.received_from_sender = sender_player.input_other_10

                    receiver_player.payoff += sender_player.input_other_10
                    sender_player.payoff += sender_player.input_self_10
                elif rand == 10:
                    sender_player.kept_of_sender = sender_player.input_self_11
                    receiver_player.received_from_sender = sender_player.input_other_11

                    receiver_player.payoff += sender_player.input_other_11
                    sender_player.payoff += sender_player.input_self_11
                elif rand == 11:
                    sender_player.kept_of_sender = sender_player.input_self_12
                    receiver_player.received_from_sender = sender_player.input_other_12

                    receiver_player.payoff += sender_player.input_other_12
                    sender_player.payoff += sender_player.input_self_12
                elif rand == 12:
                    sender_player.kept_of_sender = sender_player.input_self_13
                    receiver_player.received_from_sender = sender_player.input_other_13

                    receiver_player.payoff += sender_player.input_other_13
                    sender_player.payoff += sender_player.input_self_13
                elif rand == 13:
                    sender_player.kept_of_sender = sender_player.input_self_14
                    receiver_player.received_from_sender = sender_player.input_other_14

                    receiver_player.payoff += sender_player.input_other_14
                    sender_player.payoff += sender_player.input_self_14
                elif rand == 14:
                    sender_player.kept_of_sender = sender_player.input_self_15
                    receiver_player.received_from_sender = sender_player.input_other_15

                    receiver_player.payoff += sender_player.input_other_15
                    sender_player.payoff += sender_player.input_self_15

                # receiver_player.payoff *= Constants.scale # scaling the payoff

            elif self.subsession.random_payoff == 'SUM':
                sender_values = self.chosen_option_list(sender_player)
                sender_self, sender_other = zip(*sender_values.values())

                receiver_player.payoff += sum(sender_other)
                receiver_player.received_from_sender += sum(sender_other)

                sender_player.payoff += sum(sender_self)
                sender_player.kept_of_sender += sum(sender_self)


    # Setting the payoff at random item in case of random dictator
    def random_dictator_payoff(self, sender_player, receiver_player):

        if self.subsession.random_payoff == 'SUM':
            # sum of the amount received from the sender player (slider 1 to 6)
            receiver_player.payoff = sender_player.input_other_1 + sender_player.input_other_2 + \
                                     sender_player.input_other_3 + sender_player.input_other_4 + \
                                     sender_player.input_other_5 + sender_player.input_other_6

            sender_player.payoff = sender_player.input_self_1 + sender_player.input_self_2 + \
                                   sender_player.input_self_3 + sender_player.input_self_4 + \
                                   sender_player.input_self_5 + sender_player.input_self_6

        if self.subsession.select_items == 'PRIMARY':

            if self.subsession.random_payoff == 'RAND':
                rand = random.randint(0, 5)
                sender_player.paid_slider = rand+1
                receiver_player.slider_as_receiver = rand+1

                if rand == 0:
                    receiver_player.payoff = sender_player.input_other_1
                    sender_player.payoff = sender_player.input_self_1
                elif rand == 1:
                    receiver_player.payoff = sender_player.input_other_2
                    sender_player.payoff = sender_player.input_self_2
                elif rand == 2:
                    receiver_player.payoff = sender_player.input_other_3
                    sender_player.payoff = sender_player.input_self_3
                elif rand == 3:
                    receiver_player.payoff = sender_player.input_other_4
                    sender_player.payoff = sender_player.input_self_4
                elif rand == 4:
                    receiver_player.payoff = sender_player.input_other_5
                    sender_player.payoff = sender_player.input_self_5
                elif rand == 5:
                    receiver_player.payoff = sender_player.input_other_6
                    sender_player.payoff = sender_player.input_self_6

                receiver_player.received_from_sender = receiver_player.payoff
                sender_player.kept_of_sender = sender_player.payoff

        elif self.subsession.select_items == 'FULL':

            if self.subsession.random_payoff == 'RAND':

                rand = random.randint(0, 14)
                sender_player.paid_slider = rand+1
                receiver_player.slider_as_receiver = rand+1

                if rand == 0:
                    # receiver payoff
                    receiver_player.payoff = sender_player.input_other_1
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_1
                elif rand == 1:
                    receiver_player.payoff = sender_player.input_other_2
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_2
                elif rand == 2:
                    receiver_player.payoff = sender_player.input_other_3
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_3
                elif rand == 3:
                    receiver_player.payoff = sender_player.input_other_4
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_4
                elif rand == 4:
                    receiver_player.payoff = sender_player.input_other_5
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_5
                elif rand == 5:
                    receiver_player.payoff = sender_player.input_other_6
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_6
                elif rand == 6:
                    receiver_player.payoff = sender_player.input_other_7
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_7
                elif rand == 7:
                    receiver_player.payoff = sender_player.input_other_8
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_8
                elif rand == 8:
                    receiver_player.payoff = sender_player.input_other_9
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_9
                elif rand == 9:
                    receiver_player.payoff = sender_player.input_other_10
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_10
                elif rand == 10:
                    receiver_player.payoff = sender_player.input_other_11
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_11
                elif rand == 11:
                    receiver_player.payoff = sender_player.input_other_12
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_12
                elif rand == 12:
                    receiver_player.payoff = sender_player.input_other_13
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_13
                elif rand == 13:
                    receiver_player.payoff = sender_player.input_other_14
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_14
                elif rand == 14:
                    receiver_player.payoff = sender_player.input_other_15
                    # sender payoff
                    sender_player.payoff = sender_player.input_self_15

                receiver_player.received_from_sender = receiver_player.payoff
                sender_player.kept_of_sender = sender_player.payoff

                # receiver_player.payoff *= Constants.scale                      # scaling the payoff
                # sender_player.payoff *= Constants.scale

            elif self.subsession.random_payoff == 'SUM':
                sender_values = self.chosen_option_list(sender_player)
                sender_self, sender_other = zip(*sender_values.values())

                receiver_player.payoff += sum(sender_other)
                sender_player.payoff += sum(sender_self)


    def inequality_aversion_score(self, svo_type, selected_values):

        if svo_type == 'Prosocial':
            # stores the distances of points on sliders to mid_points
            dist_to_mid = []
            dist_to_joint_max = []
            dist_to_altruist = []
            dist_to_indiv = []
            scale = self.subsession.scale

            for item in Constants.secondary_items:
                chosen_point = selected_values[item]

                x, y = Constants.mid_points[item]
                mid_point = (scale*x, scale*y)
                dist_to_mid.append(distance(chosen_point, mid_point))

                x,y = Constants.joint_max[item]
                joint_max_point = (scale*x, scale*y)
                dist_to_joint_max.append(distance(chosen_point, joint_max_point))

                x, y = Constants.altruist_points[item]
                altruist_point = (scale*x, scale*y)
                dist_to_altruist.append(distance(chosen_point, altruist_point))

                x, y = Constants.individualist_points[item]
                indiv_point = (scale*x, scale*y)
                dist_to_indiv.append(distance(chosen_point, indiv_point))

            avg_dist_to_equality = sum(dist_to_mid)/len(dist_to_mid)
            avg_dist_to_joint = sum(dist_to_joint_max)/len(dist_to_joint_max)
            avg_dist_to_altruist = sum(dist_to_altruist)/len(dist_to_altruist)
            avg_dist_to_indiv = sum(dist_to_indiv)/len(dist_to_indiv)

            # The Inequality Aversion Score is only calculated
            # for those who are closer to efficiency or equality
            #  than to altruist or individualist.
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

    # create a dictionary from the selected values
    def chosen_option_list(self, player):
        options = {"item7":  (float(player.input_self_7), float(player.input_other_7)),
                   "item8":  (float(player.input_self_8), float(player.input_other_8)),
                   "item9":  (float(player.input_self_9), float(player.input_other_9)),
                   "item10": (float(player.input_self_10), float(player.input_other_10)),
                   "item11": (float(player.input_self_11), float(player.input_other_11)),
                   "item12": (float(player.input_self_12), float(player.input_other_12)),
                   "item13": (float(player.input_self_13), float(player.input_other_13)),
                   "item14": (float(player.input_self_14), float(player.input_other_14)),
                   "item15": (float(player.input_self_15), float(player.input_other_15))}
        return options

    # A function to calculate the payoff for the players
    def set_payoffs(self):
        players = self.get_players()                                        # Get all the players for this game
        for p in players:
            p.svo_angle = self.svo_angle(p)                                 # Calculate the SVO angle
            p.alpha = tan(2*pi*p.svo_angle/360)                                # calculate the alpha value
            p.svo_type = self.svo_type(p.svo_angle)                               # Check what is the SVO type of the player
            if self.subsession.select_items == 'FULL':                            # Calculate the inequality_aversion_score
                selected_values = self.chosen_option_list(player=p)
                p.inequality_aversion_score = self.inequality_aversion_score(p.svo_type, selected_values)

            
        # Case of RING matching 
        if self.subsession.matching == 'RING':
            for i, p in enumerate(players):
                self.ring_payoff(p, players[(i+1)%len(players)])
                players[i].is_sender = True
                players[(i+1)%len(players)].is_receiver = True


        # Case of RANDOM_DICTATOR matching
        elif self.subsession.matching == 'RANDOM_DICTATOR':
                for i in range(0, len(players),2):                          # for all possible groups
                    rand_first_group = random.randint(0, 1)                 # A random value to choose either player A or B

                    if rand_first_group == 0:                               # Choose member A as the sender and B as the receiver.
                        sender_player = players[i]
                        players[i].is_sender = True
                        players[i].is_receiver = False

                        receiver_player = players[i+1]
                        players[i+1].is_receiver = True
                        players[i+1].is_sender = False
                        self.random_dictator_payoff(sender_player, receiver_player)         # Set the payoff
                    else:                                                   # Choose member B as the sender and A as the receiver
                        receiver_player = players[i]
                        players[i].is_receiver = True
                        players[i].is_sender = False

                        sender_player = players[i+1]
                        players[i+1].is_sender = True
                        players[i+1].is_receiver = False
                        self.random_dictator_payoff(sender_player, receiver_player)         # Set the payoff

                    # TODO it seems that this is not correct
                    # self.random_dictator_payoff(a_player, b_player)         # Set the payoff


# Player base class which contains the values for a single player per game
class Player(BasePlayer):



    # input_self_1 represents the amount of money that the user has chosen for himself for the first item
    # input_other_1 represents the amount of money that the user has chosen for others for the first item.
    input_self_1 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_1 = models.DecimalField(max_digits=5, decimal_places=2)

    # Same as above but for item 2 in the paper
    input_self_2 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_2 = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Same as above but for item 3 in the paper
    input_self_3 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_3 = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Same as above but for item 2 in the paper and so on.
    input_self_4 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_4 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_5 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_5 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_6 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_6 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_7 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_7 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_8 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_8 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_9 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_9 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_10 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_10 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_11 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_11 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_12 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_12 = models.DecimalField(max_digits=5, decimal_places=2)

    input_self_13 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_13 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_14 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_14 = models.DecimalField(max_digits=5, decimal_places=2)
    
    input_self_15 = models.DecimalField(max_digits=5, decimal_places=2)
    input_other_15 = models.DecimalField(max_digits=5, decimal_places=2)

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

    svo_angle = models.DecimalField(max_digits=10, decimal_places=5)
    alpha = models.DecimalField(max_digits=10, decimal_places=5)
    svo_type = models.StringField(choices=['Altruist', 'Prosocial', 'Individualist', 'Competitive'])
    inequality_aversion_score = models.DecimalField(max_digits=7, decimal_places=2)

    # slider selected for payment as sender
    paid_slider = models.IntegerField(initial=-1)

    # slider selected for payment as receiver for matching=RING
    slider_as_receiver = models.IntegerField(initial=-1)

    # amount kept by the sender
    kept_of_sender = models.DecimalField(max_digits=5, decimal_places=2)

    # amount received from the sender
    received_from_sender = models.DecimalField(max_digits=5, decimal_places=2)

    '''
    random dictator matching
          is_sender=True : the player was a sender
          is_receiver=True : the player was a receiver
    ring matching 
        both values will be True      
    '''
    is_sender = models.BooleanField(initial=False)
    is_receiver = models.BooleanField(initial=False)

