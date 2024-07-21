from PyQt5.QtWidgets import (QMainWindow,
                             QGridLayout,
                             QStackedLayout,
                             QHBoxLayout,
                             QPushButton,
                             QLabel,
                             QWidget,
                             QComboBox,
                             QLineEdit,
                             QTableWidget,
                             QTableWidgetItem,
                             QMessageBox,
                             QApplication,
                             QVBoxLayout,
                             QSizePolicy)
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import QRect,Qt
from fractions import Fraction
import numpy as np
from SimplexMax import *
from SimplexMin import *
from toolspack import *

# TODO Graph plot simple solution areas


HEADER_SPACE=10

INPUTCONST = 2
INPUTVARS = 2


class MWindow(QMainWindow):
	def __init__(self):
		super(MWindow,self).__init__()
		self.setWindowTitle("Simplex Solver")
		self.CONSTRAINT_EQUALITY_SIGNS = [u"\u2264", u"\u2265", "="] #you can choose either <=,>=,= for constraint
		self.create_ui()
		self.set_ui_layout()

		# self.setFixedWidth(self.sizeHint().width()+200)  # To fix width if window
		self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)

	def create_ui(self):
		"""
			Create_ui : self
				this function initialize our window labels and buttons
		"""
		global INPUTCONST, INPUTVARS  #Global so we can pass the number of constraints
		self.font = QFont()
		self.font.setWeight(7)
		self.font.setBold(True)

		self.objective_function_label = QLabel("Objective function", self)
		self.objective_function_label.setFont(self.font)
		self.objective_function_label.setFixedHeight(self.objective_function_label.sizeHint().height())
		self.objective_fxn_table = self.create_table(1, INPUTVARS + 2, ["="], self.create_header_labels(INPUTVARS))

		# Adjust column widths to increase the length of the table
		column_width = 60  # Set your desired width for each column
		for i in range(self.objective_fxn_table.columnCount()):
			self.objective_fxn_table.setColumnWidth(i, column_width)

		self.objective_fxn_table.setFixedHeight(self.objective_fxn_table.sizeHint().height())


		z_item = QTableWidgetItem("Z")
		self.objective_fxn_table.setItem(0, INPUTVARS + 1, z_item)
		z_item.setFlags(Qt.ItemIsEnabled)

		#make the objective fxn table's size fit perfectly with the rows
		self.objective_fxn_table.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		self.objective_fxn_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.objective_fxn_table.resizeColumnsToContents()
		self.objective_fxn_table.setFixedHeight(self.objective_fxn_table.verticalHeader().length()+self.objective_fxn_table.horizontalHeader().height()+25)

		self.constraints_label = QLabel("Constraints Matrix", self)
		self.constraints_label.setFont(self.font)
		self.constraint_table = self.create_table(INPUTCONST, INPUTVARS + 2, self.CONSTRAINT_EQUALITY_SIGNS, self.create_header_labels(INPUTVARS))

		# Adjust column widths to increase the length of the table
		column_width = 60  # Set your desired width for each column
		for i in range(self.constraint_table.columnCount()):
			self.constraint_table.setColumnWidth(i, column_width)

		self.constraint_table.setFixedHeight(self.constraint_table.sizeHint().height())


		self.answers_label = QLabel()
		self.answers_label.setStyleSheet("font-size: 17px;font-weight: bold;")


		# self.add_row_btn = QPushButton('Add Row', self)
		# self.add_row_btn.clicked.connect(self.add_row_event)
		# self.add_col_btn = QPushButton('Add Column', self)
		# self.add_col_btn.clicked.connect(self.add_column_event)
		# self.del_row_btn = QPushButton("Delete Row", self)
		# self.del_row_btn.clicked.connect(self.del_row_event)
		# self.del_col_btn = QPushButton("Delete Column", self)
		# self.del_col_btn.clicked.connect(self.del_col_event)
		self.solve_btn = QPushButton('Solve', self)
		self.solve_btn.clicked.connect(self.solve_event)
		# self.solve_btn_graph = QPushButton('Solve', self)
		# self.solve_btn.clicked.connect(self.solve_event)

		self.operation_combo = QComboBox()
		for item in ["max", "min"]:
			self.operation_combo.addItem(item)

		self.solution_label = QLabel("Solution", self)
		self.solution_label.setFont(self.font)
		# self.pivot_label = QLabel("Pivots :", self)
		# self.pivot_label.setFont(self.font)# self.pivot_label = QLabel("Pivots :", self)
		# self.pivot_label.setFont(self.font)
		self.phase_label = QLabel(self)
		self.phase_label.setFont(self.font)
		self.solution_table = []
		self.phase_table = []
		self.next = QPushButton('back', self)
		self.next.clicked.connect(self.back_event)
		self.back = QPushButton('next', self)
		self.back.clicked.connect(self.next_event)
		self.clear = QPushButton('clear', self)
		self.clear.clicked.connect(self.clear_layout)
		self.export = QPushButton('LaTeX', self)

	def set_ui_layout(self):
		vbox_layout1 = QHBoxLayout(self)
		self.vbox_layout2 = QVBoxLayout(self)
		self.vbox_layout3 = QStackedLayout(self)
		self.vbox_layout4 = QHBoxLayout(self)
		self.vbox_layout5 = QStackedLayout(self)
		# self.vbox_layout6 = QStackedLayout(self)

		# vbox_layout1.addWidget(self.add_row_btn)
		# vbox_layout1.addWidget(self.add_col_btn)
		# vbox_layout1.addWidget(self.del_row_btn)
		# vbox_layout1.addWidget(self.del_col_btn)
		vbox_layout1.addWidget(self.operation_combo)
		vbox_layout1.addWidget(self.solve_btn)

		central_widget = QWidget(self)
		self.setCentralWidget(central_widget)

		main_v_layout = QGridLayout(self)
		central_widget.setLayout(main_v_layout)

		self.vbox_layout2.addWidget(self.objective_function_label)
		self.vbox_layout2.addWidget(self.objective_fxn_table)
		self.vbox_layout2.addWidget(self.constraints_label)
		self.vbox_layout2.addWidget(self.constraint_table)
		self.vbox_layout2.addWidget(self.answers_label)

		self.vbox_layout5.addWidget(self.solution_label)

		self.vbox_layout4.addWidget(self.next)
		self.vbox_layout4.addWidget(self.back)
		self.vbox_layout4.addWidget(self.clear)
		self.vbox_layout4.addWidget(self.export)

		main_v_layout.addLayout(vbox_layout1, 0, 0)
		main_v_layout.addLayout(self.vbox_layout2, 1, 0)
		main_v_layout.addLayout(self.vbox_layout3, 1, 1)
		main_v_layout.addLayout(self.vbox_layout5, 0, 1)
		# main_v_layout.addLayout(self.vbox_layout6, 2, 1)
		main_v_layout.addLayout(self.vbox_layout4, 2, 1)

	def create_table(self, rows, cols,equality_signs=None, horizontal_headers=None,vertical_headers=None):
		table = QTableWidget(self)
		table.setColumnCount(cols)
		table.setRowCount(rows)

		# Set the table headers
		if horizontal_headers:
			table.setHorizontalHeaderLabels(horizontal_headers)

		if vertical_headers:
			table.setVerticalHeaderLabels(vertical_headers)

		#add <=,>=,= signs so that person can select the whether that constraint is <=,>= or =
		#its also used for the objective fxn but in the objective fxn we just use = Z so an [=] sign is passed
		#for equality signs in the creation of the objective fxn table in the create_ui function
		if equality_signs:
			numofrows = table.rowCount()
			numofcols = table.columnCount()
			# add combo items to self.constraint_table
			for index in range(numofrows):
				equality_signs_combo = QComboBox()
				for item in equality_signs:
					equality_signs_combo.addItem(item)
				table.setCellWidget(index, numofcols - 2, equality_signs_combo)

		# Do the resize of the columns by content
		table.resizeColumnsToContents()
		table.resizeRowsToContents()
		return table

	def create_header_labels(self,num_of_variables):
		"""Name the columns for the tables x1,x2,.... give a space and then add bi"""
		header_labels = [" "*HEADER_SPACE +"x" + str(i + 1) + " " * HEADER_SPACE for i in range(num_of_variables)]
		header_labels.extend([" " * HEADER_SPACE, " " * HEADER_SPACE + "b" + " " * HEADER_SPACE])
		return header_labels

	def del_row_event(self):
		#allow a maximum of one constraint
		if self.constraint_table.rowCount()>1:
			self.constraint_table.removeRow(self.constraint_table.rowCount()-1)

	def del_col_event(self):
		#if we have x1,x2 and the signs and bi column don't allow deletion of column, else delete
		if self.constraint_table.columnCount()>4:
			self.constraint_table.removeColumn(self.constraint_table.columnCount()-3)
			self.objective_fxn_table.removeColumn(self.objective_fxn_table.columnCount()-3)

	def add_column_event(self):
		self.constraint_table.insertColumn(self.constraint_table.columnCount()-2)
		self.objective_fxn_table.insertColumn(self.objective_fxn_table.columnCount()-2)
		self.constraint_table.setHorizontalHeaderLabels(self.create_header_labels(self.constraint_table.columnCount()-2))
		self.objective_fxn_table.setHorizontalHeaderLabels(self.create_header_labels(self.constraint_table.columnCount()-2))

		# make the objective fxn table's size fit perfectly with the rows and columns
		self.objective_fxn_table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self.objective_fxn_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.objective_fxn_table.setFixedHeight(self.objective_fxn_table.verticalHeader().length() + self.objective_fxn_table.horizontalHeader().height() + 25)

	def add_row_event(self):
		self.constraint_table.insertRow(self.constraint_table.rowCount())
		equality_signs_combo = QComboBox()
		for item in self.CONSTRAINT_EQUALITY_SIGNS:
			equality_signs_combo.addItem(item)
		self.constraint_table.setCellWidget(self.constraint_table.rowCount()-1,self.constraint_table.columnCount() - 2, equality_signs_combo)
		self.constraint_table.resizeRowsToContents()

	def clear_layout(self):
		"""
			clear already given results for next results to be shown
		"""
		for i in reversed(range(self.vbox_layout5.count())):
			self.vbox_layout5.itemAt(i).widget().deleteLater()
			self.vbox_layout5.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.vbox_layout3.count())):
			self.vbox_layout3.itemAt(i).widget().deleteLater()
			self.vbox_layout3.itemAt(i).widget().setParent(None)
		self.answers_label.setText("")

	def create_label(self, txt):
		lbl = QLabel(txt)
		lbl.setFont(self.font)
		return lbl

	def solve_event(self):
		self.solution_table = []
		self.phase_table = []
		self.vbox_layout3.setCurrentIndex(0)
		# print("solve", "\n","="*20)
		unaugmented_matrix=self.form_unaugmented_matrix()
		# print("My inputed data : ", unaugmented_matrix)
		constraint_equality_signs=self.read_equality_signs(self.constraint_table.columnCount()-2, self.constraint_table)
		command=self.operation_combo.currentText().lower()
		c = unaugmented_matrix[0][1:].tolist()
		A = [list(unaugmented_matrix[i][1:]) for i in range(1,len(unaugmented_matrix))]
		b = [unaugmented_matrix[i].tolist()[0] for i in range(1,len(unaugmented_matrix))]
		# ineq = ['<=' if constraint_equality_signs[i] == u"\u2264" else for i in range(len(constraint_equality_signs)) ]
		ineq = []
		for i in range(len(constraint_equality_signs)):
			if (constraint_equality_signs[i] == u"\u2264"):
				ineq.append("<=")
			elif(constraint_equality_signs[i] == u"\u2265"):
				ineq.append(">=")
			else:
				ineq.append("=")


		hp_normalize_problem(A, b, c, ineq)
		hd_startDoc()
		# prob = hp_what_problem()
		prob = command
		hd_set_Problem(A, c,b, ineq, prob)
		if hp_is_simple(b, ineq):
			# print(f"{TC.B_PURPLE}This problem is a simple simplex{TC.NC}")
			self.vbox_layout5.addWidget(self.create_label("This problem is a simple simplex"))
			# print("="*75)
			if prob == 'max':
				obj = SimplexMax(A, b, c, ineq)
				final = obj.Solve()
				if final is None:
					self.answers_label.setText("The problem has an unbounded solution")
					return
				for i in range(0, len(final[3])):
					self.vbox_layout5.addWidget(self.create_label(f"Phase I table {i}"))
					# self.vbox_layout6.addWidget(self.create_label(final[-1][i - 1]))
					self.solution_table.append(self.create_gui_for_tableau(np.array(final[3][i]), final[2]["vars"], final[4][i]))
					self.solution_table[i].setFixedHeight(self.solution_table[i].verticalHeader().length() + self.solution_table[i].horizontalHeader().height() + 150)
					self.vbox_layout3.addWidget(self.solution_table[i])
				hd_finalDoc(final[0], -int(obj.table[-1][-1]))

				# print("="*100)
				# print(f"{TC.B_GREEN}The Optimal solution is :{TC.NC}", {i:final[0][i] for i in list(final[0])[:len(obj.args[-1])]})
				self.answers_label.setText(f"Optimal Solution: {str({i:round(final[0][i],2) for i in list(final[0])[:len(obj.args[-1])]})}")
				# print("="*100)
			elif prob == 'min':
				obj = SimplexMin(A, b, c, ineq)
				final = obj.Solve()
				for i in range(0, len(final[3])):
					self.vbox_layout5.addWidget(self.create_label(f"Phase I table {i}"))
					# self.vbox_layout6.addWidget(self.create_label(final[-1][i]))
					self.solution_table.append(self.create_gui_for_tableau(np.array(final[3][i]), final[2]["vars"], final[4][i]))
					self.solution_table[i].setFixedHeight(self.solution_table[i].verticalHeader().length() + self.solution_table[i].horizontalHeader().height() + 150)
					self.vbox_layout3.addWidget(self.solution_table[i])
				a_name = [f"A{i+1}" for i in obj.vars["artificial"] if i != -1]
				for var in final[2]["vb"]:
					if var in a_name:
						self.answers_label.setText("No Base Solutions!")
						return
				try:
					hd_finalDoc(final[0], -int(obj.table[2][-1][-1]))
				except Exception as e:
					print(e)


				self.answers_label.setText(f"Optimal Solution:{str({i:round(final[0][i],2) for i in list(final[0])[:len(obj.args[-1])]})}")
			else:
				self.answers_label.setText(f"Problem type is invalid.")
		else:
			self.vbox_layout5.addWidget(self.create_label("This problem is not a simple simplex - we need two phases -"))
			obj = SimplexMin(A, b, c, ineq)
			phase_1_table = obj._init_1st_phase()
			obj.table = phase_1_table
			final = obj.Solve()
			for i in range(0, len(final[3])):
				self.vbox_layout5.addWidget(self.create_label(f"Phase I table {i}"))
				# self.vbox_layout6.addWidget(self.create_label(final[-1][i]))
				self.solution_table.append(self.create_gui_for_tableau(np.array(final[3][i]), final[2]["vars"], final[4][i]))
				self.solution_table[i].setFixedHeight(self.solution_table[i].verticalHeader().length() + self.solution_table[i].horizontalHeader().height() + 150)
				self.vbox_layout3.addWidget(self.solution_table[i])

			hd_finalDoc(final[0], -int(obj.table[-1][-1]))
			hd_toPhase2Doc()

			self.vbox_layout5.addWidget(self.create_label("Phase"))
			self.answers_label.setText(f"The Base solution is : {str({i:round(final[0][i],2) for i in list(final[0])[:len(obj.args[-1])]})}")

			a_count = len([x for x in obj.vars['artificial'] if x != -1])
			e_count = len([x for x in obj.vars['ecart'] if x != -1])

			phase_2 = []
			for index, row in enumerate(final[1]):
				phase_2.append([x for i,x in enumerate(row) if i < len(row) - (a_count + 1)] + [row[-1]])
			last_line_re = obj.args[-1] + [0]*(e_count+1)

			to_correct = obj._get_column_name()[:len(obj.args[-1])]
			ito_correct = {x:i for i,x in enumerate(final[2]["vb"]) if x in to_correct}

			old_vb = obj._get_base_vars()

			new_row = [0]*len(last_line_re)

			for i, elm in enumerate(to_correct):
				if elm in old_vb and last_line_re[i] != 0:
					for j, x in enumerate(phase_2[ito_correct[elm]]):
						multiplier = last_line_re[i] * x
						new_row[j] += last_line_re[j] - multiplier
					last_line_re = new_row
					new_row = [0]*len(last_line_re)

			phase_2[-1] = last_line_re
			self.vbox_layout5.addWidget(self.create_label("First Phase has ended !\nStarting Phase II"))
			if prob == 'max':
				next_obj = SimplexMax(A, b, c, ineq)
			elif prob == 'min':
				next_obj = SimplexMin(A, b, c, ineq)
			else:
				# print(f"{TC.B_RED}Problem type is invalid! Sorry Try again!{TC.NC}")
				self.vbox_layout5.addWidget(self.create_label("Problem type is invalid! Sorry Try again"))
				return;
			next_obj.vars['artificial'] = [-1]
			next_obj.table = phase_2
			real_final = next_obj.Solve()
			if (real_final == -1):
				self.answers_label.setText(f"This table has no Optimal Solution")
				return
			self.phase2_tables = []
			for i in range(0, len(real_final[3])):
				self.vbox_layout5.addWidget(self.create_label(f"Phase II table {i}"))
				# self.vbox_layout6.addWidget(self.create_label(final[-1][i]))
				self.phase2_tables.append(self.create_gui_for_tableau(np.array(real_final[3][i]), real_final[2]["vars"], real_final[4][i]))
				self.vbox_layout3.addWidget(self.phase2_tables[i])
			hd_finalDoc(real_final[0], -int(next_obj.table[-1][-1]))

			self.vbox_layout5.addWidget(self.create_label("Second Phase has ended"))
			self.answers_label.setText(f"Optimal Solution: {str({i:round(real_final[0][i],2) for i in list(real_final[0])[:len(obj.args[-1])]})}\nZ* Value: {-int(next_obj.table[-1][-1])}")
		hd_endDoc()

	def next_event(self):
		try:
			if (self.vbox_layout5.currentWidget().text() in ("This problem is a simple simplex","Solution","Second Phase has ended","First Phase has ended !\nStarting Phase II","Starting Phase II : ", "!First phase is end", "This problem is not a simple simplex - we need two phases -")):
				self.vbox_layout5.setCurrentIndex(self.vbox_layout5.currentIndex() + 1)
			else:
				self.vbox_layout5.setCurrentIndex(self.vbox_layout5.currentIndex() + 1)
				# self.vbox_layout6.setCurrentIndex(self.vbox_layout6.currentIndex() + 1)
				self.vbox_layout3.setCurrentIndex(self.vbox_layout3.currentIndex() + 1)
		except Exception as e:
			pass

	def back_event(self):
		try:
			if (self.vbox_layout5.currentWidget().text() in ("This problem is a simple simplex","Solution","Second Phase has ended","First Phase has ended !\nStarting Phase II","Starting Phase II : ", "!First phase is end", "This problem is not a simple simplex - we need two phases -")):
				self.vbox_layout5.setCurrentIndex(self.vbox_layout5.currentIndex() - 1)
			else:
				self.vbox_layout5.setCurrentIndex(self.vbox_layout5.currentIndex() - 1)
				# self.vbox_layout6.setCurrentIndex(self.vbox_layout6.currentIndex() + 1)
				self.vbox_layout3.setCurrentIndex(self.vbox_layout3.currentIndex() - 1)
		except Exception as e:
			pass


	def form_unaugmented_matrix(self):
		"""
			This function give us our inputed matrix
		"""
		obj_fxn = self.get_obj_fxn()
		split1_of_constraints = self.read_table_items(self.constraint_table, 0, self.constraint_table.rowCount(), 0, self.constraint_table.columnCount() - 2)
		split2_of_constraints = self.read_table_items(self.constraint_table, 0, self.constraint_table.rowCount(), self.constraint_table.columnCount() - 1, self.constraint_table.columnCount())
		unaugmented_matrix_without_obj_fxn = np.concatenate((np.array(split2_of_constraints), split1_of_constraints),axis=1)
		unaugmented_matrix = np.vstack((obj_fxn, unaugmented_matrix_without_obj_fxn))
		# print("unaugmented matrix", unaugmented_matrix)
		return unaugmented_matrix

	def read_table_items(self,table,start_row,end_row,start_col, end_col):
		read_table = np.zeros((end_row-start_row, end_col-start_col))
		for i in range(start_row,end_row):
			for j in range(start_col,end_col):
				read_table[i-end_row][j-end_col] = 0 if not table.item(i, j) else float(table.item(i, j).text())
		return read_table

	def read_equality_signs(self,equality_signs_column,table):
		equality_signs=[]
		for i in range(table.rowCount()):
			equality_signs.append(table.cellWidget(i, equality_signs_column).currentText())
		return equality_signs

	def populatetable(self,table, mylist, start_row, end_row, start_col, end_col):
		for i in range(start_row, end_row):
			for j in range(start_col, end_col):
				table.setItem(i, j, QTableWidgetItem(str(Fraction(str(mylist[i - end_row][j - end_col])).limit_denominator(10))))
		table.resizeColumnsToContents()

	def get_obj_fxn(self):
		obj_fxn_coeff=self.read_table_items(self.objective_fxn_table, 0,self.objective_fxn_table.rowCount(), 0, self.objective_fxn_table.columnCount()-2)
		obj_fxn = np.insert(obj_fxn_coeff,0,0)
		return obj_fxn

	def create_gui_for_tableau(self,tableau,all_variables,vertical_headers):
		rows,cols=tableau.shape
		gui_tableau=self.create_table(rows, cols, equality_signs=None,horizontal_headers=all_variables,vertical_headers=vertical_headers)
		self.populatetable(gui_tableau, tableau, 0,rows, 0, cols)
		gui_tableau.resizeColumnsToContents()
		return gui_tableau

	def update_gui_tableau(self,tableau,gui_tableau,current_row,vertical_headers):
		#create new rows and cols
		rows, cols = tableau.shape
		for i in range(rows):
			gui_tableau.insertRow(gui_tableau.rowCount())
		self.populatetable(gui_tableau, tableau, current_row, current_row+rows, 0,cols)
		gui_tableau.setVerticalHeaderLabels(vertical_headers)

	def displayInfo(self):
		# to show our second window
		self.show()

