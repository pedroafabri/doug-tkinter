from time import sleep

# This is the class responsable for the parallel process
# "app" is an instance of AppUi, created at "Example.py"
class Parallel():
    def __init__(self, app):
        self.app = app 

    # Executes anything while updating the screen.
    # If "hide_window" is true, the app window will be minimized
    # at the start of the process and maximized after.
    def execute(self, hide_window=False):
        if not self.app.is_test_selected():
            self.app.show_popup("Erro", "Selecione pelo menos um teste!")
            return

        if hide_window:
            self.app.minimize() # If hide_window = True, minimize the app
        
        self.app.disable_screen()
        for item in self.app.get_selected():
            progress = 0
            self.app.update_process(item)
            # Simulates progress
            for i in range(1, 50):
                progress += 2
                self.app.update_progress(progress)
                sleep(0.1)

        self.app.reset_progress()
        self.app.enable_screen()
        if hide_window:
            self.app.maximize() # If hide_window = True, maximize the app