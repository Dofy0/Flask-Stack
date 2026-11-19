"""
Flask Queue Simulator
"""

import os
import secrets

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)

from queue_model import Queue

app = Flask(__name__)

app.config['SECRET_KEY'] = (
    os.environ.get('SECRET_KEY') or secrets.token_hex(32)
)

MAX_ITEMS = 20
MAX_LENGTH = 24


@app.route('/')
def index():
    queue = Queue(session.get('items', []))

    return render_template(
        'index.html',
        items=queue.items,
        size=queue.size(),
        removed=session.get('removed', []),
        highlight=request.args.get('peek') == '1'
    )


@app.route('/queue', methods=['POST'])
def operate():
    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()

    queue = Queue(session.get('items', []))
    removed = session.get('removed', [])

    peek_flag = False

    if action == 'enqueue':
        if not value:
            flash('Please enter a value.', 'warning')
        elif len(value) > MAX_LENGTH:
            flash('Value must be 1-24 characters.', 'warning')
        elif queue.size() >= MAX_ITEMS:
            flash('Queue is full! Maximum is 20 items.', 'danger')
        else:
            queue.enqueue(value)
            flash(f'{value} successfully enqueued!', 'success')

    elif action == 'dequeue':
        if queue.is_empty():
            flash('Queue is empty! Nothing to dequeue.', 'warning')
        else:
            deleted = queue.dequeue()
            removed.append(deleted)
            removed = removed[-MAX_ITEMS:]
            flash(f'{deleted} successfully dequeued!', 'success')

    elif action == 'peek':
        if queue.is_empty():
            flash('Queue is empty! Nothing to peek.', 'warning')
        else:
            flash(f'Front item: {queue.peek()}', 'info')
            peek_flag = True

    elif action == 'clear':
        queue.clear()
        removed = []
        flash('Queue and removed items cleared!', 'success')

    else:
        flash('Invalid operation.', 'danger')

    session['items'] = queue.items
    session['removed'] = removed

    if peek_flag:
        return redirect(url_for('index', peek='1'))

    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
