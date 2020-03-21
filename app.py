
from flask import Flask, request, jsonify, render_template,json, abort,flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from models import db
from sqlalchemy import create_engine
from calendar import Calendar
from datetime import date
import random
import hashlib
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
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 
app.config["ALLOWED_EXTENSIONS"] = ["jpg", "png", "pdf"]
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
    if request.method == 'POST':
        print(request.form)
        if "reset" in request.form:
            try:
                if "price_hour" in request.form:
                    price = request.form["price_hour"]
                    price = price.split("/")[0]
                    priceA,priceB = price.split(" - ")
                    
                    priceA=int(priceA.split("$")[1])
                    priceB=int(priceB.split("$")[1])
                if DEV:
                    engine = create_engine("postgresql:///oxo")
                else:
                    engine = create_engine(os.environ['DATABASE_URL'] )#                      "postgresql:///oxo")         #postgresql://noah:noahpostgres@localhost:4600/oxo')
                connection = engine.connect()
                Query = 'SELECT * FROM guides'
                my_query=""
                if "location" in request.form and request.form["location"]!= "":
                    my_query += "location='"+request.form["location"]+"' "
                if "act_level" in request.form and request.form["act_level"] !="":
                    if my_query!="":
                        my_query+="and "
                    my_query += "act_level='"+request.form["act_level"]+"' "
                if "gender" in request.form and request.form["gender"] !="":
                    if my_query!="":
                        my_query+="and "
                    my_query += "gender='"+request.form["gender"]+"' "
                if "exp" in request.form and request.form["exp"] !="":
                    if my_query!="":
                        my_query+="and "
                    my_query += "exp='"+request.form["exp"]+"' "
                if "language" in request.form and request.form["language"] != "":
                    if my_query!="":
                        my_query+="and "
                    my_query += "language='"+request.form["language"]+"' "
                if my_query!="":
                    Query=Query+" where "+my_query
                print(Query)
                results = connection.execute(Query).fetchall()
                print("==============================")
                guide_list=[]
                for guide in results:
                    if guide[18]!="":
                        #print(int(float(guide[18])))
                        if int(float(guide[18]))>priceA and int(float(guide[18]))<priceB:
                            guide_list.append(guide)
                    else:
                        guide_list.append(guide)
                #for guide in results:
                #    if int(guide[18]) < priceB and int(guide[18])>priceA: 
                #        guide_list.append(Guide(guide[1],guide[2],guide[3],guide[4],guide[5],guide[6],guide[7],guide[8],guide[9],guide[10],guide[11],guide[12],guide[13],guide[14],guide[15],guide[16],guide[17],guide[18],guide[19],guide[20],guide[21],guide[22]))
                #    print(guide[18]+" "+str(priceA)+" "+str(priceB))
                print("Here")
                return render_template('company/list_search.html',results=guide_list,search_alert=True)
                #return jsonify({'result': [dict(row) for row in results]})
            except Exception as e:
                print(str(e))
        if "search" in request.form:
            print("Target search is touch")
            print(request.form)
            if "location" in request.form:
                location = request.form["location"]
            if "act_level" in request.form:
                act_level=request.form["act_level"]
            if "language" in request.form:    
                language = request.form["language"]

            calendar=""
            if request.form['calender']!="":
                if "free" in request.form:
                    calendar=request.form['calender']+"abc"
                else:
                    if "free1" in request.form:
                        calendar=request.form['calender']+"a"
                    elif "free2" in request.form:
                        calendar=request.form['calender']+"b"
                    elif "free3" in request.form:
                        calendar=request.form['calender']+"c"

            try:
                if DEV:
                    engine = create_engine("postgresql:///oxo")
                else:
                    engine = create_engine(os.environ['DATABASE_URL'] )#                      "postgresql:///oxo")         #postgresql://noah:noahpostgres@localhost:4600/oxo')
                connection = engine.connect()
                Query = 'SELECT * FROM guides'
                my_query=""
                if "location" in request.form and location!= "All":
                    my_query += "location='"+location+"' "
                if "act_level" in request.form and act_level !="All":
                    if my_query!="":
                        my_query+="and "
                    my_query += "act_level='"+act_level+"' "
                if "language" in request.form and language != "All":
                    if my_query!="":
                        my_query+="and "
                    my_query += "language='"+language+"' "
                if my_query!="":
                    Query=Query+" where "+my_query
                print(Query)
                results = connection.execute(Query).fetchall()
                #print("==============================")
                #guide_list=[]
                #for guide in results:
                #    guide_list.append(Guide(guide[1],guide[2],guide[3],guide[4],guide[5],guide[6],guide[7],guide[8],guide[9],guide[10],guide[11],guide[12],guide[13],guide[14],guide[15],guide[16],guide[17],guide[18],guide[19],guide[20],guide[21],guide[22]))
                #    print("====================")
                return render_template('company/list_search.html',results=results,search_alert=True)
                #return jsonify({'result': [dict(row) for row in results]})
            except Exception as e:
                print(str(e))
    try:
        guides=Guide.query.all()
        return render_template('company/list_search.html',results=guides,search_alert=True)
    except Exception as e:
	    return render_template('company/list_search.html',search_alert=False)
    return render_template('company/list_search.html',search_alert=False)

