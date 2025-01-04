import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.boolean_model import BooleanModel
from models.extended_boolean import ExtendedBooleanModel
from models.vector_model import VectorModel


app = Flask(__name__)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database", "faq.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), nullable=False)  # 'en' for English, 'ar' for Arabic

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    model = request.json.get('model', 'boolean')  # Default to boolean model
    language = request.json.get('language', 'en')  # Default to English

    # Fetch documents for the selected language
    filtered_documents = [
        {'id': faq.id, 'text': faq.question + " " + faq.answer}
        for faq in FAQ.query.filter_by(language=language).all()
    ]

    # Initialize models with the filtered documents
    boolean_model = BooleanModel(filtered_documents)
    extended_boolean_model = ExtendedBooleanModel(filtered_documents)
    vector_model = VectorModel(filtered_documents)
    
    # Perform the search based on the selected model
    results = []
    if model == 'boolean':
        result_ids = boolean_model.search(query)
        results = [{'id': doc['id'], 'text': doc['text'], 'rank': 1} for doc in filtered_documents if doc['id'] in result_ids]
    elif model == 'extended_boolean':
        query_terms = [(term, 1.0) for term in query.split()]  # Equal weights
        scores = extended_boolean_model.search(query_terms)
        results = sorted(
            [{'id': doc['id'], 'text': doc['text'], 'rank': scores[doc['id']]} for doc in filtered_documents if doc['id'] in scores],
            key=lambda x: x['rank'],
            reverse=True
        )
    elif model == 'vector':
        scores = vector_model.search(query)
        results = sorted(
            [{'id': doc['id'], 'text': doc['text'], 'rank': scores[doc['id']]} for doc in filtered_documents if doc['id'] in scores],
            key=lambda x: x['rank'],
            reverse=True
        )

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
