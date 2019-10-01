from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class app_2_trust_intro(Page):

    def is_displayed(self):
        return self.player.round_number == 1


class app_2_trust_send(Page):

    form_model = 'player'
    form_fields = ['sent_amount']

    def is_displayed(self):
        if self.round_number == 1 and self.player.participant.vars['metarole'] == True:
            return True
        elif self.round_number == 1 and self.player.participant.vars['metarole'] == False:
            return False
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == True:
            return False
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == False:
            return True

    def vars_for_template(self):

        return dict(
            endowment = Constants.endowment,
            id_in_group = self.player.id_in_group
        )


class app_2_trust_beliefs_sender(Page):

    form_model = 'player'
    form_fields = ['sender_belief_if1', 'sender_belief_if2', 'sender_belief_shock']

    def is_displayed(self):
        if self.round_number == 1 and self.player.participant.vars['metarole'] == True:
            return True
        elif self.round_number == 1 and self.player.participant.vars['metarole'] == False:
            return False
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == True:
            return False
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == False:
            return True

    def vars_for_template(self):
        return dict(
            sender_belief_if1_option = Constants.send_choices[1],
            sender_belief_if2_option = Constants.send_choices[2],
        )


class app_2_trust_sendback(Page):

    form_model = 'player'
    form_fields = ['sent_back_amount_if1', 'sent_back_amount_if2']

    def is_displayed(self):
        if self.round_number == 1 and self.player.participant.vars['metarole'] == False:
            return True
        elif self.round_number == 1 and self.player.participant.vars['metarole'] == True:
            return False
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == True:
            return True
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == False:
            return False

    def vars_for_template(self):

        return dict(
            endowment = Constants.endowment,
            id_in_group = self.player.id_in_group,
            sent_1 = Constants.send_choices[1],
            sent_2 = Constants.send_choices[2],
            if_1_efficiency = Constants.send_choices[1] * Constants.factor + Constants.endowment,
            if_2_efficiency = Constants.send_choices[2] * Constants.factor + Constants.endowment
        )


class app_2_trust_beliefs_receiver(Page):

    form_model = 'player'
    form_fields = ['receiver_belief', 'receiver_belief_shock']

    def is_displayed(self):
        if self.round_number == 1 and self.player.participant.vars['metarole'] == False:
            return True
        elif self.round_number == 1 and self.player.participant.vars['metarole'] == True:
            return False
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == True:
            return True
        elif self.round_number == 2 and self.player.participant.vars['metarole'] == False:
            return False


class wait_trust(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class all_wait(WaitPage):
    wait_for_all_groups = True
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class app_2_trust_main_results(Page):

    def is_displayed(self):
         return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        self.player.tr_final_payoff()

#    def before_next_page(self):
#        self.player.report_trust()


page_sequence = [
    app_2_trust_intro,
    app_2_trust_send,
    app_2_trust_sendback,
    app_2_trust_beliefs_sender,
    app_2_trust_beliefs_receiver,
    wait_trust, #waits for the group partner only by default
    all_wait,
    app_2_trust_main_results,
]
