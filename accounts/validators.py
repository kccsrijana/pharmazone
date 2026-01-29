from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class EmailValidator:
    """Simple email validation without complex verification"""
    
    @staticmethod
    def validate_basic_format(email):
        """Basic email format validation"""
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
    
    @staticmethod
    def validate_simple(email):
        """Simple email validation for forms"""
        errors = []
        
        # Basic format check
        if not EmailValidator.validate_basic_format(email):
            errors.append("Please enter a valid email address.")
            return {'is_valid': False, 'errors': errors}
        
        # Check for common issues
        if '..' in email:
            errors.append("Email cannot contain consecutive dots.")
        
        if email.startswith('.') or email.endswith('.'):
            errors.append("Email cannot start or end with a dot.")
        
        # Check length
        if len(email) > 254:
            errors.append("Email address is too long.")
        
        # Simple domain check
        if '@' in email:
            local, domain = email.rsplit('@', 1)
            if len(local) > 64:
                errors.append("Email username part is too long.")
            if not domain or '.' not in domain:
                errors.append("Please enter a valid email domain.")
        
        is_valid = len(errors) == 0
        return {
            'is_valid': is_valid,
            'errors': errors
        }