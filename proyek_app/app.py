from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="template")

@app.route("/")
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='localhost', port=8801, debug=True)
