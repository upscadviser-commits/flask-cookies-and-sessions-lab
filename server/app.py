import os
from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "instance", "app.db")

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize the page_views count if not present
    if 'page_views' not in session:
        session['page_views'] = 0
    
    # Increment the page_views count by 1
    session['page_views'] += 1

    # Check if pageview count exceeds 3
    if session['page_views'] > 3:
        return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)

    # Retrieve the article
    article = db.session.get(Article, id)
    if not article:
        return make_response(jsonify({'error': 'Article not found'}), 404)
        
    return make_response(jsonify(ArticleSchema().dump(article)), 200)


if __name__ == '__main__':
    app.run(port=5555)
