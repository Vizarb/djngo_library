import logging
from functools import wraps
from django.utils.timezone import now, timedelta
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import LoginAttempt

# Create a custom logger for user login attempts
logger = logging.getLogger('user_login')

def track_failed_login_attempts(view_func):
    """
    Decorator to track failed login attempts and block the user after 3 consecutive failed attempts.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        username = request.POST.get('username')  # Assuming username is passed via POST
        password = request.POST.get('password')  # Assuming password is passed via POST

        user = User.objects.filter(username=username).first()
        
        if user:
            # Check if the user is blocked
            if user.is_blocked:
                logger.warning(f"Blocked user '{username}' attempted to log in.")
                return HttpResponse("Your account is blocked.", status=403)
            
            # Authenticate the user
            user_authenticated = authenticate(request, username=username, password=password)
            
            if not user_authenticated:
                # Create a failed login attempt
                LoginAttempt.objects.create(user=user, success=False)

                # Get the count of failed attempts in the last 30 minutes
                failed_attempts = LoginAttempt.objects.filter(
                    user=user,
                    success=False,
                    attempt_time__gt=now() - timedelta(minutes=30)
                ).count()
                
                logger.info(f"Failed login attempt for '{username}', total failed attempts: {failed_attempts}")

                # If there are 3 failed attempts, block the user and log as critical
                if failed_attempts >= 3:
                    user.is_blocked = True
                    user.save()
                    logger.critical(f"User '{username}' failed 3 consecutive login attempts and is blocked.")
                    return HttpResponse("Your account has been blocked due to multiple failed login attempts.", status=403)

        # Proceed to the original view function if not blocked
        return view_func(request, *args, **kwargs)

    return _wrapped_view
