'''Calculator Standard Infix App Project: simple 4 function calculator that inputs and outputs calculations
Rhett Seitz & Cj Schoenmann CPTR 215 A
Started 11/27/2024. Modified 11/28- 12/12
Sources: 
        https://www.pythontutorial.net/pyqt/pyqt-qmainwindow/
        https://doc.qt.io/qt-6/qwidget.html?search=setFixedSize
        https://www.pythonguis.com/pyside6-tutorial/
        https://doc.qt.io/qt-6/qkeyevent.html
        https://www.w3schools.com/python/ref_func_chr.asp
        https://python-reference.readthedocs.io/en/latest/docs/float/is_integer.html
        https://www.w3schools.com/python/ref_func_abs.asp

TO-DO: 

add doc tests
Add it to Github for Abishur to look at.
Doublecheck memory
Sqaureroot
#Big numbers

REPLIT: 
'''
#TO-DO and SUGGESTIONS:. 
#Rescale

from PySide6.QtWidgets import(
    QMainWindow,
    QApplication,
    QPushButton,
    QGridLayout, #Use this for Calculator's Button layouts
    QLabel,
    QWidget,
    QMessageBox
)
from PySide6.QtCore import Qt #Import Qt for alignment options
from PySide6.QtGui import QKeyEvent #Use this for keypresses