@app.route("/company/infor_detail", methods=['GET', 'POST'])
def company_infor_detail():
    if request.method == 'GET':
        print(request.args)
        ID = request.args.get('detailid', default=69)
        try:
            guide=Guide.query.filter_by(id=ID).first()
        except Exception as e:
            print(str(e))
            return render_template('company/infor_detail.html',demo=True)
        return render_template('company/infor_detail.html',demo=False,guide=guide)
    if request.method == 'POST':
        print(request.form)
        if "detail_infor" in request.form:
            try:
                print(request.form["detailid"])
                guide=Guide.query.filter_by(id=request.form["detailid"]).first()
            except Exception as e:
                print(str(e))
                return render_template('company/infor_detail.html',demo=True)
            print(request.form["detailid"])
            return render_template('company/infor_detail.html',demo=False,guide=guide)
    print("Not found ID")
    return render_template('company/infor_detail.html',demo=True)


@app.route("/guide/build_profile", methods=['GET', 'POST'])

def guide_build_profile():
    
    if request.method == 'POST':
        print(request.form)
        if "idprofile" in request.form:
            if request.form["idprofile"]=="Generate":
                text = request.form['ipinput1']
                #Check if text is not in database: use empty select
                check_exist = bool(Guide.query.filter_by(password=str(int(hashlib.sha1(text.encode('utf-8')).hexdigest(), 16) % (10 ** 8))).first())
                #If in database => notification
                if check_exist:
                    flash("Invalid Code, try another")
                    return redirect(request.url)
                #If not in database
                guide = Guide("",text,"","","","","","","","","","https://www.youtube.com/embed/jgE3W8PSj2g","","","","","","","","","","")
                try:
                    db.session.add(guide)
                    db.session.commit()
                    flash("Your Profile ID was created, save it for edit in future")
                except Exception as e:
                    flash("Fail to create new profile, check your Internet connection")
                    return redirect(request.url)
                
                return render_template('guide/build_profile.html',guide=guide, sample_profile=False)
            if request.form["idprofile"]=="Load":
                
                text = request.form['ipinput2']
                try:
                    guide=Guide.query.filter_by(password=str(int(hashlib.sha1(text.encode('utf-8')).hexdigest(), 16) % (10 ** 8))).first()
                    #If password was not created, add some notification
                    #Due with case have two password
                    print( jsonify(guide.serialize()))
                except Exception as e:
                    guide_default = Guide("","12345678","","","","","","","","","","https://www.youtube.com/embed/jgE3W8PSj2g","","","","","","","","","","")
                    flash("This Profile code was not created, please generate new one")
                    return render_template('guide/build_profile.html',guide=guide_default,sample_profile=True)
                flash("Your Previous Updated Profile was loaded")
                return render_template('guide/build_profile.html',guide=guide,sample_profile=False)
        print(request.form)
        print("--------------------------------------")
        print(request.args.getlist('apps[]'))
        if "save" in request.form:
            print("Enter Save")
            
                
            try:
                print("Enter button")
                if DEV:
                    engine = create_engine("postgresql:///oxo")
                else:
                    engine = create_engine(os.environ['DATABASE_URL'] )#                      "postgresql:///oxo")         #postgresql://noah:noahpostgres@localhost:4600/oxo')
                connection = engine.connect()
                print(request.form)
                print(request.files)
                print("Connected")
                
                #print(request.form['idprofile']) #If dont have , try to trick it in form(return outside of form)
                curID = request.form['virtual_get_id']
                name = request.form['name']
                address = request.form['address']
                
                age = request.form['age']
                gender = request.form['gender']
                location = request.form['location']
                language = request.form['language']
                act_level = request.form['act_level']
                exp = request.form['exp']
                bio = request.form['bio']
                email = request.form['email']
                phone = request.form['phone']
                linkin = request.form['linkin']
                price_hour = request.form['price_hour']
                videolink = request.form['videolink']
                print("@@@@@@@@@@@@@@@@@@@@")
                cvlink=""
                cred =""
                avatar=""
                print("@@@@@@@@@@@@@@@@@@@@")
                print(request.files)
                if "avatar" in request.files:
                    if request.files.get('avatar', None):
                        f = request.files['avatar']  
                        avatar= "../static/avatar/"+curID+f.filename
                        f.save("static/avatar/"+curID+f.filename) 
                #print(request.files['cvlink'].filename)

                if "cvlink" in request.files:
                    if request.files.get('cvlink', None):
                        print("ot null")
                        f = request.files['cvlink']  
                        cvlink= "../static/cv/"+curID+f.filename
                        f.save("static/cv/"+curID+f.filename) 
                if "cred" in request.files:
                    if request.files.get('cred', None):
                        f = request.files['cred']  
                        cred= "../static/cred/"+curID+f.filename
                        f.save("static/cred/"+curID+f.filename) 
                #ListUpadate = ["name","cvlink","cred","address","age","gender","location","language","act_level","exp","bio","email","phone","linkin","price_hour","videolink",]
                    
                my_query = ("UPDATE guides SET "+
                                "name ='"+name+"'," +
                                "address ='"+address+"'," +
                                "age ='"+age+"'," +
                                "gender ='"+gender+"'," +
                                "location ='"+location+"'," +
                                "language ='"+language+"'," +
                                "act_level ='"+act_level+"'," +
                                "exp ='"+exp+"'," +
                                "bio ='"+bio+"'," +
                                "email ='"+email+"'," +
                                "phone ='"+phone+"'," +
                                "linkin ='"+linkin+"'," +
                                "price_hour ='"+price_hour+"'," +
                                "videolink ='"+videolink+"' ")
                if cvlink!="":
                    my_query+=",cvlink ='"+cvlink+"'"
                if cred !="":
                    my_query+=",cred ='"+cred+"'"
                if avatar !="":
                    my_query+=",avatar ='"+avatar+"'"
                my_query+= " WHERE id = "+curID+";"
                print(my_query)
                connection.execute(my_query)
                #
                #
                try:
                    guide=Guide.query.filter_by(id=curID).first()
                    print(guide)
                except Exception as e:
                    flash("Save Fail, check internet")
                    return redirect(request.url)
                flash("Profile was saved")
                return render_template('guide/build_profile.html',guide=guide, sample_profile=False)
            except Exception as e:
                return(str(e))
        if "changeid" in request.form:
            curID = request.form["changeid"]
            try:
                guide=Guide.query.filter_by(id=curID).first()
                print(guide)
            except Exception as e:
                flash("Can not move to Edit CV")
                return redirect(request.url)
            flash("Moved to Edit CV")
            return render_template('guide/build_profile.html',guide=guide, sample_profile=False)
        return redirect(request.url)
    else:
        guide_default = Guide("","12345678","","","","","","","","","","https://www.youtube.com/embed/jgE3W8PSj2g","","","","","","","","","","")
        return render_template('guide/build_profile.html',guide=guide_default, sample_profile=True)

