import random
import json

# STEP 1: Initialize the Population
def initialize_population():
    """Initialize the population with three social groups and their economic conditions."""
    return {
        "rich": {"count": 100, "avg_income": 8000, "avg_expenses": 5000},
        "middle_class": {"count": 500, "avg_income": 3000, "avg_expenses": 2500},
        "poor": {"count": 400, "avg_income": 1200, "avg_expenses": 1100}
    }

# Function to display the economic state of the population
def display_population(population, month=0):
    """Display the current financial status of the population."""
    print(f"\nMonth {month}: Economic Status")
    for group, data in population.items():
        print(f"{group.replace('_', ' ').title()} - People: {data['count']} | Income: {data['avg_income']} | Expenses: {data['avg_expenses']}")

# STEP 2: Define Crises
crises = {
    "inflation_surge": {"income_factor": 1.0, "expense_factor": 1.2, "description": "Rising inflation increases the cost of living."},
    "unemployment_wave": {"income_factor": 0.8, "expense_factor": 1.0, "description": "Unemployment rises, reducing overall wages."},
    "stock_market_crash": {"income_factor": 0.7, "expense_factor": 1.0, "target": "rich", "description": "Stock market collapses, affecting high-income individuals."},
    "housing_crisis": {"income_factor": 1.0, "expense_factor": 1.3, "description": "Housing costs increase sharply, raising rent prices."},
}

# STEP 3: Define Policies
policies = {
    "increase_taxes": {"income_factor": 0.92, "expense_factor": 1.0, "description": "Higher taxes reduce disposable income but improve government stability."},
    "stimulus_checks": {"income_factor": 1.12, "expense_factor": 1.05, "target": "poor", "description": "Direct financial aid is given to low-income individuals, boosting spending."},
    "reduce_interest_rates": {"income_factor": 1.08, "expense_factor": 1.07, "target": "middle_class", "description": "Lower interest rates stimulate spending and job creation."},
    "economic_investment": {"income_factor": 1.3, "expense_factor": 1.1, "description": "Government invests in industries, significantly boosting income and job growth."},
    "do_nothing": {"income_factor": 1.0, "expense_factor": 1.0, "description": "No intervention. The economy evolves naturally."},
}

# Function to apply a crisis
def apply_crisis(population):
    """Randomly selects and applies a crisis to the population."""
    crisis_name, crisis_effect = random.choice(list(crises.items()))
    print(f"\n Crisis: {crisis_effect['description']}")

    for group, data in population.items():
        if "target" in crisis_effect and crisis_effect["target"] != group:
            continue

        data["avg_income"] = int(data["avg_income"] * crisis_effect["income_factor"])
        data["avg_expenses"] = int(data["avg_expenses"] * crisis_effect["expense_factor"])

    return crisis_name

# Function to apply a policy
def apply_policy(population):
    """Allows the user to select a policy response to the crisis."""
    print("\n Choose a policy to mitigate the crisis:")
    policy_list = list(policies.keys())

    for i, policy in enumerate(policy_list, 1):
        print(f"{i}. {policy.replace('_', ' ').title()} - {policies[policy]['description']}")

    while True:
        choice = input("Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(policy_list):
            chosen_policy = policy_list[int(choice) - 1]
            policy_effect = policies[chosen_policy]
            print(f"\n Policy Applied: {policy_effect['description']}")

            for group, data in population.items():
                if "target" in policy_effect and policy_effect["target"] != group:
                    continue

                data["avg_income"] = int(data["avg_income"] * policy_effect["income_factor"])
                data["avg_expenses"] = int(data["avg_expenses"] * policy_effect["expense_factor"])

            return chosen_policy
        else:
            print("Invalid selection. Please enter a number from the list.")

# Function to simulate economy over time
def simulate_economy(population, months):
    """Simulates the economic impact of the crisis and policy over several months."""
    initial_population = {group: data.copy() for group, data in population.items()}

    for month in range(1, months + 1):
        print(f"\n Month {month}: Economy Adjusting...")
        for group, data in population.items():
            data["avg_income"] = int(data["avg_income"] * random.uniform(0.98, 1.03))
            data["avg_expenses"] = int(data["avg_expenses"] * random.uniform(0.97, 1.02))

        display_population(population, month)

    return initial_population

# Function to evaluate crisis outcome
def evaluate_crisis_outcome(initial_population, final_population):
    """Determines whether the economy improved, collapsed, or remained unstable."""
    total_income_change = sum(((final_population[group]["avg_income"] - initial_population[group]["avg_income"]) / initial_population[group]["avg_income"]) * 100 for group in initial_population) / 3

    print("\n Economic Outcome:")
    if total_income_change > 5:
        print("✔ The economy successfully stabilized and improved.")
        return "Stabilized and improved."
    elif total_income_change < -5:
        print(" The economy collapsed into a major recession.")
        return "Collapsed into a recession."
    else:
        print("⚠ The economy remains unstable but has not collapsed.")
        return "Remains unstable but did not collapse."

# Save Report at the End of the Simulation
def save_report(history, filename="economic_report.txt"):
    """Saves a detailed report of all crises, policies, and their long-term effects."""
    with open(filename, "w") as file:
        file.write("ECONOMIC SIMULATION REPORT\n")
        file.write("===========================\n\n")

        for i, entry in enumerate(history, 1):
            file.write(f"Decision {i}:\n")
            file.write(f"Crisis: {entry['crisis_description']}\n")
            file.write(f"Policy Chosen: {entry['policy_description']}\n")
            file.write(f"Months Passed: {entry['months_passed']}\n")
            file.write(f"Outcome: {entry['outcome']}\n\n")

            file.write("Economic Impact:\n")
            for group in entry["initial_population"]:
                income_change = ((entry["final_population"][group]["avg_income"] - entry["initial_population"][group]["avg_income"]) / entry["initial_population"][group]["avg_income"]) * 100
                expense_change = ((entry["final_population"][group]["avg_expenses"] - entry["initial_population"][group]["avg_expenses"]) / entry["initial_population"][group]["avg_expenses"]) * 100

                file.write(f"{group.replace('_', ' ').title()} Income Change: {income_change:.2f}% | Expense Change: {expense_change:.2f}%\n")

            file.write("\n")

    print("\n Economic report saved to economic_report.txt")

# Main Simulation
def run_simulation():
    """Runs the economic simulation with multiple crisis cycles."""
    population = initialize_population()
    history = []

    while True:
        display_population(population)

        crisis = apply_crisis(population)
        policy = apply_policy(population)
        initial_population = simulate_economy(population, months=6)
        outcome = evaluate_crisis_outcome(initial_population, population)

        history.append({
            "crisis_description": crises[crisis]["description"],
            "policy_description": policies[policy]["description"],
            "months_passed": len(history) * 6,
            "initial_population": initial_population,
            "final_population": {group: data.copy() for group, data in population.items()},
            "outcome": outcome
        })

        if input("\nDo you want to continue with another crisis? (yes/no): ").strip().lower() == "no":
            save_report(history)
            print("\nSimulation ended.")
            break

run_simulation() 