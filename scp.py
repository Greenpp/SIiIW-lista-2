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

    def load_data(self, file_path, type_):
        """
        Load data from file

        :param file_path:   Path to data file
        :param type_:       Type of problem:
                                        futo    - Futoshiki
                                        sky     - Skyscrapper

        :return:    If data was loaded successfully
        """
        with open(file_path) as f:
            if type_ == 'futo':
                n = int(f.readline())  # Read the size

                f.readline()  # Skip 'START:'
                for i in range(n):
                    row = f.readline().rstrip()
                    # TODO parse row

                f.readline()  # Skip 'REL:'
                for line in f:
                    # TODO parse constraints + strip
                    pass
            elif type_ == 'sky':
                n = int(f.readline())  # Read the size

                for line in f:
                    # TODO parse constraints + strip
                    pass
            else:
                print('Wrong file type')
                return False

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
