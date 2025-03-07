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
def display_population(population):
    """Display the current financial status of the population."""
    print("\nCurrent Population Status:")
    for group, data in population.items():
        print(
            f"{group.replace('_', ' ').title()} - People: {data['count']} | Income: {data['avg_income']}€ | Expenses: {data['avg_expenses']}€")


# STEP 2: Define Crises
crises = {
    "inflation_surge": {"income_factor": 1.0, "expense_factor": 1.2,
                        "description": "Rising inflation increases the cost of living."},
    "unemployment_wave": {"income_factor": 0.8, "expense_factor": 1.0,
                          "description": "Unemployment rises, reducing overall wages."},
    "stock_market_crash": {"income_factor": 0.7, "expense_factor": 1.0, "target": "rich",
                           "description": "Stock market collapses, affecting high-income individuals."},
    "housing_crisis": {"income_factor": 1.0, "expense_factor": 1.3,
                       "description": "Housing costs increase sharply, raising rent prices."},
}


# Function to apply a crisis
def apply_crisis(population):
    """Randomly selects and applies a crisis to the population."""
    crisis_name, crisis_effect = random.choice(list(crises.items()))
    print(f"\nCrisis: {crisis_effect['description']}")

    for group, data in population.items():
        if "target" in crisis_effect and crisis_effect["target"] != group:
            continue  # Skip if the crisis only affects a specific group

        data["avg_income"] = int(data["avg_income"] * crisis_effect["income_factor"])
        data["avg_expenses"] = int(data["avg_expenses"] * crisis_effect["expense_factor"])

    display_population(population)
    return crisis_name, crisis_effect


# STEP 3: Define Policies
policies = {
    "increase_taxes": {"income_factor": 0.9, "expense_factor": 1.0,
                       "description": "Higher taxes reduce disposable income."},
    "stimulus_checks": {"income_factor": 1.1, "expense_factor": 1.2, "target": "poor",
                        "description": "Direct financial aid is given to low-income individuals."},
    "reduce_interest_rates": {"income_factor": 1.05, "expense_factor": 1.1, "target": "middle_class",
                              "description": "Lower interest rates stimulate middle-class spending but raise inflation."},
    "do_nothing": {"income_factor": 1.0, "expense_factor": 1.0,
                   "description": "No intervention. The economy evolves naturally."},
}


# Function to apply a government policy
def apply_policy(population):
    """Allows the user to select and apply a policy response to the crisis."""
    print("\nSelect a policy to mitigate the crisis:")
    policy_list = list(policies.keys())

    for i, policy in enumerate(policy_list, 1):
        print(f"{i}. {policy.replace('_', ' ').title()} - {policies[policy]['description']}")

    while True:
        choice = input("Enter the number of your choice: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(policy_list):
            chosen_policy = policy_list[int(choice) - 1]
            policy_effect = policies[chosen_policy]
            print(f"\nPolicy Applied: {policy_effect['description']}")

            for group, data in population.items():
                if "target" in policy_effect and policy_effect["target"] != group:
                    continue

                data["avg_income"] = int(data["avg_income"] * policy_effect["income_factor"])
                data["avg_expenses"] = int(data["avg_expenses"] * policy_effect["expense_factor"])

            display_population(population)
            return chosen_policy, policy_effect
        else:
            print("Invalid selection. Please enter a number from the list.")


# STEP 4: Save and Load Data with a Report
def save_population(population, history, filename="economic_report.txt"):
    """Save a detailed economic report instead of raw data."""
    with open(filename, "w") as file:
        file.write("ECONOMIC SIMULATION REPORT\n")
        file.write("===========================\n\n")
        file.write("Final Economic Conditions:\n")

        for group, data in population.items():
            file.write(
                f"{group.replace('_', ' ').title()} - People: {data['count']} | Income: {data['avg_income']}€ | Expenses: {data['avg_expenses']}€\n")

        file.write("\nCrisis and Policy History:\n")
        for crisis, policy in history:
            file.write(f"- Crisis: {crises[crisis]['description']}, Response: {policies[policy]['description']}\n")

        file.write("\nOverall Economic Performance:\n")
        improvement = sum(data["avg_income"] - data["avg_expenses"] for data in population.values())
        if improvement > 0:
            file.write(f"The economy improved. Net wealth change: +{improvement}€\n")
        else:
            file.write(f"The economy worsened. Net wealth change: {improvement}€\n")

    print("Economic report saved to economic_report.txt")


def load_population(filename="population_data.json"):
    """Load population data from a file, if available."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No saved data found. Initializing a new population.")
        return initialize_population()


# STEP 5: Main Simulation Loop with Proper Yes/No Input Validation
def run_simulation():
    """Runs the full economic simulation in a loop with proper input validation."""
    population = load_population()
    history = []

    while True:
        print("\nNew Economic Cycle")
        display_population(population)

        crisis, crisis_effect = apply_crisis(population)
        policy, policy_effect = apply_policy(population)
        history.append((crisis, policy))

        # Ensure valid input for continuing the simulation
        while True:
            choice = input("\nContinue simulation? (yes/no): ").strip().lower()
            if choice in ["yes", "no"]:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if choice == "no":
            save_population(population, history)
            print("\nSimulation ended.")
            break


# Run the simulation
run_simulation()