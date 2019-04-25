from time import time

from futoshiki import FutoshikiRowConstraint, FutoshikiRelationConstraint
from skyscrapper import SkyscrapperRowConstraint, SkyscrapperVisibilityConstraint


class SCP:
    """
    Constraint Satisfaction Problem engine

    Attributes:
        method              Method of problem solving:
                                            back    - backtracking
                                            forward - forward checking
        order               Method of ordering call stack:
                                            none    - stack is left in default order
                                            max_dom - max to min domain size
                                            min_dom - min to max domain size
                                            max_con - max to min constraint num
                                            min_con - min to max constraint num
        dynamic_ordering    If call stack is being ordered during the search
        all_solutions       If all solutions should be found
        call_stack          List of variables in filling order
        initial_constraints List of pairs (constraint, variable) which should be purged at the beginning
        constraints         Dictionary of variable: list of constraints its included into
        pointer             Index of variable currently changed, solving terminates when out of stack range
        state               Current problem state
        solutions           List of found solutions
    """

    def __init__(self, method='back', order='none', dynamic_ordering=False, all_solutions=False):
        """
        Create empty SCP engine

        :param method:              Method of problem solving:
                                                    back    - backtracking
                                                    forward - forward checking
        :param order:               Method of ordering call stack
                                                    none    - stack is left in default order
                                                    max_dom - max to min domain size
                                                    min_dom - min to max domain size
                                                    max_con - max to min constraint num
                                                    min_con - min to max constraint num
        :param dynamic_ordering:    If stack should be ordered after each assigment
        :param all_solutions:       If all possible solutions should be found
        """
        self.method = method
        self.order = order
        self.dynamic_ordering = dynamic_ordering
        self.all_solutions = all_solutions

        self.call_stack = []
        self.initial_constraints = []
        self.constraints = dict()
        self.pointer = -1

        self.state = None
        self.solutions = []

        self.start_time = None
        self.end_time = None
        self.returns = 0
        self.validations = 0

    def load_data(self, file_path, type_=None):
        """
        Load data from file

        :param file_path:   Path to data file
        :param type_:       Type of problem:
                                        None    - Base on file name
                                        futo    - Futoshiki
                                        sky     - Skyscrapper

        :return:    If data was loaded successfully
        """
        if type_ is None:
            # Guess data type base on file name
            file_types = {
                'futoshiki': 'futo',
                'skyscrapper': 'sky'
            }
            separator = '/' if '/' in file_path else '\\'
            file_name = file_path.split(separator)[-1].lower()
            for _, t in file_types.items():
                if t in file_name:
                    type_ = t
                    break

        if type_ == 'futo':
            return self._load_futoshiki_file(file_path)
        elif type_ == 'sky':
            return self._load_skyscrapper_file(file_path)
        else:
            print('Wrong file type')
            return False

    def _load_skyscrapper_file(self, file_path):
        """
        Load skyscrapper data from file

        :param file_path:   Path to data file

        :return:    If data was loaded successfully
        """
        try:
            f = open(file_path)
        except IOError:
            return False
        with f:
            n = int(f.readline())  # Read the size
            default_domain = [v + 1 for v in range(n)]

            self.state = [[] for i in range(n)]

            # Create variables
            for i in range(n):
                for j in range(n):
                    pos = (i, j)
                    var = _Variable(pos, default_domain.copy())

                    self.constraints[var] = []
                    self.state[i].append(var)
                    self.call_stack.append(var)

            columns = [[row[i] for row in self.state] for i in range(len(self.state))]

            # Load constraints
            for line in f:
                line = line.rstrip()
                side, *values = line.split(';')

                if side == 'G':
                    constraint_rows = columns
                elif side == 'D':
                    constraint_rows = (list(reversed(c)) for c in columns)
                elif side == 'L':
                    constraint_rows = self.state
                elif side == 'P':
                    constraint_rows = (list(reversed(r)) for r in self.state)

                for row, val in zip(constraint_rows, map(int, values)):
                    constraint_row = SkyscrapperRowConstraint(row)
                    if val != 0:
                        constraint_vis = SkyscrapperVisibilityConstraint(row, val)
                        self.initial_constraints.append((constraint_vis, None))

                    for var in row:
                        self.constraints[var].append(constraint_row)
                        if val != 0:
                            self.constraints[var].append(constraint_vis)

        return True

    def _load_futoshiki_file(self, file_path):
        """
        Load futoshiki data from file

        :param file_path:   Path to data file

        :return:    If data was loaded successfully
        """
        try:
            f = open(file_path)
        except IOError:
            return False
        with f:
            n = int(f.readline())  # Read the size
            default_domain = [v + 1 for v in range(n)]

            self.state = [[] for i in range(n)]

            # Load variables
            f.readline()  # Skip 'START:'
            for i in range(n):
                row = f.readline().rstrip()
                cells = row.split(';')

                # Load variables for row
                for j, val in enumerate(cells):
                    val = int(val)
                    domain = default_domain.copy() if val == 0 else [val]
                    pos = (i, j)

                    var = _Variable(pos, domain)
                    self.state[i].append(var)
                    self.constraints[var] = []

                    # Add only mutable variables to stack
                    if not var.fixed:
                        self.call_stack.append(var)

            # Load relations
            f.readline()  # Skip 'REL:'
            for line in f:
                line = line.rstrip()
                if line == '':
                    continue
                cell1, cell2 = line.split(';')

                row1 = ord(cell1[0]) - 65
                col1 = int(cell1[1:]) - 1

                row2 = ord(cell2[0]) - 65
                col2 = int(cell2[1:]) - 1

                var1 = self.state[row1][col1]
                var2 = self.state[row2][col2]

                constraint = FutoshikiRelationConstraint(var1, var2)
                self.constraints[var1].append(constraint)
                self.constraints[var2].append(constraint)

                # Add initial constraints for fixed values
                if var1.fixed:
                    self.initial_constraints.append((constraint, var1))
                if var2.fixed:
                    self.initial_constraints.append((constraint, var2))

            # Create rows and columns constrains
            for i in range(n):
                row_vars = self.state[i]
                col_vars = [self.state[r][i] for r in range(n)]

                row_constraint = FutoshikiRowConstraint(row_vars)
                col_constraint = FutoshikiRowConstraint(col_vars)
                for row_var, col_var in zip(row_vars, col_vars):
                    self.constraints[row_var].append(row_constraint)
                    self.constraints[col_var].append(col_constraint)

                    # Add initial constraints for fixed values
                    if row_var.fixed:
                        self.initial_constraints.append((row_constraint, row_var))
                    if col_var.fixed:
                        self.initial_constraints.append((col_constraint, col_var))

        return True

    def _order_stack(self):
        """
        Arrange call stack
        """
        if self.order == 'max_dom':
            def key_(v):
                return -v.domain_size
        elif self.order == 'min_dom':
            def key_(v):
                return v.domain_size
        elif self.order == 'max_con':
            def key_(v):
                return -len(self.constraints[v])
        elif self.order == 'min_con':
            def key_(v):
                return len(self.constraints[v])
        else:
            def key_(v):
                return 0

        self.call_stack[self.pointer + 1:] = sorted(self.call_stack[self.pointer + 1:], key=key_)

    def _step_forward(self):
        """
        Move pointer one step forward and prepare variable
        """
        self.pointer += 1
        if self.pointer < len(self.call_stack):
            self._current_variable().push_state()
            self._load_value()

    def _step_backward(self):
        """
        Move pointer one step backward
        """
        current_var = self._current_variable()
        current_var.pop_state()
        current_var.value = None
        self.pointer -= 1

        self.returns += 1

        if self.method == 'forward' and self.pointer > -1:
            self._reverse_purge()

    def _current_variable(self):
        """
        Get current variable

        :return:    Current variable
        """
        return self.call_stack[self.pointer]

    def _check(self):
        """
        Check if current state is legitimate

        :return:    If state is valid
        """
        current_var = self._current_variable()
        for constraint in self.constraints[current_var]:
            self.validations += 1
            if not constraint.check():
                return False

        return True

    def _load_value(self):
        """
        Load next value to current variable

        When forward checking, before purging with new value last state must be restored
        """
        current_var = self._current_variable()
        current_var.next_value()

    def _initial_purge(self):
        """
        Purge values with fixed variables

        :return:    If purge was successful
        """
        success = True
        if self.method == 'back':
            return True

        for constraint, var in self.initial_constraints:
            self.validations += 1
            if not constraint.purge(var):
                return False

        return success

    def _purge(self):
        """
        Purge values with current variable constraint

        :return:    If purge was successful
        """
        success = True
        current_var = self._current_variable()
        for constraint in self.constraints[current_var]:
            self.validations += 1
            if not constraint.purge(current_var):
                success = False

        return success

    def _reverse_purge(self):
        """
        Reverse last purge
        """
        current_var = self._current_variable()
        for constraint in self.constraints[current_var]:
            constraint.reverse_purge(current_var)

    def show_stats(self):
        """
        Print statistics about last calculations
        """
        time_delta = round(self.end_time - self.start_time, 6)

        print(f'Calculated in {time_delta}s, with {self.returns} returns and {self.validations} validations')

    def get_stats(self):
        """
        Get statistics about last calculation

        :return: time_delta, returns, validations
        """
        time_delta = round(self.end_time - self.start_time, 6)

        return time_delta, self.returns, self.validations

    def run(self):
        """
        Solve problem and return final state

        :return:    Final state if successful or None if failed
        """
        self.start_time = time()

        # Initial constraints check and ordering
        self._order_stack()
        forward_integrity = self._initial_purge()
        if not forward_integrity:
            self.end_time = time()
            return None

        self._step_forward()
        while True:
            # Order
            if self.dynamic_ordering:
                self._order_stack()

            # Solution found
            if self.pointer == len(self.call_stack):
                self._save_state_as_solution()
                if not self.all_solutions:
                    self.end_time = time()
                    return None

                self.pointer -= 1
                forward_integrity = False

            # Integrity
            elif self.method == 'forward':
                forward_integrity = self._purge()
            else:
                forward_integrity = self._check()

            if forward_integrity:
                self._step_forward()
            else:
                if self.method == 'forward':
                    self._reverse_purge()
                while not self._current_variable().domain_size:
                    self._step_backward()
                    if self.pointer < 0:
                        self.end_time = time()
                        return None
                self._load_value()

    def _save_state_as_solution(self):
        """
        Save current state as solution
        """
        current_state = [[v.value for v in row] for row in self.state]

        self.solutions.append(current_state)

    def show_solutions(self):
        """
        Show all saved solutions
        """
        if self.solutions:
            for solution in self.solutions:
                for row in solution:
                    print(row)
                print('=' * 25)
            print(f'Found {len(self.solutions)} solutions')
        else:
            print('No solutions found')

    def visualize(self):
        """
        Visualize current state
        """
        for row in self.state:
            print([v.value for v in row])


