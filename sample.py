from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__ ,template_folder='template')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kowsalya:Kowsi@localhost:5432/test1'
app.debug = True
db = SQLAlchemy(app)
class EmployeeModel(db.Model):
    __tablename__ = "table"

    id = db.Column('id',db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))

def __init__(self, employee_id, name, age, position):
    self.employee_id = employee_id
    self.name = name
    self.age = age
    self.position = position

def __repr__(self):
    return f"{self.name}:{self.employee_id}"

@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')

'''@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html', employees=employees)'''

@app.route('/data/<int:id>')
def RetrieveSingleEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
    return f"Employee with id ={id} Doenst exist"

@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position=position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"

    return render_template('update.html', employee=employee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')

#db.create_all()
#db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
