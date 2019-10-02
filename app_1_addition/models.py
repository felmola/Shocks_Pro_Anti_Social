from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'app_2_addition'
    players_per_group = None
    num_rounds = 10

    half_way = (num_rounds/2)
    time_limit = 15
    shock = 0.2
    piece_rate = 1000 #this code is in settings.py

    addends = [
        [57, 40, 95, 22, 73], [34, 32, 48, 57, 34], [83, 37, 58, 11, 46], [85, 33, 29, 19, 53], [93, 10, 98, 87, 50],
         [13, 69, 54, 88, 47], [15, 53, 68, 45, 99], [21, 43, 43, 28, 68], [48, 47, 32, 66, 46], [59, 60, 30, 14, 19],
         #[27, 38, 28, 97, 45], [93, 17, 54, 42, 20], [17, 44, 37, 16, 76], [67, 59, 13, 12, 93], [69, 93, 97, 37, 39],
         #[53, 97, 10, 85, 38], [60, 95, 64, 14, 49], [77, 62, 51, 87, 26], [23, 73, 80, 29, 83], [14, 77, 90, 46, 69],
         #[59, 23, 23, 50, 80], [94, 86, 16, 20, 48], [68, 93, 83, 72, 50], [34, 34, 27, 65, 97], [60, 81, 50, 38, 92],
         #[99, 35, 88, 91, 24], [96, 22, 84, 94, 70], [80, 55, 60, 41, 65], [15, 85, 75, 42, 90], [42, 90, 25, 81, 23],
         #[22, 20, 99, 81, 22], [56, 22, 18, 33, 33], [30, 85, 23, 52, 29], [49, 36, 49, 13, 92], [10, 86, 96, 21, 77],
         #[82, 36, 56, 72, 45], [57, 54, 50, 46, 69], [97, 46, 91, 57, 32], [62, 33, 39, 47, 49], [71, 31, 91, 76, 77],
         #[70, 98, 70, 95, 54], [73, 60, 69, 65, 68], [90, 32, 78, 91, 39], [62, 90, 51, 76, 59], [61, 57, 86, 85, 70],
         #[86, 41, 32, 74, 81], [99, 67, 46, 23, 17], [71, 76, 84, 36, 83], [27, 56, 87, 38, 60], [52, 43, 62, 53, 68],
         #[57, 77, 16, 10, 76], [28, 31, 86, 10, 74], [36, 53, 38, 24, 61], [64, 70, 39, 66, 96], [63, 77, 71, 51, 64],
         #[45, 87, 31, 89, 29], [65, 23, 74, 86, 43], [61, 60, 17, 88, 10], [78, 90, 34, 46, 55], [94, 84, 24, 12, 98]
    ]


