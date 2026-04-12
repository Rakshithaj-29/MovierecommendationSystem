import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

class MovieRecommender:
    def __init__(self, csv_path='movies .csv'):
        self.movies_df = pd.read_csv(csv_path)
        self.selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
        self._preprocess()

    def _preprocess(self):
        # Fill null values with empty strings
        for feature in self.selected_features:
            self.movies_df[feature] = self.movies_df[feature].fillna('')
        
        # Combine features into a single string for TF-IDF
        self.movies_df['combined_features'] = self.movies_df['genres'] + ' ' + \
                                             self.movies_df['keywords'] + ' ' + \
                                             self.movies_df['tagline'] + ' ' + \
                                             self.movies_df['cast'] + ' ' + \
                                             self.movies_df['director']
        
        # Initialize TF-IDF Vectorizer
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.feature_vectors = self.tfidf.fit_transform(self.movies_df['combined_features'])
        
        # Compute Similarity Matrix
        self.similarity = cosine_similarity(self.feature_vectors)

    def get_recommendations(self, movie_name, num_recommendations=10):
        # Find the closest match for the movie name
        list_of_all_titles = self.movies_df['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        
        if not find_close_match:
            return []
            
        close_match = find_close_match[0]
        
        # Find the index of the movie
        index_of_the_movie = self.movies_df[self.movies_df.title == close_match]['index'].values[0]
        
        # Get similarity scores
        similarity_score = list(enumerate(self.similarity[index_of_the_movie]))
        
        # Sort the movies based on similarity scores
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        
        # Get the recommended movie titles
        recommendations = []
        for i, movie in enumerate(sorted_similar_movies):
            if i == 0: continue # Skip the queried movie itself
            index = movie[0]
            title_from_index = self.movies_df[self.movies_df.index == index]['title'].values[0]
            recommendations.append(title_from_index)
            if len(recommendations) >= num_recommendations:
                break
                
        return recommendations

if __name__ == "__main__":
    recommender = MovieRecommender()
    print("Recommendations for 'Iron Man':")
    print(recommender.get_recommendations('Iron Man'))
