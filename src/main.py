#Sean Broderick
#main usr interface for the application

#INCLUDE
import sys, logging
from back import capture_audio
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QLabel, QPushButton,
    QTextEdit, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QFont  # Import QFont

#LOGGING
with open('lib\\app.log', 'w'):
    pass
logger = logging.getLogger(__name__)
logging.basicConfig(filename='lib\\app.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        logger.info('Creating GUI')

        # Title label
        self.label = QLabel("Transcription Terminal")  
        self.label.setAlignment(Qt.AlignCenter)  
        self.label.setStyleSheet("color: #0051D8;") #ADJUST COLOR LABEL

        # Set a larger font for the label
        label_font = QFont()
        label_font.setPointSize(24)  
        label_font.setBold(True)
        self.label.setFont(label_font)
        
        # Buttons
        self.button = QPushButton("Start/Stop")  # Button to change output field TODO: have button change when pressed

        # Set a larger font for the buttons
        button_font = QFont()
        button_font.setPointSize(18)  # Adjust as desired
        self.button.setFont(button_font)
        self.save.setFont(button_font)
        
        # Output text field
        self.text = QTextEdit()
        self.text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.text.setReadOnly(True)
        self.text.setStyleSheet("color: black;")  # Set output text color to black

        # Set a larger font for the output field
        output_font = QFont()
        output_font.setPointSize(14)  # Adjust as desired
        self.text.setFont(output_font)
        
        
        # Create layout and add widgets
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.save)
        
        
        layout2 = QVBoxLayout()
        layout2.addWidget(self.label)  # Add the label to the layout
        layout2.addWidget(self.text)
        layout2.addLayout(layout)

        
        # Set dialog layout
        self.setLayout(layout2)
        
        # Link function calls to buttons
        self.button.clicked.connect(self.run)
        self.save.clicked.connect(self.saves)
        self.setStyleSheet("background-color: #F9F9F9;")  #ADJUST BACKGROUND COLOR
        logger.info('GUI Construction Complete')

    # Move copy input text to output
    def run(self):
        logger.info('Generating Transcription Output')
        try:
            self.update_str('Output: ')
            #capture_audio(self, self.edit.text()) #TODO: Stream tokens to screen and have only a set amout of words be posted at a time. save entire thing to text
        except Exception as e:
            logger.error(e)
            print(e)
        logger.info('Transcription Generation Complete')

    def update_str(self, text):
        self.text.insertPlainText(text)
        self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().maximum())
        QCoreApplication.processEvents()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Set global stylesheet to set all text color to black
    app.setStyleSheet("""
        * {
            color: black;
        }
        QWidget {
            background-color: #FFB6C1;
        }
    """)
    
    win = QMainWindow()
    win.resize(800, 600)    
    # Create and show the form
    form = Form()
    win.setCentralWidget(form)
    win.show()
    # Run the main Qt loop
    sys.exit(app.exec())