class _Variable:
    """
    Single variable in problem

    Attributes:
        id_             Unique variable identifier
        domain          Domain of the variable
        state_stack     Stack of domain states
        value           Current value of the variable
        fixed           If variable value is fixed
    """

    def __init__(self, id_, domain):
        """
        Create variable with given domain

        :param id_:     Variable identifier
        :param domain:  Variables domain
        """
        self.id_ = id_
        self.domain = domain
        self.state_stack = []
        if len(domain) == 1:
            self.value = domain[0]
            self.fixed = True
        else:
            self.value = None
            self.fixed = False

    def __str__(self):
        """
        Create text representation of variable

        :return:    Text representation
        """
        return f'ID: {self.id_} | V: {self.value} | D: {self.domain}'

    def __eq__(self, other):
        """
        Check if objects are equal

        :param other:   Object to compare to

        :return:    If objects are equal
        """
        return self.id_ == other.id_

    def __ne__(self, other):
        """
        Check if objects are different

        :param other:   Object to compare to

        :return:    If objects are equal
        """
        return not (self == other)

    def __hash__(self):
        """
        Get objects hash

        :return:    Objects hash
        """
        return hash(self.id_)

    def push_state(self):
        """
        Push domain state onto stack
        """
        self.state_stack.append(self.domain.copy())

    def pop_state(self):
        """
        Pop domain state from stack
        """
        self.domain = self.state_stack.pop()

    @property
    def domain_size(self):
        """
        Get size of domain

        :return:    Size of domain
        """
        return len(self.domain)

    def next_value(self):
        """
        Set variables value to next value from work domain
        """
        self.value = self.domain.pop()

    def filter_domain(self, predicate):
        """
        Filter work domain with given predicate

        :param predicate:    Predicate to filter with
        """
        self.domain = list(filter(predicate, self.domain))
