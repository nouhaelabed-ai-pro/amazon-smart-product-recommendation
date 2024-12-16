# SmartProductRecommender

A sophisticated product recommendation system built with Python and Flask, leveraging TF-IDF and cosine similarity for intelligent product suggestions.

## 🌟 Features

- **Smart Search Engine**: Dynamic search functionality using TF-IDF vectorization
- **Intelligent Recommendations**: Product recommendations based on content similarity
- **Modern UI/UX**: Responsive design with intuitive user interface
- **Real-time Updates**: Instant search results and recommendations
- **Performance Optimized**: Efficient search algorithms and caching mechanisms

## 🚀 Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Machine Learning**: scikit-learn (TF-IDF, Cosine Similarity)
- **Natural Language Processing**: NLTK
- **Data Processing**: Pandas, NumPy
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome

## 📋 Prerequisites

- Python 3.12.6
- pip package manager
- Virtual environment (recommended)

## 📊 About Dataset

This dataset is having the data of 1K+ Amazon Product's Ratings and Reviews as per their details listed on the official website of Amazon

### Features

- **product_id** - Product ID
- **product_name** - Name of the Product
- **category** - Category of the Product
- **discounted_price** - Discounted Price of the Product
- **actual_price** - Actual Price of the Product
- **discount_percentage** - Percentage of Discount for the Product
- **rating** - Rating of the Product
- **rating_count** - Number of people who voted for the Amazon rating
- **about_product** - Description about the Product
- **user_id** - ID of the user who wrote review for the Product
- **user_name** - Name of the user who wrote review for the Product
- **review_id** - ID of the user review
- **review_title** - Short review
- **review_content** - Long review
- **img_link** - Image Link of the Product
- **product_link** - Official Website Link of the Product

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartProductRecommender.git
   cd SmartProductRecommender
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure data file is present:
   - Place the cleaned Amazon dataset in `data/cleaned_amazon_data.csv`

5. Run the application:
   ```bash
   python -m flask run
   ```

## 🎯 Usage

1. **Search Products**:
   - Enter keywords in the search bar
   - Results are ranked by relevance and popularity
   - Click on any product to see recommendations

2. **View Recommendations**:
   - Click "Get Similar Products" on any product card
   - View detailed product information and similarity scores
   - Browse through related products

3. **Explore Popular Products**:
   - Browse the homepage for top-rated products
   - Sort by ratings and popularity
   - Get instant recommendations

## 🔧 Project Structure

```
SmartProductRecommender/
├── app.py                 # Main Flask application
├── data/                  # Dataset directory
├── static/               
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
├── templates/            
│   └── index.html        # Main HTML template
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset provided by Amazon
- Inspired by modern e-commerce recommendation systems
- Built with love for a better shopping experience