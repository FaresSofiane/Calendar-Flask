from flask import Flask, render_template, jsonify, request,redirect, url_for
app = Flask(__name__)

import sqlite3
from datetime import datetime

import os

os.remove('database.db')

conn = sqlite3.connect('database.db')

cursor = conn.cursor()


create_table_query = '''
CREATE TABLE IF NOT EXISTS Calendar (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date DATE NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);
'''

cursor.execute(create_table_query)

date_str1 = '2023-08-15'
formatted_date1 = datetime.strptime(date_str1, '%Y-%m-%d').date()
insert_query1 = '''
INSERT INTO Calendar (title, date)
VALUES (?, ?)
'''
data1 = ('Événement spécial 1', formatted_date1)
cursor.execute(insert_query1, data1)

# Insérer le deuxième enregistrement
date_str2 = '2023-08-20'
formatted_date2 = datetime.strptime(date_str2, '%Y-%m-%d').date()
insert_query2 = '''
INSERT INTO Calendar (title, date)
VALUES (?, ?)
'''
data2 = ('Événement spécial 2', formatted_date2)
cursor.execute(insert_query2, data2)




conn.commit()
conn.close()

events = []


def events_json():
    global events
    events = []

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    select_query = ''' 
    SELECT * FROM Calendar
    '''
    cursor.execute(select_query)
    res = cursor.fetchall()

    for element in res:
        x = {
            'id': element[0],
            'title': element[1],
            'date': element[2]

        }
        
        events = events + [x]
    conn.commit()
    conn.close()



    return events


@app.route('/')
def calendar():
    return render_template('calendar.html')

@app.route('/events', methods=['GET', 'POST'])
def get_events():
    global events

    

    if request.method == 'POST':
        request_data = request.get_json()
        import json

        json_output = json.dumps(request_data, ensure_ascii=False, indent=4)

        json_output = json.loads(json_output)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        for element in json_output:


            select_query = '''
            SELECT * FROM Calendar
            WHERE id = ?
            '''
            cursor.execute(select_query, (element['id'],))
            res = cursor.fetchall()
            print(res)
            print(element['start'])
            print(element['id'])
            print(res[0][2])
            if res[0][2] != element['start']:
                
                update_query = '''
                UPDATE Calendar
                SET date = ?
                WHERE id = ?
                '''
                date_str2 = element['start']
                formatted_date2 = datetime.strptime(date_str2, '%Y-%m-%d').date()
                cursor.execute(update_query, (formatted_date2, element['id']))

                
            
        conn.commit()
        conn.close()

        return jsonify(events_json())
        


    return jsonify(events_json())

@app.route('/add-calendar', methods=['GET','POST'])
def add_event():
    if request.method == 'POST':
        

        title = request.form['title']
        date = request.form['date']

        print(title)
        print(date)
        

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        insert_query = '''
        INSERT INTO Calendar (title, date)
        VALUES (?, ?)
        '''
        date_str2 = date
        formatted_date2 = datetime.strptime(date_str2, '%m/%d/%Y').date()
        data = (title, formatted_date2)
        cursor.execute(insert_query, data)

        conn.commit()
        conn.close()




        return redirect(url_for('calendar'))
    
    else:
        return render_template('add.html')


if __name__ == '__main__':

    app.run(debug=True)

