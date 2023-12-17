from flask import Flask, request, render_template
import json
from constraint import Problem

app = Flask(__name__)

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
    if motherboards[motherboard]["processor_type"] != processors[processor]["processor_type"]:
        return False
    total_watt = processors[processor]["WATT"] + motherboards[motherboard]["WATT"] + vga[selected_vga]["WATT"]
    if total_watt > psu[selected_psu]["WATT"]:
        return False
    total_cost = processors[processor]["price"] + motherboards[motherboard]["price"] + vga[selected_vga]["price"] + psu[selected_psu]["price"]
    if total_cost > budget:
        return False
    return True

def recommend_pc(preferences, budget):
    problem = Problem()
    filtered_processors = [p for p, specs in processors.items() if specs['Grade'] == preferences['processor_grade']]
    filtered_motherboards = [m for m, specs in motherboards.items() if specs['Grade'] == preferences['motherboard_grade']]
    filtered_vga = [v for v, specs in vga.items() if specs['Grade'] == preferences['vga_grade']]
    filtered_psu = [p for p, specs in psu.items() if specs['Grade'] == preferences['psu_grade']]
    problem.addVariable("processor", filtered_processors)
    problem.addVariable("motherboard", filtered_motherboards)
    problem.addVariable("vga", filtered_vga)
    problem.addVariable("psu", filtered_psu)
    problem.addConstraint(lambda p, m, v, ps: pc_constraints(p, m, v, ps, budget), ["processor", "motherboard", "vga", "psu"])
    solutions = problem.getSolutions()
    if solutions:
        solution = solutions[0]
        total_cost = processors[solution['processor']]['price'] + motherboards[solution['motherboard']]['price'] + vga[solution['vga']]['price'] + psu[solution['psu']]['price']
        solution['total_cost'] = total_cost
        return solution
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_preferences = {
        "processor_grade": request.form.get('processor_grade'),
        "motherboard_grade": request.form.get('motherboard_grade'),
        "vga_grade": request.form.get('vga_grade'),
        "psu_grade": request.form.get('psu_grade')
    }
    user_budget = int(request.form.get('budget'))
    recommended_pc = recommend_pc(user_preferences, user_budget)
    if recommended_pc:
        return render_template('result.html', result=recommended_pc, budget=user_budget)
    else:
        return render_template('result.html', result=None, budget=user_budget)

if __name__ == '__main__':
    app.run(debug=True)