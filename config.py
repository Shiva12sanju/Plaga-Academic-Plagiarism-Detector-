import os


class Config:

    # =====================================
    # BASIC CONFIG
    # =====================================

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

    INSTANCE_DIR = os.path.join(
        BASE_DIR,
        "instance"
    )


    os.makedirs(
        INSTANCE_DIR,
        exist_ok=True
    )


    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        +
        os.path.join(
            INSTANCE_DIR,
            "plagiarism.db"
        )
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
# PRODUCTION CONFIG (Render)
# =====================================

class ProductionConfig(Config):

    DEBUG = False


    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "production-secret-key"
    )


    # Render SQLite location
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:////tmp/plagiarism.db"
    )




# =====================================
# CONFIG MAP
# =====================================

config = {

    "development": DevelopmentConfig,

    "production": ProductionConfig,

    "default": DevelopmentConfig

}