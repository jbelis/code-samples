from dataclasses import dataclass
from typing import Dict
from abc import ABC, abstractmethod


@dataclass
class User:
    id: str
    name: str
    contact: str
    notification_method: str
    


class Notifier(ABC):
    @abstractmethod
    def send_message(self, address: str, message: str) -> bool:
        """
        Send notification message
        
        :param address: address to send message to
        :param message: Message to send
        :return: Whether message was sent successfully
        """
        pass
    

class EmailNotifier(Notifier):
    def send_message(self, address: str, message: str) -> bool:
        """
        Send notification via email
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            # Use configuration from environment or secure config
            smtp_config = {
                'host': 'smtp.gmail.com',
                'port': 587,
                'username': 'your-email@example.com',
                'password': 'secure-password'
            }
            
            msg = MIMEText(message)
            msg['Subject'] = "Notification"
            msg['From'] = smtp_config['username']
            msg['To'] = address
            
            with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
                server.starttls()
                server.login(smtp_config['username'], smtp_config['password'])
                server.sendmail(smtp_config['username'], address, msg.as_string())
            
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False


class SMSNotifier(Notifier):
    def send_message(self, address: str, message: str) -> bool:
        """
        Send notification using an SMS service
        """
        try:
            import requests
            
            # Use configuration from environment or secure config
            sms_config = {
                'api_url': 'https://sms-gateway.com/send',
                'api_key': 'your-sms-api-key'
            }
            
            response = requests.post(sms_config['api_url'], json={
                'phone': address,
                'message': message,
                'api_key': sms_config['api_key']
            })
            
            return response.status_code == 200
        except Exception as e:
            print(f"SMS sending failed: {e}")
            return False




class UserNotificationService:
    def __init__(self, notification_services: Dict[str, Notifier]):
        """
        Dependency Injection of notification services
        
        :param notification_services: A dictionary of notification methods
        """
        self._notification_services = notification_services
    
    def notify_user(self, user: User, message: str) -> bool:
        """
        Send notification using appropriate service
        
        :param user: User to notify
        :param message: Message to send
        :return: Whether notification was successful
        """
        try:
            notification_service = self._notification_services.get(user.notification_method)
            if not notification_service:
                raise ValueError(f"No notification service for method: {user.notification_method}")
            
            return notification_service.send_message(user.contact, message)
        except Exception as e:
            print(f"Notification failed: {e}")
            return False
        