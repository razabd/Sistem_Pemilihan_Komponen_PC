from flask import Flask, render_template, request
from constraint import Problem
# ... [Your CSP code here]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# ... [Other routes and functions]

if __name__ == '__main__':
    app.run(debug=True)
