from flask import Blueprint, request, jsonify, render_template
from legblog.extensions import db
from legblog.models import Item
from datetime import datetime
from flask_login import login_required

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/')
def index():
    return render_template('todoism/index.html')


@todo_bp.route('/todoism')
@login_required
def todoism():
    items = Item.query.order_by(Item.timestamp.desc())
    all_count = Item.query.count()
    active_count = Item.query.filter_by(done=False).count()
    completed_count = Item.query.filter_by(done=True).count()
    return render_template('todoism/_todo.html', items=items,
                           all_count=all_count, active_count=active_count, completed_count=completed_count)


@todo_bp.route('/todoism/new', methods=['POST'])
@login_required
def new_item():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    now_time = datetime.now()
    time_str = datetime.strftime(now_time, '%Y/%m/%d')
    item = Item(body=data['body'], timestamp=now_time, update_time=time_str)
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('todoism/_item.html', item=item), message='+1')


@todo_bp.route('/todoism/<int:item_id>/edit', methods=['PUT'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    now_time = datetime.now()
    time_str = datetime.strftime(now_time, '%Y/%m/%d')
    item.body = data['body']
    item.timestamp = now_time
    item.update_time = time_str
    db.session.commit()
    return jsonify(message='待办更新成功')


@todo_bp.route('/todoism/<int:item_id>/toggle', methods=['PATCH'])
@login_required
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)

    item.done = not item.done
    db.session.commit()
    return jsonify(message='待办事项已完成更改')


@todo_bp.route('/todoism/<int:item_id>/delete', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(message='待办事项删除成功')


@todo_bp.route('/todoism/clear', methods=['DELETE'])
@login_required
def clear_items():
    items = Item.query.filter_by(done=True).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return jsonify(message='All clear!')