class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow,self).__init__()
		self.setWindowTitle('Simplex Solver')
		self.setFixedSize(800,400)
		self.setupUi()
		self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)

	def closeEvent(self):
		"""
			Close windows show a pop up before closing
		"""
		reply = QMessageBox.question(None, "Message",
			"Are you sure you want to quit?",
			QMessageBox.Close | QMessageBox.Cancel)
		if reply == QMessageBox.Close:
			app.quit()
		else:
			pass

	def getIntputConstVar(self):
		global INPUTVARS, INPUTCONST
		if (not self.VarsEdit.text() or not self.ConstEdit.text()):
			return
		if (int(self.VarsEdit.text()) <= 2 and int(self.ConstEdit.text()) >= 1):
			INPUTVARS = 2
			INPUTCONST = int(self.ConstEdit.text())
		elif (int(self.VarsEdit.text()) >= 2 and int(self.ConstEdit.text()) <= 1):
			INPUTVARS = int(self.VarsEdit.text())
			INPUTCONST = 1
		else:
			INPUTCONST = int(self.ConstEdit.text())
			INPUTVARS = int(self.VarsEdit.text())

		self.secondwindow = MWindow()
		self.secondwindow.displayInfo()


	def setupUi(self):
		font = QFont()
		font.setFamily("PT Mono")
		range = QIntValidator(0, 100)

		# self.Welcome = QLabel("Welcome to \nPy-simplex\ngenerator !", self)
		# self.Welcome.setGeometry(QRect(20, 0, 800,350))
		# self.Welcome.setFont(font)
		# self.Welcome.setStyleSheet("color:#d54554;font-size:70px")

		self.Varslabe = QLabel("Enter the number of variables: ", self)
		self.Varslabe.setStyleSheet("font-size:20px")
		self.Varslabe.setGeometry(QRect(240, 0, 800, 200))

		self.Constlabe = QLabel("Enter the number of constraints: ", self)
		self.Constlabe.setStyleSheet("font-size:20px")
		self.Constlabe.setGeometry(QRect(240, 0, 800, 450))

		self.VarsEdit = QLineEdit(self)
		self.VarsEdit.setGeometry(QRect(320, 150, 91, 21))
		self.VarsEdit.setValidator(range)

		self.ConstEdit = QLineEdit(self)
		self.ConstEdit.setGeometry(QRect(320, 280, 91, 21))
		self.ConstEdit.setValidator(range)

		self.generate = QPushButton(self)
		self.generate.setGeometry(QRect(630, 350, 113, 32))
		self.generate.setText("Generate")
		self.generate.clicked.connect(self.getIntputConstVar)

		# self.Exit = QPushButton(self)
		# self.Exit.setGeometry(QRect(500, 350, 113, 32))
		# self.Exit.setText("Exit")
		# self.Exit.clicked.connect(self.closeEvent)

		# self.help = QPushButton(self)
		# self.help.setGeometry(QRect(40, 350, 113, 32))
		# self.help.setText("Help")


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	sys.exit(app.exec())
