import dill as pickle
from abc import ABC, abstractmethod

from aalpy.base import SUL
from aalpy.oracles import RandomWMethodEqOracle
from aalpy.learning_algs import run_Lstar
from copy import deepcopy
from aalpy.utils import compare_automata

#import os


# interface that all loaded implementations implement
class AbstractVendingMachine(ABC):

    @abstractmethod
    # user can add any coin (0.5, 1, 2)
    def add_coin(self, coin):
        pass

    @abstractmethod
    # possible orders are 'coke', 'peanuts', 'water'
    def push_button(self, order):
        pass

    @abstractmethod
    def reset(self):
        pass

class VendingMachineSUL(SUL):
    def __init__(self, vm):
        super().__init__()
        self.vm = vm

    def pre(self):
        self.vm.reset()

    def post(self):
        pass
    
    def step(self, letter):
        # Check against defined lists of coins and buttons
        coins = [0.5, 1, 2]
        buttons = ['coke', 'peanuts', 'water']
        
        if letter in coins:
            output = self.vm.add_coin(letter)
        elif letter in buttons:
            output = self.vm.push_button(letter)
        
        if output is None:
            return 'No_Action'  # Normalize None outputs
        
        # Log output for clarity
        #print(f"Input: {letter}, Output: {output}")

        return output

if __name__ == '__main__':
    model_files = ['vending_machine_tamim.pickle', 'vending_machine_edi.pickle',
                   'vending_machine_sebastian.pickle', 'vending_machine_matthias.pickle']
    learned_models = {}
    alphabet = [0.5, 1, 2, 'coke', 'peanuts', 'water']

    # Learn a model for each vending machine independently and store them with an enumerated key
    for idx, model_file in enumerate(model_files):
        with open(f'black_box_impl/{model_file}', 'rb') as handle:
            vm = pickle.load(handle)
        sul = VendingMachineSUL(vm)
        eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=100, walk_len=100)
        model = run_Lstar(alphabet, sul, eq_oracle, 'mealy')
        learned_models[f"Model_{idx+1} ({model_file})"] = model
        # Visualize and save the model diagram
        #if not os.path.exists('visuals'):
        #    os.makedirs('visuals')

        #model.visualize(path=f"./visuals/Model_{idx + 1} ({model_file}).dot")

    # Compare all models using AALpy's compare_automata function
    for name1, dfa1 in learned_models.items():
        for name2, dfa2 in learned_models.items():
            if name1 != name2:
                # Deep copy models before comparison to prevent side-effects
                dfa1_copy = deepcopy(dfa1)
                dfa2_copy = deepcopy(dfa2)
                
                # Using AALpy's compare_automata to find counterexamples
                counterexamples = compare_automata(dfa1_copy, dfa2_copy)
                if counterexamples:
                    print(f"Counterexamples between {name1} and {name2}:")
                    for cex_idx, cex in enumerate(counterexamples, 1):
                        formatted_cex = ' -> '.join(str(x) for x in cex)
                        print(f"  {cex_idx}. {formatted_cex}")
                else:
                    print(f"No differences found between {name1} and {name2}")
