from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/schools', methods=['GET'])
def get_schools():
    with open('data/output_with_geocoding.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
