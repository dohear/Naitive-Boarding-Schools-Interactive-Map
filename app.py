from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load school data from JSON
with open('static/output_with_geocoding.json', 'r') as f:
    school_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/school')
def get_schools():
    return jsonify(school_data)

if __name__ == '__main__':
    app.run(debug=True)
