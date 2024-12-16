from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from flask_caching import Cache
from functools import lru_cache
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure Flask-Caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Global variables for TF-IDF and similarity matrix
df = None
tfidf_matrix = None
similarity_matrix = None
tfidf_vectorizer = None

@lru_cache(maxsize=1000)
def preprocess_text(text):
    if isinstance(text, str):
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        try:
            # Tokenization
            tokens = word_tokenize(text)
            
            # Remove stopwords and lemmatize
            stop_words = set(stopwords.words('english'))
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
            
            return ' '.join(tokens)
        except Exception as e:
            logger.error(f"Error in text preprocessing: {str(e)}")
            return text
    return ''

def initialize_recommendation_system():
    global df, tfidf_matrix, similarity_matrix, tfidf_vectorizer
    
    try:
        logger.info("Loading dataset...")
        df = pd.read_csv('data/cleaned_amazon_data.csv')
        
        logger.info("Cleaning text data...")
        df = clean_text_data(df)
        
        logger.info("Creating TF-IDF matrix...")
        tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_features'])
        
        logger.info("Calculating similarity matrix...")
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        logger.info("Recommendation system initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing recommendation system: {str(e)}")
        return False

def clean_text_data(df):
    logger.info("Starting text data cleaning")
    start_time = datetime.now()
    
    try:
        df['clean_name'] = df['product_name'].apply(preprocess_text)
        df['clean_about'] = df['about_product'].fillna('').apply(preprocess_text)
        df['clean_category'] = df['category'].apply(preprocess_text)
        df['combined_features'] = df['clean_name'] + ' ' + df['clean_about'] + ' ' + df['clean_category']
        
        logger.info(f"Text data cleaning completed in {datetime.now() - start_time}")
        return df
    except Exception as e:
        logger.error(f"Error in clean_text_data: {str(e)}")
        raise

def get_recommendations(idx, n=5):
    try:
        sim_scores = list(enumerate(similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        product_indices = [i[0] for i in sim_scores]
        
        recommendations = pd.DataFrame({
            'Product Name': df['product_name'].iloc[product_indices],
            'Category': df['category'].iloc[product_indices].apply(lambda x: x.split('|')[0]),
            'Price': df['discounted_price'].iloc[product_indices],
            'Rating': df['rating'].iloc[product_indices],
            'Similarity Score': [i[1] for i in sim_scores]
        })
        return recommendations
    except Exception as e:
        logger.error(f"Error in get_recommendations: {str(e)}")
        raise

def search_by_tag(query, n=10):
    try:
        # Preprocess the search query
        processed_query = preprocess_text(query)
        
        # Transform the query using the fitted vectorizer
        query_vector = tfidf_vectorizer.transform([processed_query])
        
        # Calculate similarity with all products
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Get top N similar products
        top_indices = similarities.argsort()[-n:][::-1]
        
        results = df.iloc[top_indices][['product_id', 'product_name', 'category', 'discounted_price', 'rating', 'rating_count']]
        return results
    except Exception as e:
        logger.error(f"Error in search_by_tag: {str(e)}")
        raise

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/recommendations')
def recommendations():
    try:
        # Get featured products (e.g., top-rated products)
        featured_products = df.nlargest(6, 'rating')[['product_id', 'product_name', 'category', 'discounted_price', 'rating']]
        return render_template('recommendations.html', featured_products=featured_products.to_dict('records'))
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return render_template('error.html', error="Unable to load featured products"), 500


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/search')
def search():
    try:
        query = request.args.get('query', '')
        if query:
            results = search_by_tag(query)
            return jsonify(results.to_dict('records'))
        return jsonify([])
    except Exception as e:
        logger.error(f"Error in search route: {str(e)}")
        return jsonify({'error': 'An error occurred during search'}), 500

@app.route('/api/similar-products/<product_id>')
@cache.memoize(timeout=300)  # Cache for 5 minutes
def get_similar_products(product_id):
    try:
        # Find the index of the product
        idx = df[df['product_id'] == product_id].index[0]
        # Get recommendations
        recommendations = get_recommendations(idx)
        return jsonify(recommendations.to_dict('records'))
    except Exception as e:
        logger.error(f"Error in get_similar_products: {str(e)}")
        return jsonify({'error': str(e)}), 400

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

# Initialize the recommendation system when the app starts
if __name__ == '__main__':
    if initialize_recommendation_system():
        app.run(debug=True)
    else:
        logger.error("Failed to initialize recommendation system. Application not started.")