import smtplib
from email.mime.text import MIMEText
import requests



class User:
    def __init__(self, phone, email, notification_type):
        self.phone = phone
        self.email = email
        self.notification_type = notification_type
    

class SMSNotifier:
    def send_message(self, phone_number, message):
        response = requests.post('https://sms-gateway.com/send', json={
            'phone': phone_number,
            'message': message,
            'api_key': 'your-sms-api-key'
        })
        return response.status_code == 200


class EmailNotifier:
    def send_message(self, email, message):
        
        # Hard-coded SMTP configuration
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = "your-email@gmail.com"
        password = "your-email-password"
        
        msg = MIMEText(message)
        msg['Subject'] = "Notification"
        msg['From'] = sender_email
        msg['To'] = email
        
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, email, msg.as_string())
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

class UserNotificationService:
    def __init__(self):
        self.sms_notifier = SMSNotifier()
        self.email_notifier = EmailNotifier()
    
    def notify_user(self, user, message):
        if user.notification_type == 'sms':
            return self.sms_notifier.send_message(user.phone, message)
        elif user.notification_type == 'email':
            return self.email_notifier.send_message(user.email, message)
