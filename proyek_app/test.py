import json
from constraint import Problem

# Function to load data from a JSON file within the template directory
def load_data(file_name):
    file_path = f"proyek_app/{file_name}"
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load component data from JSON files
processors = load_data("processors.json")
motherboards = load_data("motherboards.json")
vga = load_data("vga.json")
psu = load_data("psu.json")

def pc_constraints(processor, motherboard, selected_vga, selected_psu, budget):
    # Motherboard harus sesuai dengan jenis processor
    if motherboards[motherboard]["processor_type"] != processors[processor]["processor_type"]:
        return False

    # Hitung total WATT dan pilih PSU yang memadai
    total_watt = processors[processor]["WATT"] + motherboards[motherboard]["WATT"] + vga[selected_vga]["WATT"]
    if total_watt > psu[selected_psu]["WATT"]:
        return False

    # Budget constraint
    total_cost = processors[processor]["price"] + motherboards[motherboard]["price"] + vga[selected_vga]["price"] + psu[selected_psu]["price"]
    if total_cost > budget:
        return False

    return True

def recommend_pc(preferences, budget):
    problem = Problem()

    # Filter components by grade
    filtered_processors = [p for p, specs in processors.items() if specs['Grade'] == preferences['processor_grade']]
    filtered_motherboards = [m for m, specs in motherboards.items() if specs['Grade'] == preferences['motherboard_grade']]
    filtered_vga = [v for v, specs in vga.items() if specs['Grade'] == preferences['vga_grade']]
    filtered_psu = [p for p, specs in psu.items() if specs['Grade'] == preferences['psu_grade']]

    # Add variables with filtered domains
    problem.addVariable("processor", filtered_processors)
    problem.addVariable("motherboard", filtered_motherboards)
    problem.addVariable("vga", filtered_vga)
    problem.addVariable("psu", filtered_psu)

    # Constraints
    problem.addConstraint(lambda p, m, v, ps: pc_constraints(p, m, v, ps, budget), ["processor", "motherboard", "vga", "psu"])

    # Solve the CSP problem
    solutions = problem.getSolutions()

    if solutions:
        # Select the first valid solution
        solution = solutions[0]

        # Calculate the total cost
        total_cost = processors[solution['processor']]['price'] + motherboards[solution['motherboard']]['price'] + vga[solution['vga']]['price'] + psu[solution['psu']]['price']

        # Add the total cost to the solution
        solution['total_cost'] = total_cost

        return solution
    else:
        return None  # No valid solution found

# Example usage
user_preferences = {
    "processor_grade": "low",
    "motherboard_grade": "medium",
    "vga_grade": "medium",
    "psu_grade": "low"
}
user_budget = 30000000

recommended_pc = recommend_pc(user_preferences, user_budget)

if recommended_pc:
    print("Recommended PC Components:")
    print(f"Processor: {recommended_pc['processor']} (Grade: {processors[recommended_pc['processor']]['Grade']})")
    print(f"Motherboard: {recommended_pc['motherboard']} (Grade: {motherboards[recommended_pc['motherboard']]['Grade']})")
    print(f"VGA: {recommended_pc['vga']} (Grade: {vga[recommended_pc['vga']]['Grade']})")
    print(f"PSU: {recommended_pc['psu']} (Grade: {psu[recommended_pc['psu']]['Grade']})")
    print(f"Total Cost: {recommended_pc['total_cost']}")
    print(f"Budget: {user_budget}")
else:
    print("No valid solution found within the budget.")