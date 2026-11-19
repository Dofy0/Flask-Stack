
"""
Flask Stack Simulator
"""

import os
import secrets

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from stack_model import Stack

# P1 and P2: Flask setup and secret key
app = Flask(__name__)

app.config['SECRET_KEY'] = (
    os.environ.get('SECRET_KEY') or secrets.token_hex(32)
)


# Home page
@app.route('/')
def index():

    stack = Stack(session.get('items', []))

    return render_template(
        'index.html',
        items=list(reversed(stack.items)),
        size=stack.size(),
        popped=session.get('popped', []),
        highlight=request.args.get('peek') == '1'
    )


# P4, P7, P8, P9: Stack operations
@app.route('/stack', methods=['POST'])
def operate():

    # P4: Get action and value
    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()

    # P7: Restore stack and removed history
    stack = Stack(session.get('items', []))
    popped = session.get('popped', [])

    peek_flag = False

    # P8: PUSH
    if action == 'push':

        if not value:
            flash('Please enter a value.', 'warning')

        elif len(value) > 24:
            flash('Value must be 1-24 characters.', 'warning')

        elif stack.size() >= 20:
            flash('Stack is full! Maximum is 20 items.', 'danger')

        else:
            stack.push(value)
            flash(f'{value} successfully pushed!', 'success')

    # POP
    elif action == 'pop':

        if stack.is_empty():
            flash('Stack is empty! Nothing to pop.', 'warning')

        else:
            removed = stack.pop()
            popped.append(removed)

            # Keep only the 20 most recently removed values
            popped = popped[-20:]

            flash(f'{removed} successfully popped!', 'success')

    # PEEK
    elif action == 'peek':

        if stack.is_empty():
            flash('Stack is empty! Nothing to peek.', 'warning')

        else:
            top = stack.peek()
            flash(f'Top item: {top}', 'info')
            peek_flag = True

    # CLEAR
    elif action == 'clear':

        stack.clear()
        popped = []

        flash('Stack and deleted history cleared!', 'success')

    else:
        flash('Invalid operation.', 'danger')

    # P9: Save updated session data
    session['items'] = stack.items
    session['popped'] = popped

    # Redirect to index
    if peek_flag:
        return redirect(url_for('index', peek='1'))

    return redirect(url_for('index'))


# P5: Contact page
@app.route('/contact')
def contact():

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
