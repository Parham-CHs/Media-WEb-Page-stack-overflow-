from flask import Flask, render_template, request, redirect, session, url_for
import secrets
import os
import pandas as pd



app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


CSV_FILE = './data/posts.csv'

def load_posts():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        posts = df.to_dict(orient='records')
        for post in posts:
            post['comments'] = post['comments'].split('|') if pd.notna(post['comments']) else []
    else:
        posts = []
    return posts

def save_posts(posts):
    df = pd.DataFrame(posts)
    df['comments'] = df['comments'].apply(lambda x: '|'.join(x) if isinstance(x, list) else '')
    df.to_csv(CSV_FILE, index=False)

# Load posts at the start
posts = load_posts()


@app.route('/create', methods=['POST'])
def create_post():
    author = request.form['author']
    title = request.form['title']
    content = request.form['content']
    post = {'author': author, 'title': title, 'content': content, 'comments': []}
    posts.append(post)
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    comment = request.form['comment']
    posts[post_id]['comments'].append(comment)
    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('./index.html' , username = session['username'] , posts=posts)


@app.route('/register')
def register():
    return render_template('login.html')


@app.route('/login')
def login():
    failure_message = ""
    if request.args.get('failure'):
        failure_message = "Invalid username or password. Please try again."
    return render_template('login.html', message=failure_message)


@app.route('/login-post', methods=['post'])
def login_post():

    username = request.form['username']
    password = request.form['password']

    df = pd.read_csv('./Data/user_credentials.csv')
    # Check if the username exists
    if username in df['username'].values:
        # Get the correct password for the username
        correct_password = df.loc[df['username'] == username, 'password'].values[0]
        
        if password == correct_password:
            # If password matches, log in the user
            session['username'] = username
            redirect_path = '/index'
        else:
            # If password does not match, redirect to login failure
            redirect_path = '/login?failure=true'
    else:
        # If username does not exist, redirect to login failure
        redirect_path = '/login?failure=true'
    # return redirect(redirect_path)
    return redirect(redirect_path)



@app.route('/register-post', methods=['POST'])
def register_post():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    
    # Load the DataFrame from the CSV file
    df = pd.read_csv('./Data/user_credentials.csv')
    # Create a new DataFrame with the new user's data
    new_user = pd.DataFrame({
        'username': [name],
        'password': [password],
        'email': [email]
    })

    # Append the new user to the existing DataFrame
    df = pd.concat([df, new_user], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv('./Data/user_credentials.csv', index=False)
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