class Logic():
    '''class that deals with the back end (calculations, arithmetic) of the calculator'''
    def __init__(self):
        self.current_input = '0'
        self.memory = 0
        self.memory_active = False #Flag to track if memory is active
        self.operator = None
        self.operand = None
        self.reset_input = False #Flag to reset input, mainly after an operator
        #Tracks if result has been calculated yet.
        self.result_calculated = False #Flag showing result has not been calculated yet. 
        self.error_state = False #Flag to track division by zero error

    def process_digit(self, digit):
        '''Process digit input. User can enter only up to including 8 digits.
        User Cannot enter more than 8 digits.
        >>> logic = Logic()
        >>> logic.process_digit('2')
        >>> logic.current_input
        '2'

        >>> logic.process_digit('3')
        >>> logic.current_input
        '23'

        >>> logic.process_digit('4')
        >>> logic.process_digit('5')
        >>> logic.process_digit('6')
        >>> logic.process_digit('7')
        >>> logic.process_digit('8')
        >>> logic.process_digit('9')
        >>> logic.process_digit('0') #Exceeding 8 digits. Not allowed
        >>> logic.current_input 
        '23456789'
        '''
        if self.error_state: #Block any input if in error state (such as division by zero)
            return
        
        if self.result_calculated: #Reset after a result is calculated
            self.current_input = digit
            self.result_calculated = False

        elif self.reset_input: #Reset after an operator
            #If the flag is set & becomes true, show a new number
            self.current_input = digit
            self.reset_input = False  #Clear the flag back to what it was, after the new digit appears

        elif len(self.current_input) < 8: #Check if current input is less than 8. 

            #Append the digit if the length has not been reached.
            if self.current_input == '0':
                self.current_input = digit
            else:
                self.current_input += digit

    def process_operator(self, operator):
        '''Process Operator input. Operators include +, -, ×, ÷

        >>> logic = Logic()
        >>> logic.process_digit('6')
        >>> logic.process_operator('+')
        >>> logic.operator
        '+'
        >>> logic.operand
        5.0
        '''
        if self.error_state: #Block any operator input if in error state (such as division by zero)
            return
        
        if self.operator is None:
            self.operand = float(self.current_input)
        else:
            self.calculate_result()  # Compute intermediate result
        self.operator = operator #Fix this.
        self.reset_input = True #Set flag to reset input for next number
        self.result_calculated = False #Reset result for a new operation

    def calculate_result(self):
        '''evaluate the expression based on the operator and calculations'''
        if self.error_state: #Block calculations if in error state (such as division by zero)
            return
        if self.operator and self.operand is not None:  #If enter a operator and operand
            if self.operator == '+':
                self.operand += float(self.current_input)
            elif self.operator == '-':
                self.operand -= float(self.current_input)
            elif self.operator == '×':
                self.operand *= float(self.current_input)
            elif self.operator == '÷':
                if float(self.current_input) == 0: #Check for division by zero error
                    self.current_input = '0.E' #Show E for Error
                    self.error_state = True #Lock the calculator
                    return #Exit early to prevent further calculation

                else:
                    self.operand /= float(self.current_input)


            #Convert the result to an integer if it is a whole number
            if self.operand.is_integer():
                self.current_input = str(int(self.operand)) #Convert to an integer and string
            else:
                self.current_input = str(self.operand) #Keep as a float and string if not a whole number

            self.operator = None
            self.reset_input = True #Reset operator and flag for next operation
            self.result_calculated = True #Result calculated

    def clear_entry(self):
        '''When CE button is clicked, the previous entry is cleared. 
        Does not work when an = is entered or if a calculation has been set'''
        if self.error_state: #Prevent CE if in error state
            return
        if self.result_calculated:
            # If the result has been calculated, do not clear the current input
            return
        self.current_input = '0'

    def clear_all(self):
        '''When the CA button is clicked, ALL previous entries are cleared reverting back to 0.'''

        self.current_input = '0'
        self.operator = None
        self.operand = None
        self.error_state = False

    def pos_or_neg(self):
        '''Acts a toggle between positve and negative numbers. If positive, number becomes negative (viceversa)'''
        if self.error_state: #Dont do positive/negative if division by zero error
            return
        if self.current_input.startswith('-'): #Slice through the number, getting rid of the negative number
            self.current_input = self.current_input[1:] #This line converts a negative number to a positive one
        else:  #Concatenate negative sign to positive number
            self.current_input = '-' + self.current_input #This converts a positive number to a negative one

    def process_decimal(self):
        '''Creates decimal when decimal button is clicked'''
        if '.' not in self.current_input:
            self.current_input += '.'

    def backspace(self):
        '''Removes the last character from current input'''
        if self.error_state:
            return

        if len(self.current_input) > 1:
            #Creates new string that includes all characters except the last one
            #Chops off last character. Ex: 123 becomes 12
            self.current_input = self.current_input[:-1] 
        else:
            #Returns just zero
            self.current_input = '0'

    def square_root(self):
        '''Calculate the square root of the current input'''

        value = float(self.current_input)
        if value >= 0:
            self.current_input = str(value ** 0.5)

    def memory_add(self):
        '''Adds the current input to the memory and notify UI'''
        self.memory += float(self.current_input)
        self.memory_active = True #Activate Memory indicator

    def memory_clear(self):
        '''Clears the memory and notifies UI'''
        self.memory = 0
        self.memory_active = False #Turn off Memory indicator

    def memory_recall(self):
        '''Stores the current input in memory'''
        if self.error_state:
            return
        self.current_input = str(self.memory)

    def memory_subtract(self):
        '''Subtracts the current input from the memory'''
        self.memory -= float(self.current_input)
        self.memory_active = self.memory != 0   #Update flag based on memory status

    def is_memory_set(self):
        '''Returns whether memory contains a value.'''
        return self.memory_active
    
    def handle_button_press_in_logic(self, button_text):
        '''Processes Button Presses'''
        if self.error_state and button_text != 'CA':
            return #Block all inputs except Clear All in Error State

        if button_text.isdigit(): #Handle digit input. Checks if all characters in a string are digits
                self.process_digit(button_text)
        elif button_text in ['+', '-', '×', '÷']: #Handle operators
            self.process_operator(button_text)
        elif button_text == '=': #Handle equals
            self.calculate_result()
        elif button_text == 'CE': #Handle clear entry
            self.clear_entry()
        elif button_text == 'CA': #Handle clear all
            self.clear_all()
        elif button_text == '+/-':
            self.pos_or_neg()
        elif button_text == '.':
            self.process_decimal()
        elif button_text == '←':
            self.backspace()
        elif button_text == 'MC':
            self.memory_clear()
        elif button_text == 'MR':
            self.memory_recall()
        elif button_text == 'M-':
            self.memory_subtract()
        elif button_text == 'M+':
            self.memory_add()
        elif button_text == '√':
            self.square_root()

    def handle_keypress_event(self, key, text):
        '''Processes Keypresses for users keyboard inputs'''

        if Qt.Key_0 <= key <= Qt.Key_9:  # Handle digit keys 0-9
            self.process_digit(chr(key))  # Convert key to character

        elif text in ['+', '-', '*', '/']:  # Handle operators
            operator_map = {
                '+': '+',
                '-': '-',
                '*': '×',
                '/': '÷'
            }
            self.process_operator(operator_map[text])

        elif key in [Qt.Key_Enter, Qt.Key_Return]:  # Handle Enter key
            self.calculate_result()
        elif key == Qt.Key_Backspace:  # Handle Backspace
            self.backspace()
        elif key == Qt.Key_Period or text == '.':  # Handle decimal point
            self.process_decimal()
        elif key == Qt.Key_Escape:  # Handle Escape (clear all)
            self.clear_all()



