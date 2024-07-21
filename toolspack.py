from fractions import Fraction
# from pdflatex import PDFLaTeX
# import os, platform, subprocess
# from tex import latex2pdf
# from ast import literal_eval

class TC:
	B_WHITE = '\033[1;37m'
	RED = '\033[0;31m'
	GREEN = '\033[0;32m'
	CYAN = '\033[0;36m'
	B_CYAN = '\033[1;36m'
	B_GREEN = '\033[1;32m'
	B_BLUE = '\033[1;34m'
	BLUE = '\033[0;34m'
	PURPLE = '\033[0;35m'
	B_PURPLE = '\033[1;35m'
	YELLOW = '\033[0;33m'
	B_YELLOW = '\033[1;33m'
	B_RED = '\033[1;31m'
	NC = '\033[0m'

PHASE_1_MSG = '''
The iterations of the first phase are
finished and there is some possible solution to the problem.
We eliminate the artificial variables and go to the second phase:
'''

# def plot_graph(A, b, c , ineq):
#     print(A, b, c ,ineq)


### Problem Helper Functions
def hp_normalize_problem(A, b, c, ineq):
    for i in range(len(b)):
        if b[i] < 0:
            b[i] *= -1
            A[i] = [-x for x in A[i]]
            ineq[i] = '>=' if ineq[i] == '<=' else '<=' if ineq[i] == '>=' else ineq[i]

def hp_is_simple(b, ineq):
    for i in range(len(ineq)):
        if ineq[i] == '>=':
            return False
        elif ineq[i] == '=' and b[i] != 0:
            return False
    return True

def hp_what_problem():
    user_input = input(f"{TC.B_PURPLE}is your problem is (min)-Minimization or (max)-Maximization :{TC.NC}")
    if user_input == 'max':
       return ('max')
    elif user_input == 'min':
        return ('min')
    else:
        return (0)


### Exporting Document Helper Functions
def hd_startDoc():
    doc = (r"\documentclass{article}"
            r"\usepackage{amsmath}"
            r"\begin{document}"
            r"\title{Simplex Solver}"
            r"\maketitle"
            r"\begin{flushleft}"
            r"\textbf{Problem}"
            r"\end{flushleft}"
            r"\begin{flushleft}Given the following linear system and \
            objective function, find the optimal solution.\end{flushleft}")
    with open("Solution.tex", "w") as tex:
            tex.write(doc)

def hd_endDoc():
    doc = r"\end{document}"
    with open("Solution.tex", "a") as tex:
        tex.write(doc)

def hd_toPhase2Doc():
    doc = r"!First phase is end"
    doc += r"The iterations of the first phase are finished"
    doc += r"and there is some possible solution to the problem. \\"
    doc += r"We eliminate the artificial variables and go to the second phase.\\"
    with open("Solution.tex", "a") as tex:
        tex.write(doc)

def hd_finalDoc(solution, Z):
    doc = r"\begin{equation*}"
    for key, val in solution.items():
        doc += f"{key} = {Fraction(str(val)).limit_denominator(10)}; "
    doc += f"Z = {Z} " + r"\end{equation*} \\"
    with open("Solution.tex", "a") as tex:
        tex.write(doc)

def hd_get_prob_ineq(A,b, ineq):
        """Formatting problem constraint

        Returns:
            doc: Latex format to string
        """
        doc = r"\[\left\{\begin{array}"
        for i, row in enumerate(A):
            for j, el in enumerate(row):
                if el > 0:
                    doc += f"+ {el}x_{j+1} "
                elif el < 0:
                    doc += f"{el}x_{j+1} "
                elif el == 0:
                    doc += ""
            if ineq[i] == '>=':
                doc += r"\geq "+f" {b[i]}"+r"\\"
            elif ineq[i] == '<=':
                doc += r"\leq "+f" {b[i]}"+r"\\"
            else:
                doc += r"\eq "+f" {b[i]}"+r"\\"
        doc += r"\end{array}\right.\] \\ \\ \begin{flushleft}\textbf{Solution}\end{flushleft} \\"
        return (doc)

def hd_get_object_func(prob, c):
        """Formatting problem objective function

        Returns:
            doc: LateX format to String
        """
        doc = r"\\" + f"{prob}" + r"{ z = "
        for i,el in enumerate(c):
            if el >= 0:
                doc += f"+{el}x_{i+1} "
            elif el <= 0:
                doc += f"-{el}x_{i+1} "
        doc += r" } \\ \begin{flushleft}\textbf{Problem}\end{flushleft} \\"
        return (doc)

def hd_set_Problem(A, c, b, ineq, prob):
        """set problem equation and conver it to LateX

        Returns:
            doc: LateX format to String
        """
        doc = (r"\begin{equation*}"+
            hd_get_object_func(prob, c)+
            hd_get_prob_ineq(A,b, ineq)+
            r"\end{equation*}")
        with open("Solution.tex", "a") as tex:
            tex.write(doc)

# def export():
#     print("Coming soon")