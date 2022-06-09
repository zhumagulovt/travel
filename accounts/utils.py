from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_email(self, title, message, sender, receiver):
        send_mail()