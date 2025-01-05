from flask import request, jsonify, render_template,Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from api import scrap,close

app = Flask(__name__,template_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AnimeRec.db'
#initialize the database
db = SQLAlchemy(app)
app.app_context().push()


@app.route('/')
def index():
    return render_template('index.html')

#create a model
class AnimeRec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Engname = db.Column(db.String())
    Japname = db.Column(db.String())
    Type = db.Column(db.String(50))
    status = db.Column(db.String(100))
    genre = db.Column(db.String(250))
    episodes = db.Column(db.Integer)
    image = db.Column(db.String())
    
    #store the object in the database
    def store(self):
        db.session.add(self)
        db.session.commit()



@app.route('/add', methods=['GET'])
def add():
    result=scrap(AnimeRec)
    if result=='Scraping completed':
        return jsonify({'message': 'success'})
    elif result=='Scraping stopped':
        return jsonify({'message': 'stopped'})
    
    
    
@app.route('/show', methods=['GET'])
def show():
    anime = AnimeRec.query.all()
    anime_list = []
    for a in anime:
        anime_list.append({
            'Engname': a.Engname,
            'Japname': a.Japname,
            'Type': a.Type,
            'status': a.status,
            'genre': a.genre,
            'episodes': a.episodes,
            'image': a.image
        })
    return jsonify({'anime': anime_list})


@app.route('/stop' ,methods=['GET'])
def stop():
    close()
    return jsonify({'message': 'success'})

if __name__ == '__main__':
    app.run(debug=True,port=3000,host="0.0.0.0")
    db.drop_all()
    db.create_all()
