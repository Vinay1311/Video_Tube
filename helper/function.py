""" External Imports """
from rest_framework_simplejwt.tokens import RefreshToken

""" Internal Imports """


# ------------ Token Functions  --------------- #

def get_tokens_for_user(user_obj):
        """
        To get tokens by mobile number
        params mobile: mobile of user 
        result: object
        """
        refresh = RefreshToken.for_user(user_obj)

        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }


# ------------ Response Functions  --------------- #

class ResponseHandling:
    def failure_response_message(detail,result):
        """
        error message for failure
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'detail' : detail, 'result' : result, 'success' : False}

    def success_response_message(detail,result):
        """
        success message for Success
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'detail' : detail, 'result' : result, 'success' : True}

# ------------------- Error Message ------------------- #

def error_message_function(errors):
    """
    return error message when serializer is not valid
    :param errors: error object
    :returns: string
    """
    for key, values in errors.items():
        error = [value[:] for value in values]
        err = ' '.join(map(str,error))
        return err
    
# ------------------- Generate the Unique Login link --------------------- #
def generate_unique_login_link(username):
     """
     return a unique link for the login page after register
     :returns: string
     """
     return f'http://YT_Project/user={username}/login_page'