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

    def __init__(self, method='back', order='none'):
        """
        Create empty SCP engine

        :param method:  Method of problem solving:
                                        back    - backtracking
                                        forward - forward checking
        :param order:   Method of ordering call stack
                                        none    - stack is left in default order
        """
        self.method = method
        self.order = order
        self.call_stack = []
        self.constraints = dict()
        self.pointer = 0

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
            for word, t in file_types.items():
                if word in file_name:
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
            tmp_table = [[] for i in range(n)]

            # Create variables
            for i in range(n):
                for j in range(n):
                    pos = (i, j)
                    var = _Variable(pos, default_domain)

                    tmp_table[i].append(var)

                    self.call_stack.append(var)

            # Load constraints
            for line in f:
                line = line.rstrip()

                for side, *vals in line.split(';'):
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
            tmp_table = [[] for i in range(n)]

            # Load variables
            f.readline()  # Skip 'START:'
            for i in range(n):
                row = f.readline().rstrip()
                cells = row.split(';')

                # Load variables for row
                for j, val in enumerate(cells):
                    val = int(val)
                    domain = tuple(default_domain) if val == 0 else (val,)
                    pos = (i, j)

                    var = _Variable(pos, domain)
                    tmp_table[i].append(var)

                    # Add only mutable variables to stack
                    if not var.fixed:
                        self.call_stack.append(var)

            # Load relations
            f.readline()  # Skip 'REL:'
            for line in f:
                line = line.rstrip()
                cell1, cell2 = line.split(';')

                row1 = ord(cell1[0]) - 65
                col1 = int(cell1[1:])

                row2 = ord(cell2[0]) - 65
                col2 = int(cell2[1:])

                var1 = tmp_table[row1][col1]
                var2 = tmp_table[row2][col2]

                # TODO create constraint var1 < var2

            # Create rows and columns constrains
            for i in range(n):
                row_vars = tmp_table[i]
                col_vars = [tmp_table[r][i] for r in range(n)]

                # TODO create rows and columns constraints

        return True

    def _order_stack(self, method):
        """
        Arrange call stack
        """
        # TODO
        pass

    def _step_forward(self):
        """
        Move pointer one step forward and prepare variable
        """
        # TODO
        pass

    def _step_backward(self):
        """
        Move pointer one step backward
        """
        # TODO
        pass

    def run(self):
        """
        Start problem solving
        """
        # TODO
        pass


class _Variable:
    """
    Single variable in system

    Attributes:
        id_             Unique variable identifier
        domain          Domain of the variable, immutable
        work_domain     Modifiable domain used for value picking
        value           Current value of the variable
        fixed           If variable value is fixed
    """

    def __init__(self, id_, domain):
        """
        Create variable with given domain

        :param id_:     Variable identifier
        :param domain:  Immutable domain
        """
        self.id_ = id_
        self.domain = domain
        self.work_domain = None
        if len(domain) == 1:
            self.value = domain[0]
            self.fixed = True
        else:
            self.value = None
            self.fixed = False

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

    def reset_domain(self):
        """
        Copy domain into work domain
        """
        self.work_domain = list(self.domain)

    def domain_size(self):
        """
        Get size of work domain

        :return:    Size of work domain
        """
        return len(self.work_domain)

    def set_next_value(self):
        """
        Set variables value to next value from work domain
        """
        self.value = self.work_domain.pop()
