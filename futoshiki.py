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

    def purge(self, var):
        """
        Remove all values not meeting constraint from other variables domains

        :param var:     Variable to purge for

        :return:    If all domains are left with at least one value
        """
        valid_domains = True

        def predicate(x):
            return x != var.value

        for row_var in self.vars_:
            if row_var != var:
                row_var.push_state()
                row_var.filter_domain(predicate)
                if row_var.value is None and not row_var.domain_size():
                    valid_domains = False

        return valid_domains

    def reverse_purge(self, var):
        """
        Reverse states of variables changed with given variable purge

        :param var: Variable which purge will be reversed
        """
        for row_var in self.vars_:
            if row_var != var:
                row_var.pop_state()


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

    def purge(self, var):
        """
        Remove all values not meeting constraint from other variables domains

        :param var:     Variable to purge for

        :return:    If all domains are left with at least one value
        """
        valid_domains = True
        if var == self.var1:

            def predicate(x):
                return x > var.value

            self.var2.push_state()
            self.var2.filter_domain(predicate)
            if self.var2.value is None and not self.var2.domain_size():
                valid_domains = False
        else:

            def predicate(x):
                return x < var.value

            self.var1.push_state()
            self.var1.filter_domain(predicate)
            if self.var1.value is None and not self.var1.domain_size():
                valid_domains = False

        return valid_domains

    def reverse_purge(self, var):
        """
        Reverse states of variables changed with given variable purge

        :param var: Variable which purge will be reversed
        """
        if var == self.var1:
            self.var2.pop_state()
        else:
            self.var1.pop_state()
