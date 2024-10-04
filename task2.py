from random import choices, randint

from aalpy.SULs import SUL
from aalpy.learning_algs import run_Lstar
from aalpy.oracles import KWayTransitionCoverageEqOracle
from aalpy.oracles import RandomWordEqOracle


def is_balanced(x):
    len_x = len(x)
    if (len_x % 2) != 0 or len_x == 0:
        return False
    middle = (len_x - 1) // 2
    for i in range(middle + 1):
        if x[i] != '(' or x[middle + 1 + i] != ')':
            return False
    return True


def funny_counter(x, n=3):
    return len(x) % n


def verify_correctness(learned_model, function_under_test):
    assert function_under_test in {'funny_counter', 'is_balanced'}
    for _ in range(100000):
        if function_under_test == 'funny_counter':
            test_case = choices(['(', ')'], k=randint(10, 20))
            sul_output = funny_counter(test_case)
            learned_model_output = learned_model.execute_sequence(learned_model.initial_state, test_case)[-1]
        else:
            test_passing = randint(0, 1)
            x = randint(1, 10)
            test_case = list('(' * x + ')' * x)
            if not test_passing:
                mut = randint(1, len(test_case) - 1)
                test_case[mut] = '(' if test_case[mut] == ')' else ')'

            sul_output = is_balanced(test_case)
            learned_model_output = learned_model.execute_sequence(learned_model.initial_state, test_case)[-1]

        if sul_output != learned_model_output:
            print(f'Failing test-case : {test_case}')
            print(f'SUL output        : {sul_output}')
            print(f'Learned Model     : {learned_model_output}')
            return  # Exit on first failure

    print('All random test cases conform to a model')


class FunnyCounterSUL(SUL):
    def __init__(self):
        super().__init__()
        self.input = []
        self.function = funny_counter

    def pre(self):
        self.input = []

    def post(self):
        pass

    def step(self, letter):
        self.input.append(letter)
        return self.function(self.input)


class IsBalancedSUL(SUL):
    def __init__(self):
        super().__init__()
        self.input = []
        self.function = is_balanced

    def pre(self):
        self.input = []

    def post(self):
        pass

    def step(self, letter):
        if letter == '(':
            self.input.insert(0, letter)
        else:
            self.input.append(letter)

        return self.function(self.input)


input_alphabet = ['(', ')']
funny_counter_sul = FunnyCounterSUL()
funny_counter_oracle = RandomWordEqOracle(input_alphabet, funny_counter_sul)
learned_model_funny_counter = run_Lstar(input_alphabet, funny_counter_sul, funny_counter_oracle, automaton_type='mealy', print_level=0)

verify_correctness(learned_model_funny_counter, 'funny_counter')

is_balanced_sul = IsBalancedSUL()
is_balanced_oracle = KWayTransitionCoverageEqOracle(input_alphabet, is_balanced_sul, optimize='queries', k=7)
learned_model_is_balanced = run_Lstar(input_alphabet, is_balanced_sul, is_balanced_oracle, automaton_type='mealy', print_level=0)

verify_correctness(learned_model_is_balanced, 'is_balanced')