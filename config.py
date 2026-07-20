import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )


    # =====================================
    # DATABASE CONFIGURATION
    # =====================================

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:////tmp/plagiarism.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False



    # =====================================
    # UPLOAD CONFIGURATION
    # =====================================

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )


    ALLOWED_EXTENSIONS = {
        "txt",
        "pdf",
        "docx"
    }


    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )



    # =====================================
    # REPORT CONFIGURATION
    # =====================================

    REPORTS_FOLDER = os.path.join(
        BASE_DIR,
        "reports",
        "plagiarism_reports"
    )



    # =====================================
    # ADMIN CONFIGURATION
    # =====================================

    ADMIN_SECRET_KEY = "SHIVU@2026"



# =====================================
# DEVELOPMENT CONFIG
# =====================================

class DevelopmentConfig(Config):

    DEBUG = True



# =====================================
# PRODUCTION CONFIG
# =====================================

class ProductionConfig(Config):

    DEBUG = False

    SECRET_KEY = os.environ.get(
        "SECRET_KEY"
    )



# =====================================
# CONFIG MAP
# =====================================

config = {

    "development": DevelopmentConfig,

    "production": ProductionConfig,

    "default": DevelopmentConfig

}