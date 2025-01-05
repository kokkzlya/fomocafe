import os

_ = os.getenv

class Config:
    DEBUG = _("DEBUG", True)
    PORT = _("PORT", 5000)
    SECRET_KEY = _("SECRET_KEY", "changepls")
