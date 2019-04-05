class FutoshikiRowConstraint:
    """
    Constraint of row integrity in futoshiki
    """

    def __init__(self, vars_):
        """
        Create row constraint where every value must be unique

        :param vars_:   Variables in row
        """
        self.vars_ = vars_

    def check(self):
        """
        Check if constraint is meet

        :return: If constraint is meet
        """
        # Filter out Nones
        set_values = [v.value for v in self.vars_ if v.value is not None]

        return len(set_values) == len(set(set_values))

    def purge(self, var, pop=False):
        """
        Remove current variable value from all work domains in row

        :param var: Variable to get value from
        :param pop: If variables states should be popped from state stack
        """

        def predicate(x):
            return x != var.value

        for row_var in self.vars_:
            if row_var != var:
                if pop:
                    row_var.pop_state()
                row_var.filter_domain(predicate)


class FutoshikiRelationConstraint:
    """
    Constraint of relation in futoshiki
    """

    def __init__(self, var1, var2):
        """
        Create relation constraint with 2 variables, where v1 < v2

        :param var1:    First variable
        :param var2:    Second variable
        """
        self.var1 = var1
        self.var2 = var2

    def check(self):
        """
        Check if constraint is meet

        :return:    If constraint is meet
        """
        if self.var1.value is None or self.var2.value is None:
            return True

        return self.var1.value < self.var2.value

    def purge(self, var, pop=False):
        """
        Remove all values not meeting constraint from other variables working domain

        :param var:  Variable to leave unchanged
        :param pop: If variables states should be popped from state stack
        """
        if var == self.var1:
            if pop:
                self.var2.pop_state()

            def predicate(x):
                return x > var.value

            self.var2.filter_domain(predicate)
        else:
            if pop:
                self.var1.pop_state()

            def predicate(x):
                return x < var.value

            self.var1.filter_domain(predicate)
