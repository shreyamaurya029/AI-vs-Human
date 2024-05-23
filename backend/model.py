from flask import jsonify
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import nltk

# Ensure nltk resources are downloaded
nltk.download('punkt')

def preprocess_text(text, max_len=1354, max_features=10000):
    # Tokenize text
    tokens = nltk.word_tokenize(text)
    
    # Create and fit the tokenizer
    tokenizer = Tokenizer(num_words=max_features)
    tokenizer.fit_on_texts([text])
    
    # Convert text to integer sequence and pad it
    sequence = tokenizer.texts_to_sequences([tokens])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)
    
    return padded_sequence[0]  # Return the sequence itself, not as a list

def preprocess_additional_features(features):
    # Example preprocessing for additional features
    # Assuming additional features are numerical and in a dictionary format
    additional_input = np.array([features['feature1'], features['feature2'], features['feature3'], features['feature4'],
                                 features['feature5'], features['feature6'], features['feature7'], features['feature8'],
                                 features['feature9']])
    return additional_input

model_path = 'classification_model2.h5'

def make_prediction(text, additional_features=None):
    if text is None:
        return jsonify({'error': 'Missing text input'}), 400
    if additional_features is None or len(additional_features) != 9:
        return jsonify({'error': 'Missing or incorrect additional features'}), 400
    
    # load the model with a asyc call
    try:
        loaded_model = keras.models.load_model(model_path)
    except:
        return jsonify({'error': 'Model not found'}), 500
    # Preprocess text and additional features
    preprocessed_text = preprocess_text(text)
    preprocessed_features = preprocess_additional_features(additional_features)
    
    # Expand dimensions if necessary for batch input
    preprocessed_text = np.expand_dims(preprocessed_text, axis=0)
    preprocessed_features = np.expand_dims(preprocessed_features, axis=0)
    
    # Combine inputs
    prediction = loaded_model.predict([preprocessed_text, preprocessed_features])
    # print(prediction[0])
    # predicted_class = np.argmax(prediction[0])
    return prediction[0][0]

# Example usage
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
# print(make_prediction("I love this product What about you I love you darling", additional_features))
