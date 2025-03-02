from django.core.mail import send_mail

def send_otp_email(user):
    subject = "Your OTP Code"
    message = f"Hello {user.username},\n\nYour OTP code is: {user.otp_code}\n\nUse this code to verify your account."
    send_mail(subject, message, "sreejith.s.official9@gmail.com", [user.email])


