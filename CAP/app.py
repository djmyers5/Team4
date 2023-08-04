from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secret key for session security

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

        # Redirect to the login page after creating the account
        return redirect(url_for('login'))

    return redirect(url_for('welcome'))


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email and password exist in the database
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            select_query = "SELECT COUNT(*) FROM users WHERE email=%s AND password=%s"
            data = (email, password)
            cursor.execute(select_query, data)
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            if result[0] == 1:
                # Set the user's email in the session upon successful login
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                # Invalid credentials, redirect back to the login page with an error message
                return redirect(url_for('login'))

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)

    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in (i.e., email is present in the session)
    if 'email' in session:
        # Retrieve the user's name from the users table
        email = session['email']
        user_name = None

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            select_query = "SELECT name FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()

            if result:
                user_name = result[0]

            # Fetch all posts from the user_posts table (including the "company" information)
            select_query = "SELECT name, DAT, topic, post, company, industry FROM user_posts"
            cursor.execute(select_query)
            posts = cursor.fetchall()

            cursor.close()
            connection.close()

            # Render the dashboard template and pass the name and posts to it
            return render_template('dashboard.html', user_name=user_name, posts=posts)

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))

@app.route('/create_post')
def create_post():
    return render_template('createpost.html')

@app.route('/save_post', methods=['POST'])
def save_post():
    if request.method == 'POST':
        title = request.form['title']
        company_name = request.form['company_name']
        industry = request.form['industry']
        post_content = request.form['post_content']
        
        # Retrieve the user's name from the session
        if 'email' in session:
            email = session['email']
            user_name = None
            
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
                
                # Get the user's name from the users table
                select_query = "SELECT name FROM users WHERE email = %s"
                cursor.execute(select_query, (email,))
                result = cursor.fetchone()
                
                if result:
                    user_name = result[0]
                    
                    # Insert the post into the user_posts table
                    insert_query = "INSERT INTO user_posts (name, DAT, topic, post, industry, company) VALUES (%s, NOW(), %s, %s, %s, %s)"
                    data = (user_name, title, post_content, industry, company_name)
                    cursor.execute(insert_query, data)
                    connection.commit()
                    
                    cursor.close()
                    connection.close()
                    
                    # Redirect to the dashboard page after saving the post
                    return redirect(url_for('dashboard'))
                
            except mysql.connector.Error as error:
                print("Error while connecting to MySQL:", error)

    return redirect(url_for('create_post'))

@app.route('/edit_profile')
def edit_profile():
    # Retrieve the user's name and other details from the database (replace this with your actual code)
    if 'email' in session:
        email = session['email']
        user_data = None

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Get the user's details from the users table
            select_query = "SELECT name, email, industry FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()

            if result:
                user_data = {
                    'name': result[0],
                    'email': result[1],
                    'industry': result[2]
                }

            cursor.close()
            connection.close()

            # Render the editprofile.html template and pass the user's details to it
            return render_template('editprofile.html', user=user_data)

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))

@app.route('/save_changes', methods=['POST'])
def save_changes():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        industry = request.form['industry']

        # Update the user's details in the database
        if 'email' in session:
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                update_query = "UPDATE users SET name = %s, email = %s, password = %s, industry = %s WHERE email = %s"
                data = (name, email, password, industry, session['email'])
                cursor.execute(update_query, data)
                connection.commit()

                cursor.close()
                connection.close()

            except mysql.connector.Error as error:
                print("Error while connecting to MySQL:", error)

            # Redirect to the dashboard page after saving the changes
            return redirect(url_for('dashboard'))

    return redirect(url_for('edit_profile'))

@app.route('/flag_post', methods=['POST'])
def flag_post():
    if request.method == 'POST':
        post_id = request.form['post_id']

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Update the 'flag' column to 1 (flagged) for the post with the given post_id
            update_query = "UPDATE user_posts SET flag = %s WHERE id = %s"
            data = (1, post_id)
            cursor.execute(update_query, data)
            connection.commit()

            cursor.close()
            connection.close()

            # Redirect back to the dashboard after flagging the post
            return redirect(url_for('dashboard'))

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)

    # If there is an error or the method is not POST, redirect back to the dashboard
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    # Redirect to the login page after logging out
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
