from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace the following database configurations with your actual MySQL database credentials
db_config = {
    "host": "107.180.1.16",
    "port": 3306,
    "user": "sum2023team4",
    "password": "sum2023team4",
    "database": "sum2023team4",
}

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/save_account', methods=['POST'])
def save_account():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        industry = request.form['industry']

        # Save the user details to the MySQL database
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            insert_query = "INSERT INTO users (name, email, password, industry, user_type) VALUES (%s, %s, %s, %s, %s)"
            data = (name, email, password, industry, 'user')
            cursor.execute(insert_query, data)
            connection.commit()

            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)

        # After saving data, redirect to a new page showing a success message
        return redirect(url_for('success'))

    return redirect(url_for('create_account'))

@app.route('/success')
def success():
    return "Account Created/Updated Successfully."

if __name__ == '__main__':
    app.run(debug=True)
