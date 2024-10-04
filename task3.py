from time import sleep

import dill as pickle
from aalpy.base import SUL
from random import seed

ITERATION_0: int = 3
ITERATION_2: int = 50

# =============
# DO NOT REMOVE
from collections import defaultdict, Counter
import random

random.random()
placeholder = defaultdict(Counter)
# ==============

from Message import Message


class MessageBoardSUL(SUL):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.reset()

    def reset(self):
        self.board.reset()

    def step(self, inp):
        action, params = inp
        if action == 'publish_message':
            return self.board.publish_message(*params)
        elif action == 'like_message':
            return self.board.like_message(*params)
        elif action == 'dislike_message':
            return self.board.dislike_message(*params)
        elif action == 'edit_message':
            return self.board.edit_message(*params)
        elif action == 'report':
            return self.board.report(*params)
        elif action == 'remove_report':
            return self.board.remove_report(*params)
        elif action == 'search_messages':
            return self.board.search_messages(*params)
        elif action == 'retrieve_messages':
            return self.board.retrieve_messages(params)
        elif action == 'get_points':
            messages = self.board.retrieve_messages(params)
            if len(messages) == 0:
                return 0
            return messages[0].get_points()

    def pre(self):
        self.board.reset()
        pass

    def post(self):
        pass


seed(1)


class MessageBoardInterface:
    def __init__(self):
        pass

    def publish_message(self, client: str, message: str) -> str:
        pass

    def retrieve_messages(self, target_client: str) -> list[Message]:
        pass

    def search_messages(self, search_string: str) -> list[Message]:
        pass

    def report(self, reporter: str, target_client: str) -> str:
        pass

    def remove_report(self, reporter: str, target_client: str) -> str:
        pass

    def like_message(self, initiator: str, target_client: str, target_message: str) -> str:
        pass

    def dislike_message(self, initiator: str, target_client: str, target_message: str) -> str:
        pass

    def remove_like(self, initiator: str, target_client: str, target_message: str, ) -> str:
        pass

    def remove_dislike(self, initiator: str, target_client: str, target_message: str, ) -> str:
        pass

    def edit_message(self, initiator: str, target_client: str, message_to_edit: str, new_message: str) -> str:
        pass

    def delete_message(self, initiator: str, target_client: str, message_to_delete: str) -> str:
        pass

    def react(self, initiator: str, target_client: str, message_to_react_to: str, reaction: str) -> str:
        pass

    def reset(self):
        pass


possible_reactions = {'smiley', 'laughing', 'crying', 'frown', 'horror', 'surprise', 'skeptical', 'cool'}

with open(f'black_box_impl/message_board.pickle', 'rb') as handle:
    correct_message_board = pickle.load(handle)

with open(f'black_box_impl/message_board_0.pickle', 'rb') as handle:
    message_board_0 = pickle.load(handle)

with open(f'black_box_impl/message_board_1.pickle', 'rb') as handle:
    message_board_1 = pickle.load(handle)

with open(f'black_box_impl/message_board_2.pickle', 'rb') as handle:
    message_board_2 = pickle.load(handle)

correct_message_board.reset()

# TODO 1. For all 3 variations of the message board, find shortest test-cases described
#  in the assignment sheet using learning-based testing
# TODO 2. Describe the found bugs, and present the shortest test-case in the report

# Execute the test cases


correct_sul = MessageBoardSUL(correct_message_board)
sul_0 = MessageBoardSUL(message_board_0)
sul_1 = MessageBoardSUL(message_board_1)
sul_2 = MessageBoardSUL(message_board_2)

from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWordEqOracle

# Define the input alphabet (actions and their parameters)
input_alphabet0 = [
    ('publish_message', ('UserA', 'Hi')),
    ('like_message', ('User1', 'UserA', 'Hi')),
    ('dislike_message', ('User1', 'UserA', 'Hi')),
    ('like_message', ('User2', 'UserA', 'Hi')),
    ('dislike_message', ('User2', 'UserA', 'Hi')),
    ('get_points', 'UserA'),
]

input_alphabet1 = [
    ('publish_message', ('UserA', 'Hi')),
    ('report', ('User1', 'UserA')),
    ('report', ('User2', 'UserA')),
    ('report', ('User3', 'UserA')),
    ('report', ('User4', 'UserA')),
    ('report', ('User5', 'UserA')),
    ('report', ('User5', 'UserA')),
    ('publish_message', ('UserA', 'still alive')),
]

input_alphabet2 = [
    ('publish_message', ('UserA', 'Hi')),
    ('publish_message', ('UserB', 'Hi')),
    ('publish_message', ('UserC', 'Hi')),
    ('edit_message', ('UserA', 'UserA', 'Hi', 'Yo')),
    ('edit_message', ('UserB', 'UserB', 'Hi', 'Yo')),
    ('edit_message', ('UserC', 'UserC', 'Hi', 'Yo')),
    ('retrieve_messages', 'UserA'),
    ('retrieve_messages', 'UserB'),
    ('retrieve_messages', 'UserC'),
]
eq_oracle = RandomWordEqOracle(input_alphabet0, correct_sul, num_walks=100, min_walk_len=3, max_walk_len=6)
correct_model_0 = run_Lstar(input_alphabet0, correct_sul, eq_oracle, automaton_type='mealy', print_level=3)
model_0 = run_Lstar(input_alphabet0, sul_0, eq_oracle, automaton_type='mealy', print_level=3)

eq_oracle = RandomWordEqOracle(input_alphabet1, correct_sul, num_walks=100, min_walk_len=3, max_walk_len=6)
correct_model_1 = run_Lstar(input_alphabet1, correct_sul, eq_oracle, automaton_type='mealy', print_level=3)
model_1 = run_Lstar(input_alphabet1, sul_1, eq_oracle, automaton_type='mealy', print_level=3)


#eq_oracle = RandomWordEqOracle(input_alphabet2, correct_sul, num_walks=100, min_walk_len=3, max_walk_len=6)
#correct_model_2 = run_Lstar(input_alphabet2, correct_sul, eq_oracle, automaton_type='mealy', print_level=3)
#model_2 = run_Lstar(input_alphabet2, sul_2, eq_oracle, automaton_type='mealy', print_level=3)


def compare_models(model1, model2):
    if model1 == model2:
        print("Models are equivalent")
    else:
        print("Models are not equivalent")

print("Start comparison")
sleep(2)
compare_models(correct_model_0, model_0)
sleep(2)
compare_models(correct_model_1, model_1)
sleep(2)
#compare_models(correct_model_2, model_2)
