from futoshiki import FutoshikiRowConstraint, FutoshikiRelationConstraint


class SCP:
    """
    Constraint Satisfaction Problem engine

    Attributes:
        method          Method of problem solving:
                                        back    - backtracking
                                        forward - forward checking
        order           Method of ordering call stack:
                                        none    - stack is left in default order
        call_stack      List of variables in filling order
        constraints     Dictionary of variable: list of constraints its included into
        pointer         Index of variable currently changed, solving terminates when out of stack range
    """

    def __init__(self, method='back', order='none', dynamic_ordering=False):
        """
        Create empty SCP engine

        :param method:              Method of problem solving:
                                                    back    - backtracking
                                                    forward - forward checking
        :param order:               Method of ordering call stack
                                                    none    - stack is left in default order
        :param dynamic_ordering:    If stack should be ordered after each assigment
        """
        self.method = method
        self.order = order
        self.dynamic_ordering = dynamic_ordering

        self.call_stack = []
        self.constraints = dict()
        self.pointer = -1

        self.state = None

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
        with open(file_path) as f:
            # TODO return False when failed
            n = int(f.readline())  # Read the size
            default_domain = [v + 1 for v in range(n)]

            # Tmp structure for constraints definition
            self.state = [[] for i in range(n)]

            # Create variables
            for i in range(n):
                for j in range(n):
                    pos = (i, j)
                    var = _Variable(pos, default_domain.copy())

                    self.state[i].append(var)

                    self.call_stack.append(var)

            # Load constraints
            for line in f:
                line = line.rstrip()

                for side, *values in line.split(';'):
                    if side == 'G':
                        pass
                    elif side == 'D':
                        pass
                    elif side == 'L':
                        pass
                    elif side == 'P':
                        pass
                    # TODO create rows and columns constraints

        return True

    def _load_futoshiki_file(self, file_path):
        """
        Load futoshiki data from file

        :param file_path:   Path to data file

        :return:    If data was loaded successfully
        """
        with open(file_path) as f:
            # TODO return False when failed
            n = int(f.readline())  # Read the size
            default_domain = [v + 1 for v in range(n)]

            # Tmp structure for constraints definition
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

            # Create rows and columns constrains
            for i in range(n):
                row_vars = self.state[i]
                col_vars = [self.state[r][i] for r in range(n)]

                row_constraint = FutoshikiRowConstraint(row_vars)
                for var in row_vars:
                    self.constraints[var].append(row_constraint)

                col_constraint = FutoshikiRowConstraint(col_vars)
                for var in col_vars:
                    self.constraints[var].append(col_constraint)

        return True

    def _order_stack(self):
        """
        Arrange call stack
        """
        # TODO
        pass

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
        self._current_variable().pop_state()
        self._current_variable().value = None
        self.pointer -= 1

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
        # Check for empty domains when forward checking
        if self.method == 'forward':
            for var in self.call_stack[self.pointer + 1:]:
                if not var.domain_size():
                    return False

        # Check current variable constraints
        current_var = self._current_variable()
        for constraint in self.constraints[current_var]:
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

        if self.method == 'forward':
            self._purge()

    def _purge(self):
        """
        Purge values with current variable constraint
        """
        current_var = self._current_variable()
        for constraint in self.constraints[current_var]:
            constraint.purge(current_var)

    def _reverse_purge(self):
        """
        Reverse last purge
        """
        current_var = self._current_variable()
        for constraint in self.constraints[current_var]:
            constraint.purge(current_var, reverse=True)

    def run(self):
        """
        Solve problem and return final state

        :return:    Final state if successful or None if failed
        """
        self._order_stack()

        self._step_forward()
        while self.pointer < len(self.call_stack):
            if self._check():
                self._step_forward()
            else:
                if self.method == 'forward':
                    self._reverse_purge()
                while not self._current_variable().domain_size():
                    self._step_backward()
                    if self.pointer < 0:
                        return None
                self._load_value()

        return self.state

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
