import json
import os

from app.lib.util import strtobool
from redis import Redis


class Features:
    pass


class Production(Features):
    ENVIRONMENT_NAME: str = os.environ.get("ENVIRONMENT_NAME", "production")
    CONTAINER_IMAGE: str = os.environ.get("CONTAINER_IMAGE", "")
    BUILD_VERSION: str = os.environ.get("BUILD_VERSION", "")
    TNA_FRONTEND_VERSION: str = ""
    try:
        with open(
            os.path.join(
                os.path.realpath(os.path.dirname(__file__)),
                "node_modules/@nationalarchives/frontend",
                "package.json",
            )
        ) as package_json:
            try:
                data = json.load(package_json)
                TNA_FRONTEND_VERSION = data["version"] or ""
            except ValueError:
                pass
    except FileNotFoundError:
        pass

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")

    DEBUG: bool = False

    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_SAMPLE_RATE: float = float(os.getenv("SENTRY_SAMPLE_RATE", "0.1"))

    SERVICE_URL_PREFIX: str = "/request-a-military-service-record"

    COOKIE_DOMAIN: str = os.environ.get("COOKIE_DOMAIN", "")

    CSP_IMG_SRC: list[str] = os.environ.get("CSP_IMG_SRC", "'self'").split(",")
    CSP_SCRIPT_SRC: list[str] = os.environ.get("CSP_SCRIPT_SRC", "'self'").split(",")
    CSP_STYLE_SRC: list[str] = os.environ.get("CSP_STYLE_SRC", "'self'").split(",")
    CSP_FONT_SRC: list[str] = os.environ.get("CSP_FONT_SRC", "'self'").split(",")
    CSP_CONNECT_SRC: list[str] = os.environ.get("CSP_CONNECT_SRC", "'self'").split(",")
    CSP_MEDIA_SRC: list[str] = os.environ.get("CSP_MEDIA_SRC", "'self'").split(",")
    CSP_WORKER_SRC: list[str] = os.environ.get("CSP_WORKER_SRC", "'self'").split(",")
    CSP_FRAME_SRC: list[str] = os.environ.get("CSP_FRAME_SRC", "'self'").split(",")
    CSP_REPORT_URL: str = os.environ.get("CSP_REPORT_URL", "")
    if CSP_REPORT_URL:
        CSP_REPORT_URL += f"&sentry_release={BUILD_VERSION}" if BUILD_VERSION else ""
    FORCE_HTTPS: bool = strtobool(os.getenv("FORCE_HTTPS", "False"))

    CACHE_TYPE: str = "FileSystemCache"
    CACHE_DEFAULT_TIMEOUT: int = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "300"))
    CACHE_IGNORE_ERRORS: bool = True
    CACHE_DIR: str = os.environ.get("CACHE_DIR", "/tmp")
    CACHE_REDIS_URL: str = os.environ.get("CACHE_REDIS_URL", "")

    GA4_ID: str = os.environ.get("GA4_ID", "")

    GOV_UK_PAY_API_KEY: str = os.environ.get("GOV_UK_PAY_API_KEY", "")
    GOV_UK_PAY_API_URL: str = os.environ.get("GOV_UK_PAY_API_URL", "")
    GOV_UK_PAY_SIGNING_SECRET: str = os.environ.get("GOV_UK_PAY_SIGNING_SECRET", "")

    SQLALCHEMY_DATABASE_URI: str = os.environ.get("SQLALCHEMY_DATABASE_URI", "")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = strtobool(
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "False")
    )

    SESSION_COOKIE_NAME: str = "ds_request_service_record_session"
    SESSION_COOKIE_DOMAIN: str = COOKIE_DOMAIN
    SESSION_COOKIE_PATH: str = SERVICE_URL_PREFIX
    SESSION_COOKIE_SECURE: bool = True
    SESSION_REDIS_URL: str = os.environ.get("SESSION_REDIS_URL", "")
    if SESSION_REDIS_URL:
        SESSION_TYPE: str = "redis"
        SESSION_REDIS = Redis.from_url(SESSION_REDIS_URL)

    AWS_DEFAULT_REGION: str = os.environ.get("AWS_DEFAULT_REGION", "eu-west-2")
    PROOF_OF_DEATH_BUCKET_NAME: str = os.environ.get("PROOF_OF_DEATH_BUCKET_NAME", "")
    MAX_UPLOAD_ATTEMPTS: int = int(os.environ.get("MAX_UPLOAD_ATTEMPTS", "3"))

    EMAIL_FROM: str = os.environ.get("EMAIL_FROM", "")
    EMAIL_FROM_NAME: str = os.environ.get("EMAIL_FROM_NAME", "")
    DYNAMICS_INBOX: str = os.environ.get("DYNAMICS_INBOX", "")

    DELIVERY_FEE_API_URL: str = (
        os.environ.get("RECORD_COPYING_SERVICE_API_URL", "") + "GetDeliveryPrice"
    )
    COUNTRY_API_URL: str = (
        os.environ.get("RECORD_COPYING_SERVICE_API_URL", "") + "GetCountry"
    )
    MOD_COPYING_API_URL: str = os.environ.get("MOD_COPYING_API_URL", "")


class Staging(Production):
    DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))

    SENTRY_SAMPLE_RATE: float = float(os.getenv("SENTRY_SAMPLE_RATE", "1"))

    CACHE_DEFAULT_TIMEOUT: int = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "60"))


class Develop(Production):
    DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))

    SENTRY_SAMPLE_RATE: float = float(os.getenv("SENTRY_SAMPLE_RATE", "0"))

    CACHE_DEFAULT_TIMEOUT: int = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "1"))

    SESSION_COOKIE_SECURE: bool = strtobool(os.getenv("SESSION_COOKIE_SECURE", "True"))


class Test(Production):
    ENVIRONMENT_NAME = "test"

    SECRET_KEY: str = "abc123"
    DEBUG: bool = True
    TESTING: bool = True
    EXPLAIN_TEMPLATE_LOADING: bool = True

    SENTRY_DSN: str = ""
    SENTRY_SAMPLE_RATE: float = 0

    CACHE_TYPE: str = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT: int = 1

    FORCE_HTTPS: bool = False
    PREFERRED_URL_SCHEME: str = "http"

    COUNTRY_API_URL: str = (
        os.environ.get(
            "RECORD_COPYING_SERVICE_API_URL",
            "http://mock-record-copying-service-api:8080/",
        )
    ) + "GetCountry"
    DELIVERY_FEE_API_URL: str = (
        os.environ.get(
            "RECORD_COPYING_SERVICE_API_URL",
            "http://mock-record-copying-service-api:8080/",
        )
    ) + "GetDeliveryPrice"
