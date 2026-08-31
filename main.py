# -*- coding: utf-8 -*-
"""
Created on Thu May  9 22:04:42 2024

@author: Kuzn
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from calculator_ui import Ui_FormCalculator
import re
import os
from PyQt5.QtGui import QIcon

def resource_path(relative_path):
    base_path = getattr(
        sys,
        "_MEIPASS",
        os.path.dirname(os.path.abspath(__file__))
    )
    return os.path.join(base_path, relative_path)

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path(os.path.join("assets", "calculator_icon.ico"))))
        self.ui = Ui_FormCalculator()
        self.ui.setupUi(self)
        self.ui.btn_backspace.setIcon(QIcon(resource_path("Backspace.png")))
        self.chekPoint = False
        self.chekOperators = False
        self.butnBlock = True 
        self.num = 1
        
        self.ui.btn_0.clicked.connect(lambda: self.addDigit("0"))
        self.ui.btn_1.clicked.connect(lambda: self.addDigit("1"))
        self.ui.btn_2.clicked.connect(lambda: self.addDigit("2"))
        self.ui.btn_3.clicked.connect(lambda: self.addDigit("3"))
        self.ui.btn_4.clicked.connect(lambda: self.addDigit("4"))
        self.ui.btn_5.clicked.connect(lambda: self.addDigit("5"))
        self.ui.btn_6.clicked.connect(lambda: self.addDigit("6"))
        self.ui.btn_7.clicked.connect(lambda: self.addDigit("7"))
        self.ui.btn_8.clicked.connect(lambda: self.addDigit("8"))
        self.ui.btn_9.clicked.connect(lambda: self.addDigit("9"))
        self.ui.btn_del.clicked.connect(lambda: self.clearAll())
        self.ui.btn_backspace.clicked.connect(lambda: self.backspace())
        self.ui.btn_point.clicked.connect(lambda: self.setPoint())
        self.ui.btn_plus.clicked.connect(lambda: self.mathematicalOperator("+"))
        self.ui.btn_minus.clicked.connect(lambda: self.mathematicalOperator("-"))
        self.ui.btn_multiply.clicked.connect(lambda: self.mathematicalOperator("*"))
        self.ui.btn_divide.clicked.connect(lambda: self.mathematicalOperator("/"))
        self.ui.btn_equal.clicked.connect(lambda: self.mathematicalOperator("="))
        
    def addDigit (self, text_btn):
        if self.ui.lineEdit.text() == '0':
            self.ui.lineEdit.setText(text_btn)
            self.chekOperators = False
        else:
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + text_btn)
            self.chekOperators = False
    
    def clearAll(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit.setText("0")
        self.chekPoint = False
        if self.butnBlock == False:
            self.mathematicalOperator("Unblock")
    
    def backspace(self):
        if self.ui.lineEdit.text() != '0':
            self.ui.lineEdit.backspace()
            self.chekPoint = False
        if not self.ui.lineEdit.text():
            self.ui.lineEdit.setText("0")
        self.chekPoint = "." in self.ui.lineEdit.text()
        self.chekOperators = self.ui.lineEdit.text()[-1] in "+-*/"
            
        
    def setPoint(self):
        if self.chekPoint == False:
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + ".")
            self.chekPoint = True
            
    def splitExpression(self, expression):
        parts = re.findall(r'(\d+\.\d+|\d+|[+-/*])', expression)
        inclusive = []
        checOper = False 

        for i in range (len (parts)):
        
            if checOper == True:
                inclusive.append(parts[i]) 
            elif parts[0] == "-" and checOper == False:
                inclusive.append(parts[0] + parts[1])
                checOper = True
            else: 
                inclusive.append(parts[i]) 
                
        if checOper == True:
            inclusive.pop(1)
                
        return inclusive
    
    def mathematicalOperator(self, operator):
    
        expression = self.ui.lineEdit.text()
        
        if operator != "=" and operator != "Unblock":
            if len(expression) > 1 and expression[-1] in "+-*/":
                self.ui.lineEdit.setText(expression[:-1] + operator)
                return
        
        if operator != "=" and "." in expression and expression.endswith("."):
            self.ui.lineEdit.setText(expression + "0" + operator)
            return
        
        if operator != "=" and self.chekOperators == False and operator != "Unblock":
            if operator == "-" and expression == "0" and self.chekOperators == False:
                self.ui.lineEdit.setText(operator)
                self.chekOperators = True
                return
            else:
                self.ui.lineEdit.setText(expression + operator)
                self.chekPoint = False
                self.chekOperators = True
                return
        else:
            try:
          
                parts = self.splitExpression(expression)
                print(parts)
            
                def toNumber(value):
                    if "." in value:
                        return float(value)
                    return int(value)
            
                priority_parts = [toNumber(parts[0])]
                division_by_zero = False
            
                
                for i in range(1, len(parts), 2):
                    op = parts[i]
                    self.num = toNumber(parts[i + 1])
            
                    if op == "*":
                        priority_parts[-1] *= self.num
            
                    elif op == "/":
                        if self.num == 0:
                            result = "WTF :D"
                            self.butnBlock = False
                            self.ui.lineEdit.setText(str(result))
                            division_by_zero = True
                            break
            
                        priority_parts[-1] /= self.num
            
                    else:
                        priority_parts.extend([op, self.num])
            
            
                if not division_by_zero:
                    result = priority_parts[0]
            
                    for i in range(1, len(priority_parts), 2):
                        op = priority_parts[i]
                        self.num = priority_parts[i + 1]
            
                        if op == "+":
                            result += self.num
                        elif op == "-":
                            result -= self.num  
            except Exception as error:
                print(error)
                return
                       
        
        if operator == "Unblock" or self.butnBlock == True:
            self.ui.lineEdit.setText(str(round(result, 6)))
            self.chekOperators = False
            self.butnBlock = True

        self.ui.btn_0.setEnabled(self.butnBlock)
        self.ui.btn_1.setEnabled(self.butnBlock)
        self.ui.btn_2.setEnabled(self.butnBlock)
        self.ui.btn_3.setEnabled(self.butnBlock)
        self.ui.btn_4.setEnabled(self.butnBlock)
        self.ui.btn_5.setEnabled(self.butnBlock)
        self.ui.btn_6.setEnabled(self.butnBlock)
        self.ui.btn_7.setEnabled(self.butnBlock)
        self.ui.btn_8.setEnabled(self.butnBlock)
        self.ui.btn_9.setEnabled(self.butnBlock)
        self.ui.btn_backspace.setEnabled(self.butnBlock)
        self.ui.btn_point.setEnabled(self.butnBlock)
        self.ui.btn_plus.setEnabled(self.butnBlock)
        self.ui.btn_minus.setEnabled(self.butnBlock)
        self.ui.btn_multiply.setEnabled(self.butnBlock)
        self.ui.btn_divide.setEnabled(self.butnBlock)
        self.ui.btn_equal.setEnabled(self.butnBlock)
        
        
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())