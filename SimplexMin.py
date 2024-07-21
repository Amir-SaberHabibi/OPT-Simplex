from Simplex import *

class SimplexMin(Simplex):

    def can_be_improved(self):
        z = self.table[-1]
        return any(round(x, 10) < 0 for x in z[:-1])

    def pivot_position(self):
        z = list(x for x in self.table[-1])
        min = z[0]
        column = 0
        for i, elm in enumerate(z[:-1]):
            if (elm < 0):
                if min > elm:
                    column = i
                    min = elm
        return (column)

    def get_pivot_position(self):
        z = self.table[-1]
        column = self.pivot_position()

        ratio = []
        for row in self.table[:-1]:
            el = row[column]
            ratio.append(math.inf if el <= 0 else row[-1] / el)
        row = -1 if all(x == math.inf for x in ratio) else ratio.index(min(ratio))
        return row, column

    def Solve(self):
        self.tables_log = []
        self.vb_bars_log = []
        self.pivot_log = []
        self.prob = "min"
        # print(f"{TC.B_YELLOW}--> initial table :{TC.NC}")
        pivot_position = self.get_pivot_position()
        column_name = self._get_column_name() + ['RHS']
        vb_init = self._get_base_vars() + ['C']
        vb_vars = self._update_base_vars(pivot_position, vb_init)
        self.vb_bars_log.append(vb_init)
        self.tables_log.append(self.table)
        try:
            # print(f"{TC.B_WHITE}",pd.DataFrame(self._setup_fraction(), columns=column_name, index=vb_init),f"{TC.NC}")
            # print(f"{TC.B_GREEN}#> Pivot is : {self._setup_fraction()[pivot_position[0]][pivot_position[1]]} in position {pivot_position}{TC.NC}")
            self.pivot_log.append(f"#> Pivot is : {self._setup_fraction()[pivot_position[0]][pivot_position[1]]} in position {pivot_position}")
            self.doc += self._make_table(self._table_to_print(self._setup_fraction(), column_name, vb_init), "Initial")
        except Exception as e:
            # print("Simplex END!")
            return -1

        if not self.can_be_improved():
            self.doc += self._final_table_msg()
        else:
            self.doc += self._iteration_msg(column_name[pivot_position[1]], vb_init[pivot_position[0]])

        # user_pivot = literal_eval(input(f"{TC.B_PURPLE}Enter Your pivot position (i, j) else type None: {TC.NC}"))
        # if user_pivot != None:
        #     pivot_position = user_pivot
        if pivot_position[0] == -1:
            # print("end of simplex")
            return -1

        # print("_"*100+"\n")
        i = 1
        while self.can_be_improved():
            column_name = self._get_column_name() + ['RHS']
            vb_vars = self._update_base_vars(pivot_position, vb_vars)
            self.vb_bars_log.append(vb_vars)
            self.table = self.pivot_step(pivot_position)
            self.tables_log.append(self.table)
            pivot_position = self.get_pivot_position()
            # print(f'{TC.B_YELLOW}--> table d\'iteration {i}:{TC.NC}')
            # print(f"{TC.B_WHITE}", pd.DataFrame(self._setup_fraction(), columns=column_name, index=vb_vars), f"{TC.NC}")
            self.doc += self._make_table(self._table_to_print(self._setup_fraction(), column_name, vb_vars), f"Iteration {i}")

            if self.can_be_improved():
                self.doc += self._iteration_msg(column_name[pivot_position[1]], vb_vars[pivot_position[0]])
                # print(f"{TC.B_GREEN}#> Pivot is : {self._setup_fraction()[pivot_position[0]][pivot_position[1]]} in position {pivot_position}{TC.NC}")
                self.pivot_log.append(f"#> Pivot is : {self._setup_fraction()[pivot_position[0]][pivot_position[1]]} in position {pivot_position}")
                # print("_"*100+"\n")
                # user_pivot = literal_eval(input(f"{TC.B_PURPLE}Enter Your pivot position (i, j) else type None: {TC.NC}"))
                # if user_pivot != None:
                #     pivot_position = user_pivot
                if pivot_position[0] == -1:
                    # print("end of simplex")
                    return -1
            i += 1
        # print(f"{TC.B_RED}!this table is a finale{TC.NC}")
        self.doc += self._final_table_msg()
        # self.tables_log.append(self.table)
        # self.vb_bars_log.append(vb_vars)

        self._print_doc()
        return self.get_solution(), self.table, {"vars" : column_name, "vb":vb_vars}, self.tables_log, self.vb_bars_log,  self.pivot_log
