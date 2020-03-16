
from flask import Flask, request, jsonify, render_template,json
from flask_sqlalchemy import SQLAlchemy
import os
from models import db
from sqlalchemy import create_engine
app = Flask(__name__, static_url_path='/static')

#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
POSTGRES = {
    'user': 'noah',
    'pw': 'noahpostgres',
    'db': 'oxo',
    'host': 'localhost',
    'port': '4600',
}

DEV=1
if DEV == 0:
    app.config['DEVELOPMENT'] = False
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] =    os.environ['DATABASE_URL']       #"postgresql:///oxo"         #'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
else:
    app.config['DEVELOPMENT'] = True
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///oxo"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#'postgresql://noah:noahpostgres@localhost:5432/oxo' #
#"postgresql:///oxo"#
db.init_app(app)

from models import Guide

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/company/search_bar", methods=['GET', 'POST'])
def company_search_bar():
    return render_template('company/search_bar.html')

@app.route("/company/list_search", methods=['GET', 'POST'])
def company_list_search():
    return render_template('company/list_search.html')

@app.route("/company/infor_detail", methods=['GET', 'POST'])
def company_infor_detail():
    return render_template('company/infor_detail.html')


@app.route("/guide/build_profile", methods=['GET', 'POST'])
def guide_build_profile():
    return render_template('guide/build_profile.html')

@app.route("/guide/video_profile", methods=['GET', 'POST'])
def guide_video_profile():
    return render_template('guide/video_profile.html')

@app.route("/guide/time_profile", methods=['GET', 'POST'])
def guide_time_profile():
    return render_template('guide/time_profile.html')


@app.route("/testf", methods=['GET', 'POST'])
def guide_test():
    return render_template('guide/test2.html')



@app.route("/add")
def add_guide():
    name=request.args.get('name')
    password=request.args.get('password')
    gender=request.args.get('gender')
    age = request.args.get('age')
    try:
        guide=Guide(
            name=name,
            password=password,
            gender=gender,
            age = age
        )
        db.session.add(guide)
        db.session.commit()
        return "Guide added. guide id={}".format(guide.id)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        guides=Guide.query.all()
        return  jsonify([e.serialize() for e in guides])
    except Exception as e:
	    return(str(e))


@app.route("/test")
def test():
    try:
        if DEV:
            engine = create_engine("postgresql:///oxo")
        else:
            engine = create_engine(os.environ['DATABASE_URL'] )#                      "postgresql:///oxo")         #postgresql://noah:noahpostgres@localhost:4600/oxo')
        connection = engine.connect()
        my_query = 'SELECT * FROM guides'
        results = connection.execute(my_query).fetchall()
        print(results)
        return jsonify({'result': [dict(row) for row in results]})
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        guide=Guide.query.filter_by(id=id_).first()
        return jsonify(guide.serialize())
    except Exception as e:
	    return(str(e))



if __name__ == '__main__':
    app.run(port=4600)