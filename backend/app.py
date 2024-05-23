from flask import Flask, request, jsonify
from model import make_prediction
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
additional_features = {
    'feature1': 0,
    'feature2': 0,
    'feature3': 0,
    'feature4': 0,
    'feature5': 0,
    'feature6': 0,
    'feature7': 0,
    'feature8': 0,
    'feature9': 0
}



@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    # Get the prediction from the model
    prediction = make_prediction(text, additional_features)
    
    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
