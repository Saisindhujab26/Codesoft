from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime
import json

app = Flask(__name__)

# MySQL Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbotdb"
)

cursor = mydb.cursor()

# Create table if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    chat JSON NOT NULL,
    date DATETIME NOT NULL
)
"""

cursor.execute(create_table_query)
mydb.commit()

# Load brain.txt into a dictionary
brain = {}
with open('brain.txt', 'r') as f:
    for line in f:
        keyword, response = line.strip().split(',', 1)
        brain[keyword.lower()] = response


@app.route('/')
def home():
    return render_template('chat.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_message'].lower()
    options = []
    response = "Ok! We understand your requirements. Please Provice your contact details one of our Representative contact you with details?"
    response = brain.get(user_message, response)
    
    if user_message == 'buy':
        options = ['Location', 'Price', '500 sq yard house', 'Market Trends']
    elif user_message == 'sell':
        options = ['Prepare Property', 'Market Value', 'List on Market', 'Hire Realtor']
    elif user_message == '500 sq yard house':
        options = ['area1', 'area2', 'area3', 'area4']
    elif user_message == 'rent':
        options = ['100 sqyd rent', '200 sqyd rent', '600 sqyd rent', '1000 sqyd rent']
    elif user_message == '100 sqyd rent':
        options = ['100 yard portion', '100 yard apartment']
    elif user_message == 'market value':
        options = ['Market Value 1', 'Market Value 2']
    

    return jsonify(response=response, options=options)


@app.route('/save_lead', methods=['POST'])
def save_lead():
    name = request.form.get('name')
    email = request.form.get('email')
    contact = request.form.get('contact')
    chat = json.dumps(request.form.get('chat'))  # Assuming chat is sent as a JSON string
    date = datetime.now()

    if not name or not email or not contact:
        return jsonify(status="error", message="All fields are required!")
    
    try:
        cursor.execute("INSERT INTO leads (name, email, contact, chat, date) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, contact, chat, date))
        mydb.commit()
        return jsonify(status="success", message="Lead saved successfully")
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        mydb.rollback()
        return jsonify(status="error", message="Unable to save lead")

@app.route('/display_leads')
def display_leads():
    cursor.execute("SELECT * FROM leads")
    data = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    return render_template('your_template_name.html', data=data, column_names=column_names)


if __name__ == '__main__':
    app.run(debug=True)
