from django.contrib.auth import get_user_model

User = get_user_model()

def email_authenticate(email, password):
    try:
        user = User.objects.get(email=email)  # Email se user find karein
        if user.check_password(password):  # Password verify karein
            return user
    except User.DoesNotExist:
        return None
    return None
