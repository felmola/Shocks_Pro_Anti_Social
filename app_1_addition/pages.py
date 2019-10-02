from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class app_1_addition_intro(Page):

    def is_displayed(self):
        return self.player.round_number == 1

    #http://otree.readthedocs.io/en/latest/timeouts.html (timer)
    def before_next_page(self):
        self.participant.vars['expiry'] = time.time() + Constants.time_limit


class app_1_addition_task(Page):

    form_model = 'player'
    form_fields = ['answer']

    # http://otree.readthedocs.io/en/latest/timeouts.html
    def get_timeout_seconds(self):
            return self.participant.vars['expiry'] - time.time()


    def is_displayed(self):
        return self.participant.vars['expiry'] - time.time() > 0

    def vars_for_template(self):

        if self.round_number == 1:

            return (
                {
                    'this_round_index': self.round_number,
                    'treatment': self.player.treatment,
                    'piece_rate': Constants.piece_rate,
                    'was_correct': "-",
                    'was_correct_accumulated': "-",
                    'acc_payoff': "-",
                }
            )
        else:
            self.player.counting_past()
            return (
                {
                    'this_round_index': self.round_number,
                    'treatment': self.player.treatment,
                    'piece_rate': Constants.piece_rate,
                    'was_correct': self.player.in_previous_rounds()[-1].was_correct,
                    'was_correct_accumulated': self.player.acc_was_correct,
                    'acc_payoff': self.player.acc_payoff,
                }
            )

    def before_next_page(self):

        self.player.counting_future()


class app_1_addition_announcement(Page):

    def is_displayed(self):

        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):

        self.player.final_count()

        return dict(
            acc_payoff = self.player.acc_payoff,
            final_payoff = self.player.final_payoff
        )

    def before_next_page(self):
        self.player.report_addition()


page_sequence = [
    app_1_addition_intro,
    app_1_addition_task,
    app_1_addition_announcement,
]
