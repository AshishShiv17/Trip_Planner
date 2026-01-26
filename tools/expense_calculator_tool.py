from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool


class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""

        @tool("estimate_total_hotel_cost")
        def estimate_total_hotel_cost(price_per_night: float, total_days: int) -> float:
            """
            Calculate total hotel cost.

            Args:
                price_per_night (float): Cost per night
                total_days (int): Total number of nights

            Returns:
                float: Total hotel cost
            """
            try:
                price = float(price_per_night)
                days = int(total_days)
                return self.calculator.multiply(price, days)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to estimate hotel cost "
                    f"(price_per_night={price_per_night}, total_days={total_days}): {e}"
                ) from e

        @tool("calculate_total_expense")
        def calculate_total_expense(costs: list[float]) -> float:
            """
            Calculate total expense of the trip.

            Args:
                costs (list[float]): List of individual costs

            Returns:
                float: Total trip cost
            """
            try:
                if not isinstance(costs, list):
                    raise ValueError("costs must be a list of floats")

                clean_costs = [float(c) for c in costs]
                return self.calculator.calculate_total(*clean_costs)

            except Exception as e:
                raise RuntimeError(
                    f"Failed to calculate total expense (costs={costs}): {e}"
                ) from e

        @tool("calculate_daily_expense_budget")
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """
            Calculate daily expense budget.

            Args:
                total_cost (float): Total trip cost
                days (int): Number of days

            Returns:
                float: Daily budget
            """
            try:
                total = float(total_cost)
                d = int(days)

                if d <= 0:
                    raise ValueError("days must be greater than zero")

                return self.calculator.calculate_daily_budget(total, d)

            except Exception as e:
                raise RuntimeError(
                    f"Failed to calculate daily budget "
                    f"(total_cost={total_cost}, days={days}): {e}"
                ) from e

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget,
        ]
