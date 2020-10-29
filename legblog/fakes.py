import random
import os

from faker import Faker
from sqlalchemy.exc import IntegrityError

from legblog.extensions import db
from legblog.models import Admin, Category, Post, Comment

fake = Faker()


def fake_admin():
    admin = Admin(
        username=os.getenv('USERNAME'),
        blog_title='要遭打对腿',
        blog_sub_title='一个小博客',
        name='TangHao',
        about='简介'
    )
    admin.set_password(os.getenv('PASSWORD'))
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for _ in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for _ in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year(),
            can_comment=True
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for _ in range(count):
        comment = Comment(
            author=fake.name(),
            # email=fake.email(),
            # site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for _ in range(salt):
        comment = Comment(
            author=fake.name(),
            # email=fake.email(),
            # site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author='Tang Hao',
            # email='tanghao@163.com',
            # site='163.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for _ in range(salt):
        comment = Comment(
            author=fake.name(),
            # email=fake.email(),
            # site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
