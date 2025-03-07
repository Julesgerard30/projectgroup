import random

# STEP 1: Initialize the Population
def initialize_population():
    """Initialize Spain's population with three socio-economic groups and their economic conditions."""
    total_population = 47_555_580  # Spain's population in 2023
    return {
        "rich": {"count": int(0.10 * total_population), "avg_income": 60_000, "avg_expenses": 45_000},
        "middle_class": {"count": int(0.60 * total_population), "avg_income": 30_000, "avg_expenses": 24_000},
        "poor": {"count": int(0.30 * total_population), "avg_income": 15_000, "avg_expenses": 13_500}
    }

# Function to display the economic state of the population
def display_population(population, month=0):
    """Display the current financial status of the population."""
    print(f"\n📅 Month {month}: Economic Status")
    for group, data in population.items():
        print(f"{group.replace('_', ' ').title()} - People: {data['count']:,} | Income: €{data['avg_income']:,} | Expenses: €{data['avg_expenses']:,}")

# STEP 2: Define Crises
crises = {
    "housing_crisis": {"income_factor": 1.0, "expense_factor": 1.3, "description": "Rapid increase in housing prices, making housing less affordable."},
    "high_unemployment": {"income_factor": 0.8, "expense_factor": 1.0, "description": "High unemployment rates, especially among the youth, reducing household incomes."},
    "high_inflation": {"income_factor": 1.0, "expense_factor": 1.2, "description": "General increase in prices, reducing purchasing power."},
}

# STEP 3: Define Policies
policies = {
    "austerity_measures": {"income_factor": 0.92, "expense_factor": 1.0, "description": "Reduction in public spending to control the budget deficit."},
    "economic_stimulus": {"income_factor": 1.12, "expense_factor": 1.05, "description": "Increase in public spending to stimulate economic growth."},
    "labor_market_reforms": {"income_factor": 1.05, "expense_factor": 1.0, "description": "Changes in labor laws to encourage hiring and reduce unemployment."},
    "housing_subsidies": {"income_factor": 1.0, "expense_factor": 0.95, "description": "Financial aid to make housing more affordable."},
    "do_nothing": {"income_factor": 1.0, "expense_factor": 1.0, "description": "No government intervention; the economy follows its natural course."},
}

# Function to apply a crisis
def apply_crisis(population):
    """Randomly selects and applies a crisis to the population."""
    crisis_name, crisis_effect = random.choice(list(crises.items()))
    print(f"\n📉 Crisis: {crisis_effect['description']}")

    for group, data in population.items():
        data["avg_income"] = int(data["avg_income"] * crisis_effect["income_factor"])
        data["avg_expenses"] = int(data["avg_expenses"] * crisis_effect["expense_factor"])

    return crisis_name

# Function to apply a policy with strict input validation using try-except
def apply_policy(population):
    """Allows the user to select a policy response to the crisis with error handling."""
    print("\n📊 Choose a policy to mitigate the crisis:")
    policy_list = list(policies.keys())

    for i, policy in enumerate(policy_list, 1):
        print(f"{i}. {policy.replace('_', ' ').title()} - {policies[policy]['description']}")

    while True:
        try:
            choice = int(input("Enter the number of your choice (1-5): ").strip())
            if 1 <= choice <= len(policy_list):
                return policy_list[choice - 1]
            else:
                print("⛔ Invalid selection. Please enter a number between 1 and 5.")
        except ValueError:
            print("⛔ Invalid input. Please enter a valid number.")

# Function to get a yes/no response with strict validation using try-except
def get_yes_no(prompt):
    """Ensures the user inputs only 'yes' or 'no'."""
    while True:
        try:
            response = input(prompt).strip().lower()
            if response in ["yes", "no"]:
                return response
            else:
                raise ValueError
        except ValueError:
            print("⛔ Invalid input. Please enter 'yes' or 'no'.")

# Function to simulate the economy over several months
def simulate_economy(population, months=6):
    """Simulates the economic impact of the crisis and policy over several months."""
    for month in range(1, months + 1):
        print(f"\n📅 Month {month}: Economy Adjusting...")
        for group, data in population.items():
            data["avg_income"] = int(data["avg_income"] * random.uniform(0.98, 1.03))
            data["avg_expenses"] = int(data["avg_expenses"] * random.uniform(0.97, 1.02))

        display_population(population, month)

