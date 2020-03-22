from src.AppUI import AppUI
from Parallel import Parallel
import os

#======================
# Usage Example
#======================

# Reads every .txt file in directory, gets their lines and populates the tests dictionary
def get_tests():
    tests = {}
    for r, d, f in os.walk('./'):
        for filename in f:
            if '.txt' in filename:
                test_file = []
                with open(filename) as file:
                    for line in file:
                        test_file.append(line.rstrip())
                tests[filename] = test_file
    
    return tests

# Confirm Button action
def confirm_button(app):
    parallel = Parallel(app)
    parallel.execute()
    
# Results Button action
def results_button(app):
    parallel = Parallel(app)
    parallel.execute(True) # True to execute minimizing window

if __name__ == '__main__':

    test_dict = get_tests() # Creates the dictionary
    app = AppUI("Testing Tests", test_dict) # Instantiate AppUI passing the title and tests dictionary
    app.set_confirm_command(lambda : confirm_button(app)) # Define what the confirm button will make
    app.set_results_command(lambda : results_button(app))
    app.show() # Run Application