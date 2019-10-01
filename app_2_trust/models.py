from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools, random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'app_2_trust'
    players_per_group = 2
    num_rounds = 2

    endowment = 2
    factor = 3

    send_choices = [0, 1, 2]
    #send_back_choices = [x*3 for x in send_choices]

def shifter(m): # https://groups.google.com/forum/#!searchin/otree/perfect$20stranger|sort:date/otree/rciCzbTqSfQ/Sbl2-3KqAQAJ
    group_size_err_msg = 'This code will not correctly work for group size not equal 2'
    assert Constants.players_per_group == 2, group_size_err_msg
    m = [[i.id_in_subsession for i in l] for l in m]
    f_items = [i[0] for i in m]
    s_items = [i[1] for i in m]
    for i in range(Constants.num_rounds):
        yield [[i, j] for i, j in zip(f_items, s_items)]
        s_items = [s_items[-1]] + s_items[:-1]


class Subsession(BaseSubsession):

    def creating_session(self):

        if self.round_number == 1:
            # SHUFFLER
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]
            self.session.vars['paying_round'] = random.randint(1, Constants.num_rounds)
            metarole = itertools.cycle([True, False]) # The order of roles. True for sender first, False for receiver first
            for p in self.get_players():
                p.metarole = next(metarole)
                p.participant.vars['metarole'] = p.metarole
        #SHUFFLER
        fd = self.session.vars['full_data']
        self.set_group_matrix(fd[self.round_number - 1])

        print("[[ APP_2_TRUST ]] - CREATING SESSION - ROUND NUMBER ==> ", self.round_number, " <== ]]")
        print("[[ APP_2_TRUST ]] - CREATING SESSION - GROUP.MATRIX ==> ", self.get_group_matrix(), " <== ]]")
        print("[[ APP_2_TRUST ]] - CREATING SESSION - PAYING_ROUND ==> ", self.session.vars['paying_round'], " <== ]]")
        for p in self.get_players():
            print("[[ APP_2_TRUST ]] - CREATING SESSION - PLAYER_ID_INGROUP ==> ", p.id_in_group, " <== ]]")
            print("[[ APP_2_TRUST ]] - CREATING SESSION - PLAYER_ID_INSUBSESSION ==> ", p.id_in_subsession, " <== ]]")
            #print("[[ APP_2_TRUST ]] - CREATING SESSION - METAROLE ==> ", p.metarole, " <== ]]")
            print("[[ APP_2_TRUST ]] - CREATING SESSION - PVARS.METAROLE ==> ", p.participant.vars['metarole'], " <== ]]")
            print("[[ APP_2_TRUST ]] - CREATING SESSION - ###############################################################")


