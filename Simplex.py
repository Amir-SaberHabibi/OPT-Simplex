import numpy as np
import pandas as pd
import math, copy
from fractions import Fraction
from toolspack import *

class Simplex():
    def __init__(self, a=None, B=None, C=None, ineq=None):
        self.prob = "max"
        self.args = [a, B, C]
        self.ineq = ineq
        self.vars = self.get_vars_list()
        self.c = self._make_c()
        self.A = self._make_A()
        self.b = B
        self.table = self.to_table()
        self.doc = ""

    def _normalize_problem(self):
        for i in range(len(self.b)):
            if self.b[i] < 0:
                self.b[i] *= -1
                self.A[i] = [-x for x in self.A[i]]
                self.ineq[i] = '>=' if self.ineq[i] == '<=' else '<=' if self.ineq[i] == '>=' else self.ineq[i]
        self.table = self.to_table

    def to_table(self):
        body = [row + [x] for row, x in zip(self.A, self.b)]
        z = self.c + [0]
        return body + [z]

    def _setup_fraction(self):
        new_table = []
        for raw in self.table:
            new_raw = [Fraction(str(x)).limit_denominator(10) for x in raw]
            new_table.append(new_raw)
        return (new_table)

    def is_basic(self, column):
        return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1

    def get_solution(self):
        columns = np.array(self.table).T
        solutions = {}
        for column, name in zip(columns, self._get_column_name()):
            solution = 0
            if self.is_basic(column):
                one_index = column.tolist().index(1)
                solution = columns[-1][one_index]
            solutions[name] = solution
        return solutions

    def pivot_step(self, pivot_position):
        new_table = [[] for eq in self.table]

        i, j = pivot_position
        pivot_value = self.table[i][j]
        new_table[i] = np.array(self.table[i]) / pivot_value

        for eq_i, eq in enumerate(self.table):
            if eq_i != i:
                multiplier = np.array(new_table[i]) * self.table[eq_i][j]
                new_table[eq_i] = np.array(self.table[eq_i]) - multiplier

        return new_table

    def get_vars_list(self):
        vars_count = len(self.args[2])
        # e_vars_count = [i for i,x in enumerate(self.ineq) if x != '=']
        e_vars_count = [i if x != '=' else -1 for i,x in enumerate(self.ineq)]
        # a_vars_count = [i for i,x in enumerate(self.ineq) if x != '=' and x != '<=']
        a_vars_count = [i if x != '<=' and self.args[1][i] != 0 else -1 for i,x in enumerate(self.ineq)]
        return {"decision": vars_count, "ecart":e_vars_count, "artificial":a_vars_count}

    def _make_c(self):
        tmp = copy.deepcopy(self.args[2])
        e_count = len([x for x in self.vars["ecart"] if x != -1])
        a_count = len([x for x in self.vars["artificial"] if x != -1])
        return tmp + [0]*(e_count + a_count)

    def _make_A(self):
        tmp = copy.deepcopy(self.args[0])
        e_var_index = self.vars["ecart"]
        a_var_index = self.vars["artificial"]
        e_flag = False if len(e_var_index) == 0 else True
        a_flag = False if len(a_var_index) == 0 else True
        if e_flag :
            for i , row in enumerate(tmp):
                if self.ineq[i] == '=':
                    for k in range(len([el for el in e_var_index if el != -1])):
                        row.append(0)
                if i in e_var_index:
                    for j in range(len(self.ineq)):
                        if j not in e_var_index and not a_flag:
                            continue
                        if j == i:
                            if self.ineq[j] == '<=':
                                row.append(1)
                            else:
                                row.append(-1)
                        elif e_var_index[j] != -1:
                            row.append(0)
        if a_flag :
            for i , row in enumerate(tmp):
                if i in a_var_index:
                    for j in range(len(self.ineq)):
                        if j == i:
                            row.append(1)
                        elif a_var_index[j] != -1:
                            row.append(0)
                else :
                    for el in range(len([x for x in a_var_index if x != -1])):
                        row.append(0)
        return tmp

    def _get_column_name(self):
        _1 = [f'X{i+1}' for i in range(len(self.args[-1]))]
        # e_vars_count = len([x for x in self.vars["ecart"] if x != -1])
        # a_vars_count = len([x for x in self.vars["artificial"] if x != -1])

        _2 = [f'S{i+1}' for i in self.vars["ecart"] if i != -1]
        _3 = [f'R{i+1}' for i in self.vars["artificial"] if i != -1]
        # _2 = [f'E{i+1}' for i in range(e_vars_count)]
        # _3 = [f'A{i+1}' for i in range(a_vars_count)]
        return _1 + _2 + _3

    def _get_base_vars(self):
        tmp = np.array(self.table).T
        col = self._get_column_name()
        vb_vars = []
        for index, column in enumerate(tmp):
            if self.is_basic(column):
                vb_vars.append(col[index])
        ret = sorted(vb_vars, key=lambda x: int(x[-1]))
        return (ret)

    def _update_base_vars(self, pivot_position, vb):
        init = copy.deepcopy(vb)
        column = self._get_column_name()
        i, j = pivot_position
        init[i] = column[j]
        return (init)

    # TODO
    def _init_1st_phase(self):
        phase_1_args = [self.A, self.b, self.c]
        e_vars_count = len([x for x in self.vars["ecart"] if x != -1])
        a_vars_count = len([x for x in self.vars["artificial"] if x != -1])
        e_vars_index = self.vars["ecart"]
        a_vars_index = self.vars["artificial"]
        # print(a_vars_index,  e_vars_index)
        a_column = []
        tmp = 0
        for i in a_vars_index:
            if i == -1:
                a_column.append(-1)
            else:
                a_column.append(tmp + e_vars_count + len(self.args[-1]))
                tmp += 1
        corr_last_line = self.to_table()
        row =  [0] * len(corr_last_line[0])
        for index in a_vars_index:
            if index == -1:
                continue
            else:
                for j in range(len(corr_last_line[index])):
                    if j in a_column:
                        row[j] = 0
                    else:
                        row[j] += corr_last_line[index][j]
        corr_last_line[-1] = [-x for x in row]
        corr_last_line[-1][-1] *= -1
        return (corr_last_line)

    ### Document exporting
    def _startDoc(self):
        """Init document header
        """
        self.doc = (r"\documentclass{article}"
                    r"\usepackage{amsmath}"
                    r"\begin{document}"
                    r"\title{Simplex Solver}"
                    r"\maketitle"
                    r"\begin{flushleft}"
                    r"\textbf{Problem}"
                    r"\end{flushleft}")

    def _init_problem_doc(self):
        """Init problem script
        """
        self.doc += (r"\begin{flushleft}Given the following linear system and \
            objective function, find the optimal solution.\end{flushleft}")

    def _set_Problem(self):
        """set problem equation and conver it to LateX

        Returns:
            STR: LateX format to String
        """
        STR = (r"\begin{equation*}"+
                     self._get_object_func()+
                     self._get_prob_ineq()+
                     r"\end{equation*}")
        return (STR)

    def _get_object_func(self):
        """Formatting problem objective function

        Returns:
            STR: LateX format to String
        """
        STR = r"\\" + f"{self.prob}" + r"{ z = "
        for i,el in enumerate(self.args[-1]):
            if el >= 0:
                STR += f"+{el}x_{i+1} "
            elif el <= 0:
                STR += f"-{el}x_{i+1} "
        STR += r" } \\ \begin{flushleft}\textbf{Solution}\end{flushleft} \\"
        return (STR)

    def _get_prob_ineq(self):
        """Formatting problem constraint

        Returns:
            STR: Latex format to string
        """
        STR = r"\[\left\{\begin{array}"
        for i, row in enumerate(self.args[0]):
            for j, el in enumerate(row):
                if el > 0:
                    STR += f"+ {el}x_{j+1} "
                elif el < 0:
                    STR += f"- {el}x_{j+1} "
                elif el == 0:
                    STR += ""
            if self.ineq[i] == '>=':
                STR += r"\geq "
                STR += f"{self.b[i]} \\"
            elif self.ineq[i] == '<=':
                STR += r"\leq "
                STR += f"{self.b[i]} \\"
            else:
                STR += r"\eq "
                STR += f"{self.b[i]} \\"
        STR += r"\end{array}\right.\] \\ \\ \begin{flushleft}\textbf{Solution}\end{flushleft} \\"
        return (STR)

    def _make_table(self, table, name):
        """Formatting table to LateX

        Args:
            name (STR):  of the table

        Returns:
            STR: Latex format to string
        """
        length = len(table[0])
        STR = r"\rightarrow " + f"table "+ r"\hspace{2}"+ f" {name}" + r"\\ \\ \begin{center}\begin{tabular}{"
        for i in range(length):
            STR += r"|c"
        STR += r"|} \hline "
        for i, row in enumerate(table):
            for j, el in enumerate(row):
                if j != len(row)-1:
                    STR += f" {el} & "
                else:
                    STR += f"{el} "

            STR += r"\\ \hline "
        STR += r" \end{tabular} \end{center} \\"
        return (STR)

    def _iteration_msg(self, entering, departing):
        """Formatting iteration message to LateX

        Args:
            entering (STR): entering variable
            departing (STR): departing variable

        Returns:
            STR: Latex format to string
        """
        STR = r"The current solution is not optimal."
        STR += r"Thus, pivot to improve the current solution. The entering variable is "
        STR += f" {entering} " + r" and the departing variable is "
        STR += f" {departing}. " + r" \\"
        return (STR)

    def _final_table_msg(self):
        """Formatting finale table message

        Returns:
            STR: Latex format to string
        """
        if self.prob == "min":
            tmp = "negative"
        elif self.prob == "max":
            tmp = "positive"
        STR = r"There are no "+f" {tmp} "+r"elements in the bottom row, so we know the solution is"
        STR += r"optimal. Thus, the solution is : \\"
        return (STR)

    def _phase_1_msg(self):
        """Formatting transfer message from

        Returns:
            STR: Latex format to string
        """
        STR = r"!First phase is end"
        STR += r"The iterations of the first phase are finished"
        STR += r"and there is some possible solution to the problem. \\"
        STR += r"We eliminate the artificial variables and go to the second phase.\\"
        return (STR)

    def _print_solution(self, solution, Z):
        """Formatting problem solution to Latex

        Args:
            solution (Dictionary): problem solution
            Z (int): optimal objective value

        Returns:
            STR: Latex format to string
        """
        STR = r"\begin{equation*}"
        for key, val in solution.items():
            STR += f"{key} = {val}, "
        STR += f"Z = {Z} " + r"\end{equation*} \\"
        return (STR)

    def _table_to_print(self, table, col_name, base_v):
        tmp = np.array(copy.deepcopy(table))
        up = np.array(['vb'] + col_name)
        base = np.array([base_v]).T
        _1 = np.hstack((base, table))
        _2 = np.vstack((up, _1))
        _3 = list([list(row) for row in _2])
        return (_3)

    def _print_doc(self):
        """export the file to LateX format
        """
        # self.doc += (r"\end{document}")
        with open("Solution.tex", "a") as tex:
            tex.write(self.doc)





