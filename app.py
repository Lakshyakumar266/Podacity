from flask import Flask, render_template, session, redirect, flash, request, url_for
from flask_mail import Mail, Message
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import warnings
import random
import math
import json
import os

app = Flask(__name__)
app.secret_key = "suspices"
moment = Moment(app)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['user_gmail'],
    MAIL_PASSWORD=params['user_gmail_pass']
)
mail = Mail(app)

# Creating Config Paths
app.config['PROFILE_UPLOAD_FOLDER'] = params['profile_pic_upload_location']
app.config['THUMBNAIL_UPLOAD_FOLDER'] = params['thumbnail_upload_location']
app.config['PODCAST_UPLOAD_FOLDER'] = params['podcast_upload_location']


# Connection With Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['lical_uri']
    warnings.warn(
        'SQL: Working On Local URI!.', stacklevel=2)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['Prod_uri']
    warnings.warn(
        'SQL: Working On Production URI!.', stacklevel=2)

db = SQLAlchemy(app)


# sno	title	short_intro	intro	audio_file	creator_id	thumbnail	datetime
class Creators(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_pic = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.Text, nullable=False)
    views = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    iscreator = db.Column(db.String(50), nullable=False)
    block = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)


class Applies(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    profile_pic = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.String(50), nullable=False)


class Podcasts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    short_intro = db.Column(db.String(500), nullable=False)
    intro = db.Column(db.String(), nullable=False)
    audio_file = db.Column(db.Text, nullable=False)
    views = db.Column(db.String(100), default=0)
    creator_id = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.String(50), nullable=False)

# Spl Mistake Subscribe


class Subacriber(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(400), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)


# Convert Views to M and K form
def num_system(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


@app.route('/', methods=["GET", "POST"])
def index():
    MaxLength = int(params['max_page_view_value'])
    creators = Creators.query.all()

    # Creators Profile
    ctrarr = []
    for i in range(len(creators)):
        if len(ctrarr) == MaxLength:
            break
        else:
            if int(creators[i].views) >= 1000:
                myctr = creators[i]
                if myctr.profile_pic != 'default_profile.png':
                    ctrarr.append(myctr)

    # Popular Creators
    popcre = []
    for i in range(len(creators)):
        if len(popcre) == MaxLength:
            break
        else:
            if int(creators[i].views) >= 1000:
                popcre.append(creators[i])

    PodcastPage = Podcasts.query.all()
    PodcastPage.reverse()
    Pods = []
    if len(PodcastPage) >= MaxLength:
        for i in range(MaxLength):
            Mypods = PodcastPage[i]
            Pods.append(Mypods)
        print(Pods)
    else:
        Pods = PodcastPage
        print(Pods)
    return render_template('index.html', params=params, creators=creators, popcre=popcre, profils=ctrarr, podcasts=Pods, isat="home")


@app.route('/podcasts', methods=["GET", "POST"])
def podcasts():
    mainposts = Podcasts.query.filter_by().all()
    posts = Podcasts.query.filter_by().all()
    posts.reverse()
    last = math.ceil(len(posts)/int(params['max_page_view_value']))

    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['max_page_view_value']): (page-1)
                  * int(params['max_page_view_value'])+int(params['max_page_view_value'])]

    if(page == 1):
        previous = "#"
        next = "/podcasts?page=" + str(page+1)
    elif(page == last):
        previous = "/podcasts?page=" + str(page-1)
        next = "#"
    else:
        previous = "/podcasts?page=" + str(page-1)
        next = "/podcasts?page=" + str(page+1)

    if(len(mainposts) <= int(params['max_page_view_value'])):
        previous = "#"
        next = "#"

    return render_template('podcast/podcastPage.html', next=next, prev=previous, podcasts=posts, params=params, isat="home")


@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('about.html', params=params, isat="about")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    return render_template('contact.html', params=params, isat="contact")


