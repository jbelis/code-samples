import hashlib
import smtplib
import sqlite3

class UserValidator:
    @staticmethod
    def validate_username(username):
        if not username or len(username) < 3:
            raise ValueError("Invalid username")
        return username

    @staticmethod
    def validate_email(email):
        if not email or '@' not in email:
            raise ValueError("Invalid email")
        return email

class PasswordEncoder:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def save_user(self, username, email, hashed_password):
        try:
            self.db.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
        except Exception as e:
            raise RuntimeError(f"Database error: {e}")

class EmailService:
    @staticmethod
    def send_welcome_email(email, username):
        try:
            server = smtplib.SMTP('localhost')
            server.sendmail(
                'welcome@example.com', 
                email, 
                f"Welcome, {username}!"
            )
            server.quit()
        except Exception as e:
            raise RuntimeError(f"Failed to send welcome email") from e

class UserService:
    def __init__(self, repository, email_service):
        self.repository = repository
        self.email_service = email_service
    
    def create_user(self, username, email, password):
        # Orchestrates the user creation process
        # Each step is delegated to a specialized class
        validated_username = UserValidator.validate_username(username)
        validated_email = UserValidator.validate_email(email)
        hashed_password = PasswordEncoder.hash_password(password)
        
        self.repository.save_user(
            validated_username, 
            validated_email, 
            hashed_password
        )
        
        self.email_service.send_welcome_email(
            validated_email, 
            validated_username
        )

if __name__ == '__main__':
    db = sqlite3.connect(":memory:")
    db.cursor().execute('''
CREATE TABLE users (
	username TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL UNIQUE
);''')

    repository = UserRepository(db)
    email_service = EmailService()
    user_service = UserService(repository, email_service)
    
    try:
        user_service.create_user("john", "johne@xample.com", "password")
    except ValueError as e:
        print(f"Validation error: {e}")
    except RuntimeError as e:
        print(e)

