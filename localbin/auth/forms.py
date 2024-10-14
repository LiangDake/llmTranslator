from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, equal_to

USERNAME_EMPTY_MSG = "用户名不能为空！"
PASSWORD_FIELD_EMPTY_MSG = "密码不能为空！"
MIN_MAX_LENGHT_MSG = "请设置5至15个字符！"

class UserFormLogin(FlaskForm):
    """
    Form for login page
    """
    username = StringField("Username", validators=[DataRequired(message=USERNAME_EMPTY_MSG), Length(min=5, max=15, message=MIN_MAX_LENGHT_MSG)])
    password = PasswordField("Password", validators=[DataRequired(message=PASSWORD_FIELD_EMPTY_MSG)])
    login_btn = SubmitField("Login")

class UserFormRegister(FlaskForm):
    """
    Form for registering
    For now i have not set required lenght for password nor any special chars
    """
    username = StringField("Username", validators=[DataRequired(USERNAME_EMPTY_MSG), Length(min=5, max=15, message=MIN_MAX_LENGHT_MSG)])
    password = PasswordField("Password", validators=[DataRequired(message=PASSWORD_FIELD_EMPTY_MSG)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(message=PASSWORD_FIELD_EMPTY_MSG), EqualTo("password", message="密码不匹配!")])
    register_btn = SubmitField("Register")

# TODO
# Reset password form