@app.route("/guide/job_profile", methods=['GET', 'POST'])
def guide_job_profile():
    '''
    if request.method == 'POST':
        
        if "changeid" in request.form:
            print("cv")
            curID = request.form("changeid")
            try:
                guide=Guide.query.filter_by(id=curID).first()
                print(guide)
            except Exception as e:
                print(e)
                flash("Can not edit")
                return redirect(request.url)
            flash("Edit Profile CV")
            return render_template('guide/build_profile.html',guide=guide, sample_profile=False)
        else:
            print("No")
            '''
    return render_template('guide/job_profile.html')

@app.route("/guide/time_profile", methods=['GET', 'POST'])
def guide_time_profile():
    return render_template('guide/time_profile.html')


@app.route('/guide/cal_profile', defaults={'year': None})
@app.route('/guide/cal_profile/<int:year>/')
def guide_cal_profile(year):

    cal = Calendar(0)
    try:
        if not year:
            year = date.today().year
        cal_list = [
            cal.monthdatescalendar(year, i+1)
            for i in range(12)
        ]
        print(len(cal_list))
        for i in cal_list:
            print(len(i))
        print(cal_list[1][0])
    except:
        abort(404)
    else:
        return render_template('guide/cal_profile.html', year=year, cal=cal_list)
    abort(404)
    #Cac loi
    #Khong chuyen sang nam moi duoc
    #Hien thi Ngay thang truoc


########################################################################## Data Manage Function

