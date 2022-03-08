import pymysql
# from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Flask
from flask_cors import CORS, cross_origin
# from app import app
from flaskext.mysql import MySQL


app = Flask(__name__)
CORS(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'healthcare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/add', methods=['POST'])
def add_emp():
    try:
        _json = request.json
        _looking_for = _json['looking_for']
        _products = _json['products']
        _name = _json['name']
        _address = _json['address']
        if _looking_for and _products and _name and _address and request.method == 'POST':
            sqlQuery = "INSERT INTO customers(looking_for, products, name, address) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_looking_for, _products, _name, _address)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, looking_for, products, name, address FROM customers")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/emp/<int:id>')
def employee(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, looking_for, products, name, address FROM customers WHERE id =%s", id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _id = _json['id']
        _looking_for = _json['looking_for']
        _products = _json['products']
        _name = _json['name']
        _address = _json['address']
        # validate the received values
        if _looking_for and _products and _name and _address and _id and request.method == 'PUT':
            sqlQuery = "UPDATE customers SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
            bindData = (_looking_for, _products, _name, _address, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_emp(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id =%s", (id,))
        conn.commit()
        respone = jsonify('Employee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run()