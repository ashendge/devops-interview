import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template
from app import db, app
from app.models import User


def make_flask_routes():
    """
    flask routes
    """
    from app import app

    app.add_url_rule('/', endpoint='home', view_func=home, methods=['GET'])
    app.add_url_rule('/alert/mem', endpoint='mem_test', view_func=mem_test, methods=['GET'])
    app.add_url_rule('/alert/cpu', endpoint='cpu_test', view_func=cpu_test, methods=['GET'])
    app.add_url_rule('/users', endpoint='all_users', view_func=all_users, methods=['GET'])
    app.add_url_rule('/<string:username>', endpoint='user_greeting', view_func=greeting, methods=['GET'])



def home():
    return render_template('index.html')


def all_users():
    return render_template(
        'users.html',
        users=db.session.query(User).all()
    )


def greeting(username):
    not_new = True
    user = db.session.query(User).filter(User.username == username).first()
    if not user:
        not_new = False
        user = User(username=username, email='{username}@example.com'.format(username=username))
        db.session.add(user)

        msg = MIMEMultipart('alternative')

        from_addr = 'no-reply@simpleenergy.com'
        to_addr = app.config.get('NOTIFICATION_EMAIL')
        msg['Subject'] = '{username} was here!'.format(username=user.username)
        msg['From'] = from_addr
        msg['To'] = to_addr

        message_body = 'A new user has signed up!'
        msg.attach(MIMEText(message_body, 'plain'))
        msg.attach(MIMEText(message_body, 'html'))

        s = smtplib.SMTP(
            host=app.config.get('SMTP_HOST'),
            port=app.config.get('SMTP_PORT'),
        )
        s.sendmail(from_addr, [to_addr], msg.as_string())
        s.quit()

        # don't save the user if we can't send the email
        db.session.commit()

    return render_template(
        'greetings.html',
        username=user,
        not_new=not_new,
    )


def mem_test():
    data = []
    while True:
        string = '*' * 1024 * 1024 * 1024
        data.append(string)


def cpu_test():
    import multiprocessing
    import math

    def worker():
        x = 0
        while x < 1000000000000000000:
            p = x * math.pi
            p2 = math.sqrt(x**2 + p**2)
            x += 1
        return

    jobs = []
    for i in range(50):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()
