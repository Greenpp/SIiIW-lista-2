class SkyscrapperRowConstraint:
    """
    Constraint of unique values in skyscrapper row
    """

    def __init__(self, vars_):
        """
        Create row constraint where every value must be unique

        :param vars_:    Variables in row
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
            if row_var != var and row_var.value is None:
                row_var.push_state()
                row_var.filter_domain(predicate)
                if row_var.value is None and not row_var.domain_size:
                    valid_domains = False

        return valid_domains

    def reverse_purge(self, var):
        """
        Reverse states of variables changed with given variable purge

        :param var: Variable which purge will be reversed
        """
        for row_var in self.vars_:
            if row_var != var and row_var.value is None:
                row_var.pop_state()


class SkyscrapperVisibilityConstraint:
    """
    Constraint of visibility in skyscrapper row
    """

    def __init__(self, vars_, in_sight):
        """
        Create row constraint where <in_sight> buildings must be visible from left

        :param vars_:   Variables in row
        :param in_sight:    Number of required visible buildings from left
        """
        self.vars_ = vars_
        self.in_sight = int(in_sight)

    def check(self):
        """
        Check if constraint is meet

        :return:    If constraint is meet
        """
        heights = [v.value for v in self.vars_]
        if None in heights:
            return True

        max_height = 0
        visible = 0
        for height in heights:
            if height > max_height:
                visible += 1
                max_height = height
                if visible > self.in_sight:
                    return False

        return visible == self.in_sight

    def purge(self, var):
        """
        Remove all values not meeting constraint from other variables domains

        :param var:     Variable to purge for

        :return:    If all domains are left with at least one value
        """
        # TODO
        pass

    def reverse_purge(self, var):
        """
        Reverse states of variables changed with given variable purge

        :param var: Variable which purge will be reversed
        """
        for row_var in self.vars_:
            if row_var != var and row_var.value is None:
                row_var.pop_state()
