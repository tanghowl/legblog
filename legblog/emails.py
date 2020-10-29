from flask import url_for, current_app
from legblog.extensions import mail
from flask_mail import Message
from threading import Thread


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_main(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_main(subject='New comment', to=current_app.config['LEGBLOG_EMAIL'],
              html=f'<p>New comment in post <i>{post.title}</i>, click the link below to check:</p>'
              f'<p><a href={post_url}>{post_url}</p>'
              f'<p><small style="colar: #868e96">Do not reply this email.</smail></p>')

# def send_new_reply_email(comment):
#     post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comment'
#     send_main(subject='New reply', to=comment.email,
#               html=f'<p>New reply for the comment you left in post <i>{comment.post.title}</i>, click the link below the check:</p>'
#               f'<p><a href={post_url}>{post_url}</p>'
#               f'<p><samll style="color: #868e96">Do not reply this email.</small></p>')
