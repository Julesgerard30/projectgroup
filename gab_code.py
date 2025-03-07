import random

# STEP 1: Initialize the Population
def initialize_population():
    """Initialize the population with three social groups based on Spain's data (adjusted for accuracy)."""
    return {
        "high_income": {"count": 4_700_000, "avg_income": 60000, "avg_expenses": 45000},
        "middle_income": {"count": 19_000_000, "avg_income": 30000, "avg_expenses": 24000},
        "low_income": {"count": 23_300_000, "avg_income": 15000, "avg_expenses": 13500}
    }

# Function to display the economic state of the population
def display_population(population, month=0):
    """Display the current financial status of the population."""
    print(f"\nMonth {month}: Economic Status")
    for group, data in population.items():
        print(f"{group.replace('_', ' ').title()} - People: {data['count']:,} | Income: €{data['avg_income']:,} | Expenses: €{data['avg_expenses']:,}")

# STEP 2: Define Crises
crises = {
    "2008_financial_crisis": {"income_factor": 0.85, "expense_factor": 1.1},
    "european_debt_crisis": {"income_factor": 0.9, "expense_factor": 1.05},
    "covid_19_pandemic": {"income_factor": 0.8, "expense_factor": 1.2},
    "housing_crisis": {"income_factor": 0.95, "expense_factor": 1.15},
}

# STEP 3: Define Policies
policies = {
    "austerity_measures": {"income_factor": 0.9, "expense_factor": 1.0},
    "economic_stimulus": {"income_factor": 1.1, "expense_factor": 1.05},
    "labor_market_reforms": {"income_factor": 1.05, "expense_factor": 1.0},
    "housing_subsidies": {"income_factor": 1.0, "expense_factor": 0.95},
    "do_nothing": {"income_factor": 1.0, "expense_factor": 1.0},
}

# Function to apply a crisis
def apply_crisis(population):
    """Randomly selects and applies a crisis to the population."""
    crisis_name, crisis_effect = random.choice(list(crises.items()))
    print(f"\nCrisis: {crisis_name.replace('_', ' ').title()}")

    for group, data in population.items():
        data["avg_income"] = int(data["avg_income"] * crisis_effect["income_factor"])
        data["avg_expenses"] = int(data["avg_expenses"] * crisis_effect["expense_factor"])

    return crisis_name

# Function to apply a policy
def apply_policy(population):
    """Allows the user to select a policy response to the crisis."""
    print("\nChoose a policy to mitigate the crisis:")
    policy_list = list(policies.keys())

    for i, policy in enumerate(policy_list, 1):
        print(f"{i}. {policy.replace('_', ' ').title()}")

    while True:
        choice = input("Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(policy_list):
            chosen_policy = policy_list[int(choice) - 1]
            policy_effect = policies[chosen_policy]

            for group, data in population.items():
                data["avg_income"] = int(data["avg_income"] * policy_effect["income_factor"])
                data["avg_expenses"] = int(data["avg_expenses"] * policy_effect["expense_factor"])

            return chosen_policy
        else:
            print("Invalid selection. Please enter a number from the list.")

# Function to simulate economy over time
def simulate_economy(population, months=6):
    """Simulates the economic impact of a crisis and policy over time."""
    for month in range(1, months + 1):
        for group, data in population.items():
            data["avg_income"] = int(data["avg_income"] * random.uniform(0.98, 1.03))
            data["avg_expenses"] = int(data["avg_expenses"] * random.uniform(0.97, 1.02))

        display_population(population, month)

# Evaluate economic impact
def evaluate_crisis_outcome(initial_population, population):
    """Compares pre-crisis and post-crisis economic conditions."""
    outcomes = {}
    for group in initial_population:
        income_change = population[group]["avg_income"] - initial_population[group]["avg_income"]
        expense_change = population[group]["avg_expenses"] - initial_population[group]["avg_expenses"]
        outcomes[group] = {"income_change": income_change, "expense_change": expense_change}
    return outcomes

# Main Simulation
def run_simulation():
    """Runs the economic simulation with multiple crisis cycles."""
    population = initialize_population()
    history = []

    while True:
        display_population(population)
        crisis = apply_crisis(population)
        policy = apply_policy(population)
        initial_population = {group: data.copy() for group, data in population.items()}
        simulate_economy(population, months=6)
        outcome = evaluate_crisis_outcome(initial_population, population)

        history.append({
            "crisis": crisis,
            "policy": policy,
            "outcome": outcome,
        })

        if input("\nDo you want to continue with another crisis? (yes/no): ").strip().lower() == "no":
            print("\nSimulation ended.")
            break

run_simulation()