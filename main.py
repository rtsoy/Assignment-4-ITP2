from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
db = SQLAlchemy(app)


class Phonebook(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), nullable = False)
    phone_number = db.Column(db.String(32), nullable = False)
    email = db.Column(db.String(32), nullable = False)


@app.route('/')
def main_page():
    phonebook = Phonebook.query.order_by(Phonebook.id.desc()).all()
    return render_template('main.html', phonebook = phonebook)


@app.route('/add-contact', methods = ['POST', 'GET'])
def add_contact():
    if request.method == 'POST':
#         name = request.form['name']
#         phone_number = request.form['phone_number']
#         email = request.form['email']

#         contact = Phonebook(name=name, phone_number=phone_number, email=email)
        contact = Phonebook(**request.form.to_dict(flat=False))

        try:
            db.session.add(contact)
            db.session.commit()
            return redirect('/')
        except:
            return "An error occurred while adding a contact"
    else:
        return render_template('add-contact.html')


@app.route('/<int:id>/edit', methods = ['POST', 'GET'])
def edit_contact(id):
    contact = Phonebook.query.get(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone_number = request.form['phone_number']
        contact.email = request.form['email']

        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred while editing a contact'
    else:
        return render_template('edit-contact.html', contact=contact)


@app.route('/<int:id>/delete')
def delete_contact(id):
    contact = Phonebook.query.get_or_404(id)
    try:
        db.session.delete(contact)
        db.session.commit()
        return redirect('/')
    except:
        return "An error occurred while deleting a contact"


if __name__ == '__main__':
    app.run()
