from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, make_response  # , abort
from flask_login import current_user
from legblog.models import Post, Category, Comment, MessageBoard
from legblog.forms import AdminCommentForm, CommentForm, MessageBoardForm
# from legblog.emails import send_new_comment_email, send_new_reply_email
from legblog.utils import get_current_theme
from legblog.extensions import db
from legblog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    theme = get_current_theme()
    # response = make_response(redirect_back())
    # response.set_cookie('theme', theme)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['LEGBLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog_bp.route('/about')
def about():
    wechat_payment = '/Users/23mofang/Desktop/WechatIMG31.jpg'
    zhifubao_payment = '/Users/23mofang/Desktop/WechatIMG32.jpeg'
    return render_template('blog/about.html', wechat_payment=wechat_payment, zhifubao_payment=zhifubao_payment)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['LEGBLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['LEGBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.desc()).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        # form.email.data = current_app.config['LEGBLOG_EMAIL']
        # form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = True

    if form.validate_on_submit():
        author = form.author.data
        # email = form.email.data
        # site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author,
            # email=email,
            # site=site,
            body=body,
            from_admin=from_admin,
            post=post,
            reviewed=reviewed
        )
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            # send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论已发布', 'success')
        else:
            flash('您的评论发布成功，若审核存在不适内容，可能会被隐藏', 'info')
            # send_new_comment_email(post)
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, comments=comments, pagination=pagination, form=form)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


@blog_bp.route('/change-theme/<any(black_swan, perfect_blue):theme_name>')
def change_theme(theme_name):
    # if theme_name not in current_app.config['LEGBLOG_THEMES'].keys():
    #     abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response


@blog_bp.route('/message-board', methods=['GET', 'POST'])
def message_board():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['LEGBLOG_MESSAGE_PER_PAGE']
    pagination = MessageBoard.query.order_by(MessageBoard.timestamp.desc()).paginate(page, per_page=per_page)
    messagepage = pagination.items

    form = MessageBoardForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        contact = form.contact.data
        message = MessageBoard(body=body, name=name, contact=contact)
        db.session.add(message)
        db.session.commit()
        flash('您的留言已经被收录', 'info')
        return redirect(url_for('.message_board'))
    return render_template('blog/message_board.html', form=form, messages=messagepage, pagination=pagination)