@app.route('/subscribe', methods=["GET", "POST"])
def subacriber():
    if request.method == "POST":
        email = request.form.get('email')
        query = Subacriber(email=email, datetime=datetime.now())
        db.session.add(query)
        db.session.commit()
        flash('Thanks For Subscribing Us We Will Mail You Every Updates.', 'success')
    return redirect('/')


@app.route('/signup', methods=["GET", "POST"])
def signUp():
    if 'user' in session and session['user'] == True:
        flash('You Are Already Loged In ...', 'warning')
        return redirect('/podcaster_admin/home')
    creators = Creators.query.all()
    if request.method == 'POST':
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        email = request.form.get('email')
        describe = request.form.get('describe')
        username = request.form.get('username')
        profile_pic = request.form.get('profile-pic-loc')
        password = request.form.get('password')

        cuname = []
        cemail = []
        for creator in creators:
            cuname.append(creator.username)
            cemail.append(creator.username)

        if username in cuname or email in cemail:
            flash(
                'Username Or Email Is Alredy Exist. Try Again With Other Credintials.', 'danger')
        else:
            try:
                mail.send_message(f'{username} Aplied For Podcaster In Podacity Website.',
                                  sender=email,
                                  recipients=[params['user_gmail']],
                                  body=f'first_name = {fname}\nlast_name = {lname}\ndescribe={describe}\nemail = {email}\nusername = {username}\niscreator = 0\ndatetime = {datetime.now()}'
                                  )

                # Switch It Off #
                # https://myaccount.google.com/lesssecureapps

                query = Creators(first_name=fname, last_name=lname, profile_pic=profile_pic, email=email,
                                 describe=describe, views='0', username=username, password=password, iscreator=0, block='0', datetime=datetime.now())
                db.session.add(query)
                db.session.commit()

                longname = f'{fname} {lname}'
                query = Applies(name=longname, profile_pic=profile_pic, username=username,
                                email=email, describe=describe, datetime=datetime.now())
                db.session.add(query)
                db.session.commit()

                flash('Your Sign Up Request Has Bean Submited Successfully.', 'success')
                flash('You Have to Wait For 24-48hr For Our Validation Then You Can LogIn <a href="/ourpolicy#joining-policy">read more</a>.', 'warning')
                return redirect('/')
            except Exception as e:
                print(e)
                flash('Try Again Later. Internal Server Error.', 'danger')

    return render_template('account/signup.html', params=params, file_name='default_profile.png')


@app.route('/signup/upload', methods=["GET", "POST"])
def signup_upload():
    if request.method == 'POST':
        f = request.files['profile-pic']
        f.save(os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], f.filename))
        flash('Your Profile Picture Uploaded Successfully Now You can Fill the SignUp Form.', 'success')
        return render_template('account/signup.html', params=params, file_name=f.filename)
    flash('Some Error Ocored Try Again Later On.', 'danger')
    return redirect('/signup')


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user' in session and session['user'] == True:
        creator = Creators.query.filter_by(
            username=session['username']).first()
        if creator.block == '1':
            try:
                session.pop("user")
                session.pop("username")
                flash("You Are Blocked You Can't Login Now.", "danger")
                return redirect('/login')
            except Exception as e:
                flash('Some Error Ocered You Cant LogIn Now.', 'danger')
                return redirect('/login')
            return redirect('/login')
        else:
            flash('You Are Already Loged In.', 'info')
            return redirect('/podcaster_admin/home')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            creator = Creators.query.filter_by(
                username=username, password=password).first()
            if creator.block == '1':
                flash("You Are Blocked You Can't Login Now.", "danger")
                return redirect('/login')
            else:
                session['username'] = username
                session['user'] = True
                flash('You Have Been Loged In You Are a Creator Now.', 'success')
                return redirect('/podcaster_admin/home')
        except Exception as e:
            print(e)
            flash(
                'Wrong Username Or Password, Try Aagin With Correct Credintials.', 'danger')
            return redirect('/login')
    return render_template('account/login.html', params=params)


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if 'admin' in session and session['admin'] == True:
        return redirect('/dashboard_admin/home')
    return redirect('/dashboard_login')


