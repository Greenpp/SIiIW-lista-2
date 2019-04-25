from itertools import islice


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

        self.domain_size = int(self.vars_[0].domain_size)
        self.min_field = vars_[0].domain_size

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
        valid_domains = True

        if var is None:
            for i, row_var in enumerate(self.vars_):
                row_var.filter_domain(lambda x: x <= (self.domain_size - self.in_sight + i + 1))
                if row_var.domain_size == 0:
                    return False
        else:
            # Find index of the new var
            new_var_pos = self.vars_.index(var)
            if new_var_pos < self.min_field:
                # Check if the value will be covered
                max_height = 0
                for prev_var in islice(self.vars_, new_var_pos):
                    if prev_var.value is not None:
                        prev_val = prev_var.value
                    elif prev_var.domain_size > 0:
                        prev_val = min(prev_var.domain)
                    else:
                        prev_val = 0
                    if prev_val > max_height:
                        max_height = prev_val
                if max_height > var.value:
                    # Shift min highest value index if the value will be covered
                    if self.min_field < len(self.vars_):
                        domain_size = len(self.vars_)
                        self.vars_[self.min_field].push_state()
                        self.vars_[self.min_field].filter_domain(lambda x: x != domain_size)
                        if self.vars_[self.min_field].domain_size == 0:
                            valid_domains = False
                    self.min_field += 1

        return valid_domains

    def reverse_purge(self, var):
        """
        Reverse states of variables changed with given variable purge

        :param var: Variable which purge will be reversed
        """
        # Find index of the var
        new_var_pos = self.vars_.index(var)
        if new_var_pos < self.min_field:
            # Check if the value will be covered
            max_height = 0
            for prev_var in islice(self.vars_, new_var_pos):
                if prev_var.value is not None:
                    prev_val = prev_var.value
                elif prev_var.domain_size > 0:
                    prev_val = min(prev_var.domain)
                else:
                    prev_val = 0
                if prev_val > max_height:
                    max_height = prev_val
            if max_height > var.value:
                # Reverse shift and state if the value will be covered
                self.min_field -= 1
                if self.min_field < len(self.vars_):
                    self.vars_[self.min_field].pop_state()