class Interface(QMainWindow): #Inherit ONLY from QMainWindow, NOT Logic
    '''class that deals with the front end (design) of the calculator'''

    def __init__(self):
        '''Constrcutor that sets up the main functions of the front end'''
        super().__init__()
        self.logic = Logic() #Class Interface HAS A class Logic (see yuml diagram)

        self.setWindowTitle("Rhett and CJ's Calculator") #Window Title for App

        self.setFixedSize(400, 500) #main window size for app

        #Code below allows organizing and grouping calculator's UI elements within a single, manageable widget
        self.central_widget = QWidget(self) #Create central widget acting as a container for all other widgets
        self.setCentralWidget(self.central_widget) #sets newly created QWidget as the central widget of QMainWindow

        #Grid Layout for buttons and display
        self.layout = QGridLayout(self.central_widget)

        #Memory indicator label
        self.memory_label = QLabel('')
        self.memory_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.memory_label.setFixedSize(20, 20) #Small size for M

        self.layout.addWidget(self.memory_label, 0, 0)

        #Call helper methods to build the interface
        self.create_display()
        self.create_buttons()

    def create_display(self):
        '''Create and set up display for the calculator'''
        self.display = QLabel('0', self)
        self.display.setFixedHeight(70)
        self.display.setStyleSheet(
            'font-size: 48px; color: black; border: 2px solid black; background-color: white;')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter) #Align text to the right
        self.layout.addWidget(self.display, 0, 0, 1, 5) #Add display at the top spanning 4 columns

    def create_buttons(self):
        '''Create and arrange calculator buttons. Used a dictionary to store buttons'''
        buttons = {
            'MC': (1, 0), 'MR': (1, 1), 'M-': (1, 2), 'M+': (1, 3), '÷': (1, 4),
            '√': (2, 0), '7': (2, 1), '8': (2, 2), '9': (2, 3), '×': (2, 4),
            '+/-': (3, 0), '4': (3, 1), '5': (3, 2), '6': (3, 3), '-': (3, 4),
            'CE': (4, 0), '1': (4, 1), '2': (4, 2), '3': (4, 3), '+': (4, 4),
            'CA': (5, 0), '0': (5, 1), '.': (5, 2), '←': (5, 3), '=': (5, 4)
        }

        self.buttons = {} #Store button references for usage later
        for text, position in buttons.items(): #keys in dict are strings that is the text. position is the value
            button = QPushButton(text, self)
            button.setFixedSize(50, 50)

            if text == 'CE':
                button.setStyleSheet('font-size: 20px; color: black; background-color: yellow;')
            elif text == 'CA':
                button.setStyleSheet('font-size: 20px; color: white; background-color: red;')
            else:
                # General style for all buttons
                button.setStyleSheet('font-size: 20px; font-weight: bold;')

            self.layout.addWidget(button, position[0], position[1])
            self.buttons[text] = button

            #Connect all buttons to a a central common slot using the button's text as it's identifer
            button.clicked.connect(self.handle_button_press) #Connect to slot function handle_button_press

    def handle_button_press(self):
        '''Button Press Processing is in Logic class. 
        This function implements the logic on the front end'''

        button = self.sender() #Identify which button was clicked (signal was sent)
        if isinstance(button, QPushButton): #Make sure the sender is a QPushButton
            button_text = button.text() #Get the text of the button

            if button_text == 'CA':

                #Create a confirmation box asking user if they really want to clear all or not
                confirmation_box = QMessageBox(self)
                confirmation_box.setWindowTitle('Confirm Clear All')
                confirmation_box.setText('Are you sure you want to clear everything?')
                confirmation_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirmation_box.setDefaultButton(QMessageBox.No)

                #User's response
                response = confirmation_box.exec()
                if response == QMessageBox.Yes:
                    self.logic.clear_all() #Delegate actual clearing to Logic

            else:
                self.logic.handle_button_press_in_logic(button_text)
            self.update_display() #Update the display after processing logic.

    def keyPressEvent(self, event: QKeyEvent) -> None:
        '''Delegate KeyPress Events to Logic'''

        key = event.key()
        text = event.text()
        self.logic.handle_keypress_event(key, text)
        self.update_display()

    def update_display(self):
        '''Updates the display with the values entered by the user and processed by the backend'''
        display_text = self.logic.current_input
        if self.logic.is_memory_set():
            display_text += ' M'
        self.display.setText(display_text)


app = QApplication([])
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    window = Interface()
    window.show()
    app.exec()

