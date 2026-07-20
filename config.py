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

    INSTANCE_DIR = os.path.join(
        BASE_DIR,
        "instance"
    )

    # Create instance folder automatically
    os.makedirs(
        INSTANCE_DIR,
        exist_ok=True
    )


    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(
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