class Group(BaseGroup):

    #Group Shifter
    def shifter(m):
        group_size_err_msg = 'This code will not correctly work for group size not equal 2'
        assert Constants.players_per_group == 2, group_size_err_msg
        m = [[i.id_in_subsession for i in l] for l in m]
        f_items = [i[0] for i in m]
        s_items = [i[1] for i in m]
        for i in range(Constants.num_rounds):
            yield [[i, j] for i, j in zip(f_items, s_items)]
            s_items = [s_items[-1]] + s_items[:-1]

    def set_payoffs(self):
        #this code could be reduced if I use get_players() "Returns a list of all the groups in the subsession"
        for p in self.get_players():
            if self.round_number == 1:
                p1 = self.get_player_by_id(1)
                p2 = self.get_player_by_id(2)
            elif self.round_number == 2:
                p1 = self.get_player_by_id(2)
                p2 = self.get_player_by_id(1)

        # trust payoffs
        if p1.sent_amount == Constants.send_choices[0]:
            p1.t_temp_payoff = Constants.endowment
            p2.t_temp_payoff = Constants.endowment
        elif (p1.sent_amount == Constants.send_choices[1] and p2.sent_back_amount_if1 == True) or (p1.sent_amount == Constants.send_choices[2] and p2.sent_back_amount_if2 == True):
            p1.t_temp_payoff = int(((Constants.endowment - p1.sent_amount) + (p1.sent_amount * Constants.factor) + Constants.endowment) / 2)
            p2.t_temp_payoff = p1.t_temp_payoff
        elif (p1.sent_amount == Constants.send_choices[1] or  p1.sent_amount == Constants.send_choices[2]) and (p2.sent_back_amount_if1 == False or p2.sent_back_amount_if2 == False):
            p1.t_temp_payoff = Constants.endowment - p1.sent_amount
            p2.t_temp_payoff = Constants.endowment + (p1.sent_amount * 3)

        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - ROUND NUMBER ==> ", self.round_number, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - PLAYER_ID_INSUBSESSION ==> ", p.id_in_subsession, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - P.METAROLE ==> ", p.participant.vars['metarole'], " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - P1.T.TEMP.PAYOFF ==> ", self.get_player_by_id(1).t_temp_payoff, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - P2.T.TEMP.PAYOFF ==> ", self.get_player_by_id(2).t_temp_payoff, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - ###############################################################")

        # BELIEFS
        # belief answers and markers (sender)
        if p2.sent_back_amount_if1 == p1.sender_belief_if1:
            p1.pay_sender_belief_if1 = True
        else:
            p1.pay_sender_belief_if1 = False
        if p2.sent_back_amount_if2 == p1.sender_belief_if2:
            p1.pay_sender_belief_if2 = True
        else:
            p1.pay_sender_belief_if2 = False
        if p2.participant.vars['treatment'] == p1.sender_belief_shock:
            p1.pay_sender_belief_shock = True
        else:
            p1.pay_sender_belief_shock = False

        # belief answers and markers (receiver)
        if p1.sent_amount == p2.receiver_belief:
            p2.pay_receiver_belief = True
        else:
            p2.pay_receiver_belief = False
        if p1.participant.vars['treatment'] == p2.receiver_belief_shock:
            p2.pay_receiver_belief_shock = True
        else:
            p2.pay_receiver_belief_shock = False

        if self.round_number == 1:
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - ROUND NUMBER ==> ", self.round_number, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_sender_belief_if1 ==> ", self.get_player_by_id(1).pay_sender_belief_if1, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_sender_belief_if2 ==> ", self.get_player_by_id(1).pay_sender_belief_if2, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_sender_belief_shock ==> ", self.get_player_by_id(1).pay_sender_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_receiver_belief ==> ", self.get_player_by_id(2).pay_receiver_belief, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_receiver_belief_shock ==> ", self.get_player_by_id(2).pay_receiver_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - ###############################################################")
        elif self.round_number == 2:
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) ROUND NUMBER ==> ", self.round_number, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_sender_belief_if1 ==> ", self.get_player_by_id(2).pay_sender_belief_if1, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_sender_belief_if2 ==> ", self.get_player_by_id(2).pay_sender_belief_if2, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_sender_belief_shock ==> ", self.get_player_by_id(2).pay_sender_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_receiver_belief ==> ", self.get_player_by_id(1).pay_receiver_belief, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_receiver_belief_shock ==> ", self.get_player_by_id(1).pay_receiver_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) ###############################################################")

        # beliefs payoffs (temp):
        for p in self.get_players():
            p.b_temp_payoff = sum([0 if e is None else e for e in [p.pay_sender_belief_if1, p.pay_sender_belief_if2, p.pay_sender_belief_shock, p.pay_receiver_belief, p.pay_receiver_belief_shock]])
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS-TEMP) - PLAYER_ID_INSUBSESSION ==> ", p.id_in_subsession, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS-TEMP) - P.B_TEMP_PAYOFF ==> ", p.b_temp_payoff, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS-TEMP) ###############################################################")

        # temporary participant vars for comparison in admin report database # No trust report function below needed
        for p in self.get_players():
            # trust basics
            p.participant.vars['metarole'] = p.in_round(1).metarole
            p.participant.vars['paying_round'] = self.session.vars['paying_round']
            # trust r1
            p.participant.vars['r1_sent_amount'] = p.in_round(1).sent_amount
            p.participant.vars['r1_sent_back_amount_if1'] = p.in_round(1).sent_back_amount_if1
            p.participant.vars['r1_sent_back_amount_if2'] = p.in_round(1).sent_back_amount_if2
            p.participant.vars['r1_t_payoff'] = p.in_round(1).t_temp_payoff
            # trust r2
            p.participant.vars['r2_sent_amount'] = p.in_round(2).sent_amount
            p.participant.vars['r2_sent_back_amount_if1'] = p.in_round(2).sent_back_amount_if1
            p.participant.vars['r2_sent_back_amount_if2'] = p.in_round(2).sent_back_amount_if2
            p.participant.vars['r2_t_payoff'] = p.in_round(2).t_temp_payoff
            #beliefs sender
            p.participant.vars['sender_belief_if1'] = p.sender_belief_if1
            p.participant.vars['sender_belief_if2'] = p.sender_belief_if2
            p.participant.vars['sender_belief_shock'] = p.sender_belief_shock
            p.participant.vars['pay_sender_belief_if1'] = p.pay_sender_belief_if1
            p.participant.vars['pay_sender_belief_if2'] = p.pay_sender_belief_if2
            p.participant.vars['pay_sender_belief_shock'] = p.pay_sender_belief_shock
            #beliefs receiver
            p.participant.vars['receiver_belief'] = p.receiver_belief
            p.participant.vars['receiver_belief_shock'] = p.receiver_belief_shock
            p.participant.vars['pay_receiver_belief'] = p.pay_receiver_belief
            p.participant.vars['pay_receiver_belief_shock'] = p.pay_receiver_belief_shock
            p.participant.vars['b_temp_payoff'] = p.b_temp_payoff
            p.participant.vars['b_final_payoff'] = p.b_final_payoff


