from flask_mail import Mail, Message

def send_mail(email, message):
    msg = Message(recipients=[email])
    msg.html = render_template('result.html', final=message)
    mail.send(msg)