@app.route('/dashboard_login', methods=["GET", "POST"])
def admin_login():
    if 'admin' in session and session['admin'] == True:
        return redirect('/dashboard_admin/home')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == params['admin_username'] and password == params['admin_password']:
            session['admin'] = True
            flash('LogIn Successfully. You Have Admin Power Now.', 'success')
            return redirect('/dashboard_admin/home')
        else:
            flash('Sorry Username Or Password Incorrect.', 'danger')
            return redirect('/dashboard_login')
    flash('Login First For Admin dashboard Access.', 'warning')
    return render_template('admin/dashboard_login.html', params=params)


@app.route('/dashboard_admin/home', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' in session and session['admin'] == True:
        ApliedUsers = Applies.query.filter_by().all()
        AllCreators = Creators.query.filter_by(iscreator='1').all()
        AllBlocked = Creators.query.filter_by(block='1').all()
        return render_template('admin/dashboard_admin.html', params=params, ApliedUsers=ApliedUsers, AllCreators=AllCreators, AllBlocked=AllBlocked)
    return redirect('/dashboard_login')


@app.route('/dashboard_admin/aplications/<username>', methods=['GET', 'POST'])
def aplication_allow(username):
    if 'admin' in session and session['admin'] == True:
        alowed = request.args.get('allow')
        if alowed == 'True':
            try:
                query = Creators.query.filter_by(username=username).first()
                query.iscreator = '1'
                db.session.commit()
                done = True
            except:
                done = False

            if done == True:
                try:
                    query = Applies.query.filter_by(username=username).first()
                    db.session.delete(query)
                    db.session.commit()
                    done = True
                except:
                    done = False

            if done == True:
                try:
                    query = Creators.query.filter_by(username=username).first()
                    mail.send_message(f'Creater Verefication Success On '+params['website_name'],
                                      sender=query.email,
                                      recipients=[query.email],
                                      html=f'Congratulations You Are Selected For Creator On ' +
                                      params['website_name'] +
                                      ' Website Now\n<b>Folow This Link To </b> <a href="' +
                                      params['website_url']+'/login">Login</a>'
                                      )
                    print('oooooooooooooooooooooop')
                    done == True
                except Exception as e:
                    print(e)
                    done == False

            if done == True:
                flash('User Is a Creator Now...', 'success')
            else:
                flash('Some Internal Server Error Try Again later On.', 'danger')
        elif alowed == 'False':
            try:
                query = Creators.query.filter_by(username=username).first()
                mail.send_message(f'Creater Verefication failure'+params['website_name'],
                                  sender=query.email,
                                  recipients=[query.email],
                                  html=f'Congratulations You Are Selected For Creator On ' +
                                  params['website_name'] +
                                  f' Website Now\n<b>Folow This Link To Login </b> <a href="//ok">ok</a>'
                                  )
                done = True
            except:
                done = False

            try:
                query = Creators.query.filter_by(username=username).first()
                db.session.delete(query)
                done = True
            except:
                done = False

            if done == True:
                try:
                    query = Applies.query.filter_by(username=username).first()
                    db.session.delete(query)
                    db.session.commit()
                    done = True
                except:
                    done = False

            if done == True:
                flash('User Is a Creator Now...', 'success')
            else:
                flash('Some Internal Server Error Try Again later On.', 'danger')
        return redirect('/dashboard_admin/home')
    return redirect('/dashboard_login')


@app.route('/dashboard_admin/creator/block/<username>', methods=['GET', 'POST'])
def creators_block(username):
    if 'admin' in session and session['admin'] == True:
        block = request.args.get('block')
        if block == 'True':
            try:
                query = Creators.query.filter_by(username=username).first()
                query.block = '1'
                db.session.commit()
                done = True
            except:
                done = False

            if done == True:
                try:
                    query = Creators.query.filter_by(username=username).first()
                    mail.send_message(f'You Have Been Blocked On '+params['website_name'],
                                      sender=query.email,
                                      recipients=[query.email],
                                      html=f'<h1>'+params['website_name']+' Blocked You</h1>' +
                                      f'Your Account Has Been Blocked For Doing Inactivities. Contact ' +
                                      params['user_gmail'] +
                                      f'\n And Request To Get Unblocked.'
                                      )
                    done == True
                except:
                    done == False

            if done == True:
                flash('User Blocked Now...', 'success')
            else:
                flash('Some Internal Server Error Try Again later On.', 'danger')
        elif block == 'False':
            try:
                query = Creators.query.filter_by(username=username).first()
                mail.send_message(f'Congratulations You Got Unblocked On '+params['website_name'],
                                  sender=query.email,
                                  recipients=[query.email],
                                  html=f'<h1>'+params['website_name']+' Unblocked You</h1>' +
                                  f'Congratulations Your Account Has Been Unblocked <b>Dont try To Do Inactivities</b> Otherwise Your Acount Will Be Deleted'
                                  )
                done = True
            except:
                done = False

            try:
                query = Creators.query.filter_by(username=username).first()
                query.block = '0'
                db.session.commit()
                done = True
            except:
                done = False

            if done == True:
                flash('User Unblocked Now...', 'success')
            else:
                flash('Some Internal Server Error Try Again later On.', 'danger')
        return redirect('/dashboard_admin/home')
    return redirect('/dashboard_login')


@app.route('/dashboard_admin/creator/remove/<username>', methods=['GET', 'POST'])
def creators_remove(username):
    if 'admin' in session and session['admin'] == True:
        try:
            query = Creators.query.filter_by(username=username).first()
            mail.send_message(f'Your Account have Been Removed In '+params['website_name'],
                              sender=query.email,
                              recipients=[query.email],
                              html=f'<h1>'+params['website_name']+' Removed You</h1>' +
                              f'Your Account have Been Removed Due To Doing Inactivities. Contact ' +
                              params['user_gmail'] +
                              f'\n For More Information.'
                              )
            done = True
        except:
            done = False

        if done == True:
            try:
                query = Creators.query.filter_by(username=username).first()
                db.session.delete(query)
                db.session.commit()
                done = True
            except:
                done = False

        if done == True:
            flash('User Removed Now...', 'success')
        else:
            flash('Some Internal Server Error Try Again later On.', 'danger')
        return redirect('/dashboard_admin/home')
    return redirect('/dashboard_login')


@app.route('/dashboard_logout', methods=['GET', 'POST'])
def admin_logout():
    if 'admin' in session and session['admin'] == True:
        try:
            session.pop("admin")
            return redirect('/dashboard_admin/home')
        except Exception as e:
            flash('Some Error Ocered You Cant LogOut Now.', 'danger')
            return redirect('/dashboard_admin/home')
    return redirect('/dashboard_login')


# Podcaster Admin Panel
@app.route('/ourpolicy', methods=["GET", "POST"])
def policy_view():
    return render_template('account/policy.html', params=params)


@app.route('/podcaster_admin/home', methods=["GET", "POST"])
def podcaster_home():
    if 'user' in session and session['user'] == True:
        username = session['username']
        Creator = Creators.query.filter_by(username=username).first()
        Podcast = Podcasts.query.filter_by(creator_id=Creator.uid).all()
        return render_template('podcaster/podcaster_admin.html', params=params, username=username, Creator=Creator, Podcasts=Podcast)
    return redirect('/login')


@app.route('/podcaster_admin/update_password', methods=["GET", "POST"])
def podcaster_Change_Password():
    if 'user' in session and session['user'] == True:
        if request.method == "POST":
            username = session['username']
            Creator = Creators.query.filter_by(username=username).first()
            o_password = request.form.get('old_password')
            n_password = request.form.get('new_password')
            r_password = request.form.get('re_password')
            if o_password == Creator.password and n_password == r_password:
                try:
                    query = Creators.query.filter_by(username=username).first()
                    query.password = n_password
                    db.session.commit()
                    flash("Your Password Updated Successfully...", "success")
                    return redirect('/podcaster_admin/home')
                except Exception as e:
                    flash(
                        "Your Password Not Changed due To Some Internal Server Error Try Again Next Time.", "danger")
                    return redirect('/podcaster_admin/home')
            else:
                flash("Wrong Credintial try Again With Correct Values.", "danger")
                return redirect('/podcaster_admin/home')

    return redirect('/login')


@app.route('/podcaster_admin/update_settings', methods=["GET", "POST"])
def podcaster_update_credintials():
    if 'user' in session and session['user'] == True:
        if request.method == "POST":
            username = session['username']
            Creator = Creators.query.filter_by(username=username).first()
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            bio = request.form.get('bio')
            nameArray = full_name.split()
            try:
                Creator.first_name = nameArray[0]
                Creator.last_name = nameArray[1]
                Creator.email = email
                Creator.describe = bio
                db.session.commit()
                flash('Your credintials Updated Successfuly.', 'success')
                return redirect('/podcaster_admin/home')
            except Exception as e:
                flash('cant Update Your credintials Now.', 'danger')
                return redirect('/podcaster_admin/home')
    return redirect('/login')


@app.route('/podcaster_admin/pic_update', methods=["GET", "POST"])
def podcaster_Change_pic():
    if 'user' in session and session['user'] == True:
        if request.method == "POST":
            username = session['username']
            Creator = Creators.query.filter_by(username=username).first()
            file_image = request.files['add_image']
            profile_pic = Creator.profile_pic
            if profile_pic == 'default_profile.png':
                try:
                    file_image.save(os.path.join(
                        app.config['PROFILE_UPLOAD_FOLDER'], file_image.filename))
                    Creator.profile_pic = file_image.filename
                    db.session.commit()
                    flash('Your Profile Picture Updated Successfully.', 'success')
                    return redirect('/podcaster_admin/home')
                except Exception as e:
                    flash('''Can't Change Profile Picture Now.''', 'danger')
                    return redirect('/podcaster_admin/home')
            else:
                try:
                    image_old = f'''{ app.config['PROFILE_UPLOAD_FOLDER'] }\\{ profile_pic }'''
                    if os.path.exists(image_old):
                        os.remove(image_old)
                        file_image.save(os.path.join(
                            app.config['PROFILE_UPLOAD_FOLDER'], file_image.filename))
                        Creator.profile_pic = file_image.filename
                        db.session.commit()

                        flash('Your Profile Picture Updated Successfully.', 'success')
                        return redirect('/podcaster_admin/home')
                    else:
                        file_image.save(os.path.join(
                            app.config['PROFILE_UPLOAD_FOLDER'], file_image.filename))
                        Creator.profile_pic = file_image.filename
                        db.session.commit()

                        flash('Your Profile Picture Updated Successfully.', 'success')
                        return redirect('/podcaster_admin/home')
                except Exception as e:
                    flash('''Can't Change Profile Picture Now.''', 'danger')
                    return redirect('/podcaster_admin/home')
    return redirect('/login')


@app.route('/podcaster_admin/podcast_fils_upload', methods=["GET", "POST"])
def podcast_fils_upload():
    if 'user' in session and session['user'] == True:
        if request.method == "POST":
            audio = request.files['audio']
            thumbnail = request.files['thumbnail']

            username = session['username']
            Creator = Creators.query.filter_by(username=username).first()

            try:
                # Save Files
                audio.save(os.path.join(
                    app.config['PODCAST_UPLOAD_FOLDER'], audio.filename))
                thumbnail.save(os.path.join(
                    app.config['THUMBNAIL_UPLOAD_FOLDER'], thumbnail.filename))

                # save configs
                audio_file = audio.filename
                thumbnail_file = thumbnail.filename
                flash(
                    "Your Files Uploaded SucesFully Now You can Go and Fill The exces Form", 'success')
            except Exeptation as e:
                flash('Sumthing went Wrong Your Fils Are Not uploaded', 'danger')

            return render_template('podcaster/podcaster_admin.html', params=params, username=username, Creator=Creator, audio_file=audio_file, thumbnail_file=thumbnail_file, fils_added=True)
    return redirect('/login')


@app.route('/podcaster_admin/podcast/add', methods=["GET", "POST"])
def podcast_Add():
    if 'user' in session and session['user'] == True:
        if request.method == "POST":
            # sno title short_intro intro audio_file views creator_id thumbnail datetime
            username = session['username']
            Creator = Creators.query.filter_by(username=username).first()
            title = request.form.get('title')
            shortDec = request.form.get('shortDec')
            pageDsn = request.form.get('pageDsn')
            audio = request.form.get('audio')
            thumbnail = request.form.get('thumbnail')
            try:
                query = Podcasts(title=title, short_intro=shortDec, intro=pageDsn, audio_file=audio,
                                 views='0', creator_id=Creator.uid, username=username, thumbnail=thumbnail, datetime=datetime.now())
                db.session.add(query)
                db.session.commit()
                flash(
                    '''Your Podcast Is Added succesfully. Look At Podcasts Tab For Your Podcast Link.''', 'success')
                return redirect('/podcaster_admin/home')
            except Exception as e:
                flash('''Can't Add Podcast Now''', 'danger')
                print(e)
                return redirect('/podcaster_admin/home')
    return redirect('/login')


@app.route('/podcaster_admin/delete/<username>/<sno>', methods=["GET", "POST"])
def delete_podcast(username, sno):
    if 'user' in session and session['user'] == True:
        podcast = Podcasts.query.filter_by(username=username, sno=sno).first()
        if session['username'] == podcast.username:
            db.session.delete(podcast)
            db.session.commit()
            flash('Podcast deleted...', 'success')
    return redirect('/podcaster_admin/home')


@app.route('/podcaster_admin/edit/<sno>', methods=["GET", "POST"])
def edit_podcast(sno):
    if 'user' in session and session['user'] == True:
        podcast = Podcasts.query.filter_by(sno=sno).first()
        if session['username'] == podcast.username:
            if request.method == 'POST':
                title = request.form.get('title')
                shortDec = request.form.get('shortDec')
                pageDsn = request.form.get('pageDsn')

                podcast.title = title
                podcast.short_intro = shortDec
                podcast.intro = pageDsn

                db.session.commit()
                flash('podcast Updated...', 'success')
                return redirect(f"/podcast/{session['username']}/{sno}")

            flash('You Can Edit this Post Now.', 'success')
            return render_template('/podcast/podcast_edit.html', params=params, podcast=podcast)
    return redirect('/podcaster_admin/home')


@app.route('/podcast/<username>/<sno>', methods=["GET", "POST"])
def podcast_view(username, sno):
    Creator = Creators.query.filter_by(username=username).first()
    Podcast = Podcasts.query.filter_by(sno=sno).first()
    RecPodcast = Podcasts.query.filter_by(creator_id=Creators.uid).all()
    RecPodcast.reverse()
    RecPodcast = RecPodcast[0:int(params['max_rec_page'])]
    return render_template('podcast/post.html', params=params, creator=Creator, podcast=Podcast, RecPodcast=RecPodcast)


@app.route('/user_logout', methods=['GET', 'POST'])
def user_logout():
    if 'user' in session and session['user'] == True:
        try:
            session.pop("user")
            session.pop("username")
            flash('Successfully You Loged Out ...', 'info')
            return redirect('/login')
        except Exception as e:
            flash('Some Error Ocered You Cant LogOut Now.', 'danger')
            return redirect('/login')
    return redirect('/login')


# Error Page Handle
@app.errorhandler(404)
def bar(error):
    return render_template('error.html', params=params), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2000, debug=True)
