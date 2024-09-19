import pandas as pd

# Sample data
data = {
    'username': ['user1', 'user2', 'user3'],
    'password': ['password1', 'password2', 'password3'],
    'email': ['email1@sth.com','email1@sth.com','email3@sth.com']
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Exporting to CSV file
df.to_csv('user_credentials.csv', index=False)

print("CSV file created successfully.")
