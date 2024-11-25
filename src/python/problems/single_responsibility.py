import hashlib
import smtplib
import sqlite3

class UserManager:
    def __init__(self, db):
        self.db = sqlite3.connect(":memory:")
        self.db.cursor().execute('''
CREATE TABLE users (
	username TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL UNIQUE
);''')
    
    def create_user(self, username, email, password):
        # Multiple responsibilities:
        # 1. Validate user input
        # 2. Hash password
        # 3. Database interaction
        # 4. Send welcome email
        
        # Input validation
        if not username or len(username) < 3:
            raise ValueError("Invalid username")
        
        if not email or '@' not in email:
            raise ValueError("Invalid email")
        
        # Password hashing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Database interaction
        try:
            self.db.cursor().execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
        except Exception as e:
            raise RuntimeError(f"Database error: {e}")
        
        # Sending email
        try:
            server = smtplib.SMTP('localhost')
            server.sendmail(
                'welcome@example.com', 
                email, 
                f"Welcome, {username}!"
            )
            server.quit()
        except Exception as e:
            print(f"Failed to send welcome email: {e}")

if __name__ == '__main__':
    db = sqlite3.connect(":memory:")
    db.cursor().execute('''
CREATE TABLE users (
	username TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL UNIQUE
);''')

    um = UserManager(db)
    um.create_user("john", "john@example.com", "password")