from flask import Flask, jsonify, request, json
import mysql.connector


app = Flask(__name__)

def establish_connection():
    conn = mysql.connector.connect(
        user='username', password='password', host="127.0.0.1", port="3306", database="WaterCarrier"
    )
    return conn



@app.route('/')
def index():
    return "Hello from Water Carrier"

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    try:
        conn = establish_connection()
        cursor = conn.cursor()
        if request.method == "GET":
            cursor.execute("SELECT * FROM user")
            data = cursor.fetchall()
            user_list = []
            for row in data:
                user = {
                    'userid': row[0],
                    'username': row[1],
                    'firstname': row[2],
                    'lastname': row[3],
                    'email': row[4],
                    'password': row[5]
                }
                user_list.append(user)
            return jsonify({'data': user_list}), 200
        elif request.method == "POST":
            data = request.json
            username_col = data.get('username')
            firstname_col = data.get('firstname')
            lastname_col = data.get('lastname')
            email_col = data.get('email')   
            password_col = data.get('password')  
            if username_col is None or firstname_col is None or lastname_col is None or email_col is None or password_col is None:
                return jsonify({'message': 'first name, last name, username, email and password are required'}), 400 
            query = "INSERT INTO user(username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)"
            values = (username_col, firstname_col, lastname_col, email_col, password_col)
            cursor.execute(query, values)
            new_user_id = cursor.lastrowid
            user = {
                'userid': new_user_id,
                'username': username_col,
                'firstname': firstname_col,
                'lastname': lastname_col,
                'email': email_col,
                'password': password_col
            }
            conn.commit()
            return jsonify({'data': user}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to execute database operation', 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users/<userid>', methods=['GET', 'PUT', 'DELETE'])
def user(userid):
    try:
        conn = establish_connection()  
        cursor = conn.cursor()
        if request.method == "GET":
            cursor.execute("SELECT * FROM user WHERE userid=%s", (userid,))
            data = cursor.fetchone()
            if data is None: 
                return jsonify({'message': 'Data does not exist'}), 400
            user = {
                'userid': data[0],
                'username': data[1],
                'firstname': data[2],
                'lastname': data[3],
                'email': data[4],
                'password': data[5]
            }
            return jsonify({'data': user}), 200
        elif request.method == "PUT":
            data = request.json
            username_col = data.get('username')
            firstname_col = data.get('firstname')
            lastname_col = data.get('lastname')
            email_col = data.get('email')
            password_col = data.get('password')
            param_list = []
            update_query = "UPDATE user SET "
            if username_col is not None:
                update_query += "username=%s, "
                param_list.append(username_col)
            if firstname_col is not None:
                update_query += "firstname=%s, "
                param_list.append(firstname_col)
            if lastname_col is not None:
                update_query += "lastname=%s, "
                param_list.append(lastname_col)
            if password_col is not None:
                update_query += "password=%s, "
                param_list.append(password_col)
            if email_col is not None:
                update_query += "email=%s, "
                param_list.append(email_col)
            update_query = update_query.rstrip(", ")
            update_query += " WHERE userid=%s"
            param_list.append(userid)
            cursor.execute(update_query, tuple(param_list))
            if cursor.rowcount == 0:
                return jsonify({'message': 'User not found or failed to update data'}), 404
            conn.commit()
            return jsonify({'message': 'Data updated successfully'}), 200
        elif request.method == "DELETE":
            cursor.execute("DELETE FROM user WHERE userid=%s", (userid,))
            if cursor.rowcount == 0:
                return jsonify({'message': 'User not found'}), 404
            conn.commit()
            cursor.close()
            return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to execute database operation', 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/events', methods=['GET', 'POST'])
def get_events():
    try:
        conn = establish_connection()
        cursor = conn.cursor()
        if request.method == 'GET':
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM event")
            data = cursor.fetchall()
            event_list = []
            for row in data:
                event = {
                    'eventid': row[0],
                    'difficulty': row[1],
                    'duration': row[2],
                    'score': row[3],
                    'userid': row[4],
                    'result': row[5]
                }
                event_list.append(event)
            conn.commit()
            return jsonify({'data': event_list}), 200
        elif request.method == 'POST':
            data = request.json
            duration_col = data.get('duration')
            result_col = data.get('result')
            score_col = data.get('score')
            userid_col = data.get('userid')   
            difficulty_col = data.get('difficulty')   
            if duration_col is None or result_col is None or score_col is None or userid_col is None or difficulty_col is None:
                return jsonify({'message': 'duration, score, userid, difficulty and result are required'}), 400 
            query = "INSERT INTO event(difficulty, duration, score, userid, result) VALUES (%s, %s, %s, %s, %s)"
            values = (difficulty_col, duration_col, score_col, userid_col, result_col)
            cursor.execute(query, values)
            new_event_id = cursor.lastrowid
            event = {
                'eventid': new_event_id,
                'duration': duration_col,
                'result': result_col,
                'score': score_col,
                'userid': userid_col,
                'difficulty': difficulty_col
            }
            conn.commit()
            return jsonify({'data': event}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to execute database operation', 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/events/<eventid>', methods=['GET', 'PUT', 'DELETE'])
def event(eventid):
    try:
        conn = establish_connection()
        cursor = conn.cursor()
        if request.method == "GET":
            cursor.execute("SELECT * FROM event WHERE eventid=%s", (eventid,))
            data = cursor.fetchone()
            if data is None: 
                return jsonify({'message': 'Data does not exist'}), 400
            event = {
                'eventid': data[0],
                'difficulty': data[1],
                'duration': data[2],
                'score': data[3],
                'userid': data[4],
                'result': data[5]
            }
            conn.commit()
            return jsonify({'data': event}), 200
        elif request.method == "PUT":
            data = request.json
            duration_col = data.get('duration')
            result_col = data.get('result')
            score_col = data.get('score')
            userid_col = data.get('userid')   
            difficulty_col = data.get('difficulty')  
            param_list = []
            update_query = "UPDATE event SET "
            if duration_col is not None:
                update_query += "duration=%s, "
                param_list.append(duration_col)
            if result_col is not None:
                update_query += "result=%s, "
                param_list.append(result_col)
            if score_col is not None:
                update_query += "score=%s, "
                param_list.append(score_col)
            if userid_col is not None:
                update_query += "userid=%s, "
                param_list.append(userid_col)
            if difficulty_col is not None:
                update_query += "difficulty=%s, "
                param_list.append(difficulty_col)
            update_query = update_query.rstrip(", ")
            update_query += " WHERE eventid=%s"
            param_list.append(eventid)
            cursor.execute(update_query, tuple(param_list))
            if cursor.rowcount == 0:
                return jsonify({'message': 'Event not found or failed to update data'}), 404
            conn.commit()
            return jsonify({'message': 'Data updated successfully'}), 200
        elif request.method == "DELETE":
            cursor.execute("DELETE FROM event WHERE eventid=%s", (eventid,))
            if cursor.rowcount == 0:
                return jsonify({'message': 'Event not found'}), 404
            conn.commit()
            return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to execute database operation', 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': 'This request is not supported'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0')