from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
from django.core.validators import EmailValidator


author = 'Your name here'

doc = """
Your app description
"""


class UnalEmailValidator(EmailValidator):
    def validate_domain_part(self, domain_part):
        if domain_part != 'unal.edu.co':
            return False
        return True
    message = "Por favor ingrese un correo con dominio @unal.edu.co"


class Constants(BaseConstants):
    name_in_url = 'app_9_report'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        table_rows = []
        for p in self.get_players():
            row = p.participant.vars #quejesto?
            row['participant_code'] = p.participant.code
            row['consent_name'] = p.participant.vars.get('consent_name')
            row['consent_id_number'] = p.participant.vars.get('consent_id_number')
            row['addition_treatment'] = p.participant.vars.get('treatment')
            row['addition_acc_was_correct'] = p.participant.vars.get('addition_acc_was_correct')
            row['addition_acc_acc_payoff'] = p.participant.vars.get('addition_acc_acc_payoff')
            row['addition_final_payoff'] = p.participant.vars.get('addition_final_payoff')
            row['trust_metarole'] = p.participant.vars.get('metarole')
            row['trust_paying_round'] = p.participant.vars.get('paying_round')
            row['trust_t_final_payoff'] = p.participant.vars.get('t_final_payoff')
            row['trust_b_final_payoff'] = p.participant.vars.get('b_final_payoff')
            table_rows.append(row)
        return {'table_rows': table_rows}


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    e_mail = djmodels.EmailField(verbose_name='Correo Electrónico', validators=[UnalEmailValidator()])

    #basic info
    report_participant_code = models.LongStringField()
    report_consent_name = models.LongStringField()
    report_consent_id_number = models.IntegerField()
    report_treatment = models.IntegerField()

    #additions
    report_addition_acc_was_correct = models.IntegerField()
    report_addition_acc_acc_payoff = models.IntegerField()
    report_addition_final_payoff = models.FloatField()

    # trust basics
    report_metarole = models.BooleanField()
    report_paying_round = models.IntegerField()

    # trust r1
    report_r1_sent_amount = models.IntegerField()
    report_r1_sent_back_amount_if1 = models.BooleanField()
    report_r1_sent_back_amount_if2 = models.BooleanField()
    report_r1_t_payoff = models.IntegerField()

    # trust r2
    report_r2_sent_amount = models.IntegerField()
    report_r2_sent_back_amount_if1 = models.BooleanField()
    report_r2_sent_back_amount_if2 = models.BooleanField()
    report_r2_t_payoff = models.IntegerField()
    report_t_final_payoff = models.IntegerField()
    
    # beliefs sender
    report_sender_belief_if1 = models.BooleanField()
    report_sender_belief_if2 = models.BooleanField()
    report_sender_belief_shock = models.IntegerField()
    report_pay_sender_belief_if1 = models.IntegerField()
    report_pay_sender_belief_if2 = models.IntegerField()
    report_pay_sender_belief_shock = models.IntegerField()
    report_r1_b_temp_payoff = models.IntegerField()
    
    # beliefs receiver
    report_receiver_belief = models.IntegerField()
    report_receiver_belief_shock = models.IntegerField()
    report_pay_receiver_belief = models.IntegerField()
    report_pay_receiver_belief_shock = models.IntegerField()
    report_r2_b_temp_payoff = models.IntegerField()
    report_b_final_payoff = models.IntegerField()

    def report_vars_for_database(self): #this code sends the info from participant.vars up to the variables defined in player class for database
        self.report_participant_code = self.participant.code
        vars_fields = [
            # basic info
        'participant_code',
        'consent_name',
        'consent_id_number',
        'treatment',

        # additions
        'addition_acc_was_correct',
        'addition_acc_acc_payoff',
        'addition_final_payoff',

        # trust basics
        'metarole',
        'paying_round',

        # trust r1
        'r1_sent_amount',
        'r1_sent_back_amount_if1',
        'r1_sent_back_amount_if2',
        'r1_t_payoff',

        # trust r2
        'r2_sent_amount',
        'r2_sent_back_amount_if1',
        'r2_sent_back_amount_if2',
        'r2_t_payoff',
        't_final_payoff',

        # beliefs sender
        'sender_belief_if1',
        'sender_belief_if2',
        'sender_belief_shock',
        'pay_sender_belief_if1',
        'pay_sender_belief_if2',
        'pay_sender_belief_shock',
        'r1_b_temp_payoff',

        # beliefs receiver
        'receiver_belief',
        'receiver_belief_shock',
        'pay_receiver_belief',
        'pay_receiver_belief_shock',
        'r2_b_temp_payoff',
        'b_final_payoff',
        ]

        for field in vars_fields:
            setattr(self, 'report_{}'.format(field), self.participant.vars.get(field))
