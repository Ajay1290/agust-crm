from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from manager.libs.MultiTenantSQLAlchemy import MultiTenantSQLAlchemy

csrf = CSRFProtect()
db = SQLAlchemy()
dbt = MultiTenantSQLAlchemy()
login_manager = LoginManager()
mail = Mail()
