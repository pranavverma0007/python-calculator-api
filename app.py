from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Calculator API',
        'endpoints': {
            '/add': 'POST - {"a": 5, "b": 3}',
            '/subtract': 'POST - {"a": 10, "b": 4}',
            '/multiply': 'POST - {"a": 6, "b": 7}',
            '/divide': 'POST - {"a": 15, "b": 3}',
            '/health': 'GET - Check service status'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'calculator-api'})

@app.route('/add', methods=['POST'])
def add():
    try:
        data = request.get_json()
        a = data.get('a')
        b = data.get('b')
        
        if a is None or b is None:
            return jsonify({'error': 'Missing parameters a or b'}), 400
        
        result = a + b
        return jsonify({
            'operation': 'addition',
            'a': a,
            'b': b,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/subtract', methods=['POST'])
def subtract():
    try:
        data = request.get_json()
        a = data.get('a')
        b = data.get('b')
        
        if a is None or b is None:
            return jsonify({'error': 'Missing parameters a or b'}), 400
        
        result = a - b
        return jsonify({
            'operation': 'subtraction',
            'a': a,
            'b': b,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/multiply', methods=['POST'])
def multiply():
    try:
        data = request.get_json()
        a = data.get('a')
        b = data.get('b')
        
        if a is None or b is None:
            return jsonify({'error': 'Missing parameters a or b'}), 400
        
        result = a * b
        return jsonify({
            'operation': 'multiplication',
            'a': a,
            'b': b,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/divide', methods=['POST'])
def divide():
    try:
        data = request.get_json()
        a = data.get('a')
        b = data.get('b')
        
        if a is None or b is None:
            return jsonify({'error': 'Missing parameters a or b'}), 400
        
        if b == 0:
            return jsonify({'error': 'Division by zero is not allowed'}), 400
        
        result = a / b
        return jsonify({
            'operation': 'division',
            'a': a,
            'b': b,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
