from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL
from legblog.models import Category


class LoginForm(FlaskForm):
    username = StringField('账 户：', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密 码：', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登 陆')


class PostForm(FlaskForm):
    title = StringField('题目', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('标签', coerce=int, default=1)
    body = CKEditorField('正文', validators=[DataRequired()])
    submit = SubmitField('提 交')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in
                                 Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('标签', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('提 交')

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('该标签已经被使用.')


class CommentForm(FlaskForm):
    author = StringField('昵称', validators=[DataRequired(), Length(1, 30)])
    # email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    # site = StringField('Site', validators=[DataRequired(), URL(), Length(0, 255)])
    body = TextAreaField('评论区', validators=[DataRequired()])
    submit = SubmitField('提 交')


class AdminCommentForm(CommentForm):
    author = HiddenField()
    # email = HiddenField()
    # site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('昵称', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', default='https://', validators=[DataRequired(), Length(1, 255)])
    submit = SubmitField('提 交')


class SettingForm(FlaskForm):
    name = StringField('用 户 名', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('主 题', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('副 标 题', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('简 介', validators=[DataRequired()])
    submit = SubmitField('提 交')


class MessageBoardForm(FlaskForm):
    name = StringField('昵 称', validators=[DataRequired(), Length(1, 200)])
    contact = StringField('联 系 方 式', validators=[DataRequired(), Length(1, 200)])
    body = TextAreaField('留 言 区', validators=[DataRequired()])
    submit = SubmitField()
