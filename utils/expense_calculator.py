class Calculator:
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """
        Multiply two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of a and b
        """
        try:
            return float(a) * float(b)
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Invalid inputs for multiply: a={a}, b={b}") from e

    @staticmethod
    def calculate_total(*x: float) -> float:
        """
        Calculate sum of the given list of numbers.

        Args:
            x (list): List of floating numbers

        Returns:
            float: The sum of numbers in the list x
        """
        try:
            values = [float(v) for v in x]
            return sum(values)
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Invalid inputs for calculate_total: x={x}") from e

    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """
        Calculate daily budget.

        Args:
            total (float): Total cost.
            days (int): Total number of days

        Returns:
            float: Expense for a single day
        """
        try:
            total = float(total)
            days = int(days)

            if days <= 0:
                raise ValueError("Days must be greater than zero")

            return total / days

        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Invalid inputs for calculate_daily_budget: total={total}, days={days}"
            ) from e