class Subsession(BaseSubsession):
    
    def creating_session(self):

        #loading treatments:
        if self.round_number == 1:
            treatment = itertools.cycle([1, 2, 3])
            for p in self.get_players():
                p.treatment = next(treatment) #this is just to keep it for the database. the code below is the useful one because thisone does not persist between rounds or apps
                p.participant.vars['treatment'] = p.treatment #this one is the one to use throught the entire code

        #loading addends to each player in session
        for p in self.get_players():
            p.addend_1 = Constants.addends[self.round_number - 1][0]
            p.addend_2 = Constants.addends[self.round_number - 1][1]
            p.addend_3 = Constants.addends[self.round_number - 1][2]
            p.addend_4 = Constants.addends[self.round_number - 1][3]
            p.addend_5 = Constants.addends[self.round_number - 1][4]
            p.solution = p.addend_1 + p.addend_2 + p.addend_3 + p.addend_4 + p.addend_5

            print("[[ APP_1_ADDITION ]] - CREATING SESSION - PLAYER_ID ==> ", p.id_in_group, " <== ]]")
            print("[[ APP_1_ADDITION ]] - CREATING SESSION - P.PAR.VAR.TREATMENT ==> ",  p.participant.vars['treatment'], " <== ]]")
            #print("[[ APP_1_ADDITION ]] - CREATING SESSION - P.TREATMENT ==> ",  p.treatment, " <== ]]")
        print("[[ APP_1_ADDITION ]] - CREATING SESSION - ROUND NUMBER ==> ", self.round_number, " <== ]]")
        print("[[ APP_1_ADDITION ]] - CREATING SESSION - ADDENDS  ==> ",  p.addend_1, p.addend_2, p.addend_3, p.addend_4, p.addend_5, " <== ]]")
        print("[[ APP_1_ADDITION ]] - CREATING SESSION - SOLUTION ==> ",  p.solution, " <== ]]")
        print("[[ APP_1_ADDITION ]] - CREATING SESSION -------------------------------------------------------------]]")


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    addend_1 = models.IntegerField()
    addend_2 = models.IntegerField()
    addend_3 = models.IntegerField()
    addend_4 = models.IntegerField()
    addend_5 = models.IntegerField()

    solution = models.IntegerField()
    answer = models.IntegerField(min = 50, max = 495)

    treatment = models.IntegerField()

    was_correct = models.BooleanField()
    acc_was_correct = models.IntegerField()
    acc_payoff = models.IntegerField()
    final_payoff = models.FloatField()

    def counting_future(self):
        # For "before_next_page() in pages.py"

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............--------------------------------]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]]")

        if self.answer == self.solution:
            self.was_correct = True
        elif self.answer != self.solution:
            self.was_correct = False
        else:
            self.was_correct = "ERROR 69"

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ WAS_CORRECT ==> ", self.was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............--------------------------------]")

    def counting_past(self):
        # For vars_for_template() in pages.py"

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............--------------------------------]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]]")

        self.acc_was_correct = sum([p.was_correct for p in self.in_previous_rounds()])
        self.acc_payoff = sum([i * Constants.piece_rate for i in [p.was_correct for p in self.in_previous_rounds()]])
        #self.acc_payoff = sum([i * self.session.config['piece_rate'] for i in [p.was_correct for p in self.in_previous_rounds()]])

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ACC_WAS_CORRECT ==> ", self.acc_was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ WAS_CORRECT_LIST ==> ", [p.was_correct for p in self.in_previous_rounds()], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ACC_PAYOFF ==> ", self.acc_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............--------------------------------]")

    def final_count(self): # In the last round the function counting past is not working, leaving the last info not inputed in the lists so i have to run it but using in_all_rounds()

        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............--------------------------------]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]]")

        self.acc_was_correct = sum(filter(None, [p.was_correct for p in self.in_all_rounds()]))
        self.acc_payoff = sum([i * Constants.piece_rate for i in [p.was_correct for p in self.in_all_rounds()] if i != None]) #this creates a list multiplying every correct '1' times the piece rate and then adds it all
        #self.acc_payoff = sum([i * self.session.config['piece_rate'] for i in [p.was_correct for p in self.in_all_rounds()]]) #this creates a list multiplying every correct '1' times the piece rate and then adds it all

        if self.participant.vars['treatment'] == 1:
            self.final_payoff = self.acc_payoff
        elif self.participant.vars['treatment'] == 2 or self.participant.vars['treatment'] == 3:
            self.final_payoff = self.acc_payoff * Constants.shock
            #self.final_payoff = self.acc_payoff * self.session.config['shock']
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ACC_WAS_CORRECT ==> ", self.acc_was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ACC_PAYOFF ==> ", self.acc_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ FINAL_PAYOFF ==> ", self.final_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............--------------------------------]")

    def report_addition(self):
        #self.participant.vars['treatment'] = self.participant.vars['treatment']
        self.participant.vars['addition_acc_was_correct'] = self.acc_was_correct
        self.participant.vars['addition_acc_acc_payoff'] = self.acc_payoff
        self.participant.vars['addition_final_payoff'] = self.final_payoff
        print("[[ APP_1_ADDITION ]] - PLAYER - REPORT_ADDITION.............ROUND NUMBER", self.round_number)
        print("[[ APP_1_ADDITION ]] - PLAYER - REPORT_ADDITION.............PVARS ARE", self.participant.vars)
