from flask import Flask, render_template, request, jsonify
from recommender import MovieRecommender
import os

app = Flask(__name__)

# Initialize the logic once at startup
print("Loading recommendation engine...")
try:
    recommender = MovieRecommender('movies .csv')
except Exception as e:
    print(f"Error initializing recommender: {e}")
    recommender = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form.get('movie_name')
    if not movie_name:
        return jsonify({'error': 'Please enter a movie name'}), 400
    
    if not recommender:
        return jsonify({'error': 'Recommendation engine not ready'}), 500
        
    try:
        # Call the function defined in the recommender class
        recommendations = recommender.get_recommendations(movie_name)
        if not recommendations: # Handle "Movie not found" or no matches case
            return jsonify({'error': 'Movie not found in our database. Try another one!'}), 404
            
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
