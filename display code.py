import sys

class FinancialAccount:
    """Represents an individual investment account."""
    
    def __init__(self, name: str, initial_balance: float, monthly_contribution: float, annual_return: float):
        self.name = name
        self.balance = initial_balance
        self.monthly_contribution = monthly_contribution
        self.annual_return = annual_return
        self.total_contributed = initial_balance

    def apply_monthly_growth(self):
        """Applies one month of compound interest and adds the monthly contribution."""
        # Convert annual return percentage to a decimal monthly rate
        monthly_rate = (self.annual_return / 100) / 12
        
        # New Balance = Previous Balance * (1 + Monthly Rate) + Monthly Contribution
        self.balance = self.balance * (1 + monthly_rate) + self.monthly_contribution
        self.total_contributed += self.monthly_contribution

def calculate_wealth_projection(accounts: list, target_goal: float, max_years: int = 50):
    """
    Projects the timeline to reach a combined financial target goal.
    Returns the years to reach the goal and the finalized account states.
    """
    months = 0
    max_months = max_years * 12

    # Check if the initial balance already meets the goal
    total_balance = sum(acc.balance for acc in accounts)
    if total_balance >= target_goal:
        return 0.0, accounts

    # Run the monthly projection loop
    while total_balance < target_goal and months < max_months:
        total_balance = 0
        for acc in accounts:
            acc.apply_monthly_growth()
            total_balance += acc.balance
        months += 1

    years_to_goal = months / 12
    return years_to_goal, accounts

def display_professional_dashboard():
    """Formats and prints a professional terminal display of the financial projection."""
    
    # 1. Define the Initial Data State
    target_goal = 1000000.00
    portfolio = [
        FinancialAccount("TFSA", initial_balance=20000, monthly_contribution=500, annual_return=7.0),
        FinancialAccount("RRSP", initial_balance=20000, monthly_contribution=500, annual_return=6.5),
        FinancialAccount("Non-Registered", initial_balance=10000, monthly_contribution=200, annual_return=5.0)
    ]

    # 2. Run the Calculation
    years, final_portfolio = calculate_wealth_projection(portfolio, target_goal)
    
    # 3. Format the Output
    print("\n" + "="*70)
    print(" STRATEGIC WEALTH PROJECTION DASHBOARD ".center(70, "="))
    print("="*70)
    
    print(f" Global Target Goal:           ${target_goal:,.2f}")
    
    if years >= 50:
        print(f" Projected Timeline:           50+ Years (Capped)")
    else:
        print(f