# Function to evaluate the economic outcome
def evaluate_crisis_outcome(initial_population, final_population):
    """Evaluates if the economy improved, collapsed, or remained unstable."""
    outcome_data = {}
    total_income_change = sum(
        ((final_population[group]["avg_income"] - initial_population[group]["avg_income"]) / initial_population[group]["avg_income"]) * 100
        for group in initial_population
    ) / 3

    print("\n🔎 Economic Outcome:")
    if total_income_change > 5:
        final_state = "The economy has stabilized and improved."
    elif total_income_change < -5:
        final_state = "The economy has collapsed into a recession."
    else:
        final_state = "The economy remains unstable but has not collapsed."

    print(final_state)

    for group in initial_population:
        outcome_data[group] = {
            "income_change": ((final_population[group]["avg_income"] - initial_population[group]["avg_income"]) / initial_population[group]["avg_income"]) * 100,
            "expense_change": ((final_population[group]["avg_expenses"] - initial_population[group]["avg_expenses"]) / initial_population[group]["avg_expenses"]) * 100
        }

    return final_state, outcome_data

# Function to save the economic report
def save_report(history, filename="economic_report.txt"):
    """Logs every crisis, policy, and economic change in detail with performance analysis."""
    with open(filename, "w") as file:
        file.write("📜 ECONOMIC SIMULATION REPORT\n")
        file.write("=================================\n\n")

        total_months = 0

        for i, entry in enumerate(history, 1):
            total_months += 6
            file.write(f"🔄 Cycle {i}:\n")
            file.write(f"🌍 Crisis: {crises[entry['crisis']]['description']}\n")
            file.write(f"🏛️ Policy Applied: {policies[entry['policy']]['description']}\n")
            file.write(f"📆 Months Passed (Cumulative): {total_months}\n")
            file.write(f"📈 Outcome: {entry['final_state']}\n\n")

            file.write("📊 Economic Performance:\n")
            for group in entry["outcome"]:
                file.write(f"   - {group.replace('_', ' ').title()} → Income: {entry['outcome'][group]['income_change']:.2f}%, "
                           f"Expenses: {entry['outcome'][group]['expense_change']:.2f}%\n")

            # Ajout des conseils en fonction de la politique appliquée
            file.write("\n📢 SUGGESTIONS & IMPROVEMENTS:\n")
            if entry["policy"] == "austerity_measures":
                file.write("- Austerity reduced expenses but slowed economic recovery. **Economic Stimulus** could have helped create jobs faster.\n")
            elif entry["policy"] == "economic_stimulus":
                file.write("- Public spending increased incomes but also raised expenses. A combination with **Austerity Measures** may have controlled inflation better.\n")
            elif entry["policy"] == "labor_market_reforms":
                file.write("- Labor reforms improved employment but had little impact on inflation. **Targeted subsidies** could have balanced economic growth.\n")
            elif entry["policy"] == "housing_subsidies":
                file.write("- Housing subsidies eased the cost of living but didn't boost employment. **Investing in the labor market** could have been a better alternative.\n")
            elif entry["policy"] == "do_nothing":
                file.write("- No intervention led to worsening economic conditions. Future crises should be met with **proactive measures rather than inaction**.\n")

            file.write("\n")

        file.write("📢 FINAL ECONOMIC INSIGHTS:\n")
        file.write(f"- The simulation lasted a total of {total_months} months.\n")
        file.write("- **Alternative Strategies That Could Have Been Used:**\n")
        file.write("- In cases of **high unemployment**, **Economic Stimulus** or **Labor Market Reforms** would have been more effective than Austerity Measures.\n")
        file.write("- If facing **rising housing prices**, **Housing Subsidies** would have reduced the burden on lower and middle-income groups.\n")
        file.write("- **Doing nothing** was the worst option in most cases, as crises worsened without intervention.\n")
        file.write("- When inflation surged, a mix of **Austerity Measures** and **targeted subsidies** would have worked better than only reducing spending.\n")
        file.write("- Policies should have been **adapted based on economic trends**, rather than applying the same solution to every crisis.\n")

    print("\n💾 Economic report saved as 'economic_report.txt'.")

# Run the simulation
def run_simulation():
    """Runs the economic simulation with logging and enhanced reporting."""
    population = initialize_population()
    history = []

    while True:
        display_population(population)
        crisis = apply_crisis(population)
        policy = apply_policy(population)
        initial_population = {group: data.copy() for group, data in population.items()}
        simulate_economy(population, months=6)
        final_state, outcome = evaluate_crisis_outcome(initial_population, population)

        history.append({
            "crisis": crisis,
            "policy": policy,
            "months_passed": len(history) * 6,
            "final_state": final_state,
            "outcome": outcome
        })

        if get_yes_no("\nDo you want to continue with another crisis? (yes/no): ") == "no":
            save_report(history)
            print("\n🏁 Simulation ended.")
            break

run_simulation()