@app.route("/addguide_random")
def addguide_random():
    try:
        language=["English","Spanish","Vietnamese","Frech","Chinese","Russian","Korean","Japanese"]
        location=["HoChiMinh","Hoian","Danang","Hanoi","Hue","Sapa","Phuquoc","Halong", "Phanthiet","Mekong","Cuchi"]
        act_level=["Sightseeing","Foodserve","Historical","Exploration"]
        exp=["1year","2year","fresher","student"]
        password = str(random.randrange(10000000))
        print(password)
        avatar = "../static/avatar/"+str(random.randrange(20))+".jpg"
        age = str(random.randrange(18,35))
        guide=Guide("Rebecca Sanders",password,"Female",age,str(random.choice([1, 2, 3, 5,4])),"",avatar,"XIN CHAO (Good Morning Vietnam) Let's call me Chau(Joe). I have been working as a Tour Guide, ...",random.choice(language),"",random.choice(location),"https://www.youtube.com/embed/jgE3W8PSj2g","","https://www.linkedin.com/in/lorem","Rebecca.S@website.com",str(random.choice(act_level)),random.choice(exp),str(random.randrange(1,20)),"123 Tran Hung Dao, 1 District, HCMC","2a;4b;3c;5c;5b","0909190247","12032020a")
    
        db.session.add(guide)
        db.session.commit()
        return "Guide added. guide id={}".format(guide.id)
    except Exception as e:
	    return(str(e))
@app.route("/addguide_url")
def addguide_url():
    name=request.args.get('name')
    password=request.args.get('password')
    gender=request.args.get('gender')
    age = request.args.get('age')
    rating = request.args.get('rating')
    list_review=request.args.get('list_review')
    avatar = request.args.get('avatar')
    bio =request.args.get('bio')
    language =request.args.get('language')
    cred = request.args.get('cred')
    location = request.args.get('location')
    videolink= request.args.get('videolink')
    cvlink =request.args.get('cvlink')
    linkin = request.args.get('linkin')
    email =request.args.get('email')
    act_level = request.args.get('act_level')
    exp = request.args.get('exp')
    price_hour = request.args.get('price_hour')
    address = request.args.get('address')
    freetime = request.args.get('freetime')
    phone = request.args.get('phone')
    calender = request.args.get('calender')
    try:
        guide=Guide(
            name=name,
            password=password,
            gender=gender,
            age = age,
            rating = rating,
            list_review=list_review,
            avatar = avatar,
            bio =bio,
            language =language,
            cred = cred,
            location = location,
            videolink= videolink,
            cvlink =cvlink,
            linkin = linkin,
            email =email,
            act_level = act_level,
            exp = exp,
            price_hour = price_hour,
            address = address,
            freetime = freetime,
            phone = phone,
            calender = calender,
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


@app.route("/testselectquerry")
def testselectquerry():
    try:
        if DEV:
            engine = create_engine("postgresql:///oxo")
        else:
            engine = create_engine(os.environ['DATABASE_URL'] )#                      "postgresql:///oxo")         #postgresql://noah:noahpostgres@localhost:4600/oxo')
        connection = engine.connect()
        my_query = 'SELECT * FROM guides'
        print(my_query)
        results = connection.execute(my_query).fetchall()
        print(results)
        return jsonify({'result': [dict(row) for row in results]})
    except Exception as e:
	    return(str(e))

@app.route("/testupdatequerry")
def testupdatequerry():
    try:
        if DEV:
            engine = create_engine("postgresql:///oxo")
        else:
            engine = create_engine(os.environ['DATABASE_URL'] )#                      "postgresql:///oxo")         #postgresql://noah:noahpostgres@localhost:4600/oxo')
        connection = engine.connect()
        my_query = "Update guides Set name='Amee' where id=3;"
        print(my_query)
        connection.execute(my_query)
        print("---------------------------------")
        my_query = "Select * from guides where id=3;"
        results = connection.execute(my_query).fetchall()
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

@app.route("/deleteall")
def deleteall():
    try:
        if DEV:
            engine = create_engine("postgresql:///oxo")
        else:
            engine = create_engine(os.environ['DATABASE_URL'] )#                      "postgresql:///oxo")         #postgresql://noah:noahpostgres@localhost:4600/oxo')
        connection = engine.connect()
        my_query = "TRUNCATE guides;"
        connection.execute(my_query)
        print("---------------------------------")
        my_query = "DELETE FROM guides;"
        connection.execute(my_query).fetchall()
        my_query = "Select * from guides where id=3;"
        results = connection.execute(my_query).fetchall()
        return jsonify({'result': [dict(row) for row in results]})
    except Exception as e:
	    return(str(e))



if __name__ == '__main__':
    app.run(port=4600)