# save this code for posterity.  print("[[ APP_2_TRUST ]] - BBBBBB - GROUP.MATRIX R2 ==> ", self.get_players()[0].get_others_in_subsession(), " <== ]]",) #  get_others_in_subsession() is a player methodd. So it has to be called on a player object (get_players()[0] wich is a group method)
class Player(BasePlayer):

    #treatment = models.IntegerField()
    metarole = models.BooleanField()

    sent_amount = models.IntegerField(
        choices = Constants.send_choices
    )

    sent_back_amount_if1 = models.BooleanField(
        choices=[
            (False, 'No reciprocar'),
            (True, 'Reciprocar'),
        ],
    )

    sent_back_amount_if2 = models.BooleanField(
        choices=[
            (False, 'No reciprocar'),
            (True, 'Reciprocar'),
        ],
    )

    t_temp_payoff = models.IntegerField() # payoff per round of trust
    t_final_payoff = models.IntegerField() # final payoff for trust

    #beliefs

    sender_belief_if1 = models.BooleanField(
        choices=[
            (False, 'No Reciprocó'),
            (True, 'Si Reciprocó'),
        ],
    )

    sender_belief_if2 = models.BooleanField(
        choices=[
            (False, 'No Reciprocó'),
            (True, 'Si Reciprocó'),
        ],
    )

    sender_belief_shock = models.IntegerField(
        choices=[
            (1, 'No Shock'),
            (2, 'Random Shock'),
            (3, 'Intentional Shock'),
        ],
    )

    pay_sender_belief_if1 = models.BooleanField()
    pay_sender_belief_if2 = models.BooleanField()
    pay_sender_belief_shock = models.BooleanField()

    receiver_belief = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
            (2, '2'),
        ],
    )

    receiver_belief_shock = models.IntegerField(
        choices=[
            (1, 'No Shock'),
            (2, 'Random Shock'),
            (3, 'Intentional Shock'),
        ],
    )

    pay_receiver_belief = models.BooleanField()
    pay_receiver_belief_shock = models.BooleanField()

    b_temp_payoff = models.IntegerField() # payoff per round of belief
    b_final_payoff = models.IntegerField() # final payoff for belief

    def tr_final_payoff(self): #mind this. It gave me an error saying "redeclared t_final_payoff defined above without usage.
        # Apparently fixed my b_final_payoff and

        print("[[ APP_2_TRUST ]] - PLAYER/FINAL PAYOFFS (BELIEF and TRUST) - ROUND_NUMBER ==> ", self.round_number, " <== ]]")
        self.t_final_payoff = self.in_round(self.session.vars['paying_round']).t_temp_payoff
        #self.b_final_payoff = sum(filter(None, [self.b_temp_payoff for p in self.in_rounds(1, self.round_number)]))
        self.b_final_payoff = sum(filter(None, [self.in_round(1).b_temp_payoff, self.in_round(Constants.num_rounds).b_temp_payoff]))
        print("[[ APP_2_TRUST ]] - PLAYER/FINAL_PAYOFFS - PLAYER_ID_INSUBSESSION ==> ", self.id_in_subsession, " <== ]]")
        print("[[ APP_2_TRUST ]] - PLAYER/FINAL_PAYOFFS - P.T_FINAL_PAYOFF ==> ", self.t_final_payoff, " <== ]]")
        print("[[ APP_2_TRUST ]] - PLAYER/T_FINAL_PAYOFF  - P.B_FINAL_PAYOFF ==> ", self.b_final_payoff, " <== ]]")

#    def report_trust(self):
#        # for the admin_report
#        self.participant.vars['metarole'] = self.in_round(1).metarole
#        self.participant.vars['paying_round'] = self.session.vars['paying_round']
#        self.participant.vars['t_final_payoff'] = self.t_final_payoff
#        self.participant.vars['b_final_payoff'] = self.b_final_payoff
#
#        # for the tests
#        self.participant.vars['sent_amount'] = self.sent_amount
#        self.participant.vars['receiver_belief'] = self.receiver_belief
#        self.participant.vars['pay_receiver_belief'] = self.pay_receiver_belief
#        self.participant.vars['receiver_belief_shock'] = self.receiver_belief_shock
#        self.participant.vars['pay_receiver_belief_shock'] = self.pay_receiver_belief_shock
#        self.participant.vars['sent_back_amount_if1'] = self.sent_back_amount_if1
#        self.participant.vars['sender_belief_if1'] = self.sender_belief_if1
#        self.participant.vars['pay_sender_belief_if1'] = self.pay_sender_belief_if1
#        self.participant.vars['sent_back_amount_if2'] = self.sent_back_amount_if2
#        self.participant.vars['pay_sender_belief_if2'] = self.pay_sender_belief_if2
#        self.participant.vars['sender_belief_shock'] = self.sender_belief_shock
#        self.participant.vars['pay_sender_belief_shock'] = self.pay_sender_belief_shock
#
#        print("[[ APP_1_ADDITION ]] - PLAYER - REPORT_TRUST.............ROUND NUMBER", self.round_number)
#        print("[[ APP_1_ADDITION ]] - PLAYER - REPORT_TRUST.............PVARS ARE", self.participant.vars)
