import os


def get_bool_from_string(string: str):
    return string.lower() in ("true", "1")


class AppSettings:
    # General
    APP_VERSION: str = os.getenv("APP_VERSION", "0.0.0")

    # Firebase config
    FIRESTORE_JSON_CONFIG: str = os.getenv("FIRESTORE_JSON_CONFIG", "")

    # Openai config
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MOCK_RESPONSES: str = os.getenv("OPENAI_MOCK_RESPONSES", "false")
    OPENAI_MODEL_ABILITY: int = 1

    # Clerk config
    CLERK_JWT_PEM_KEY: str = os.getenv("CLERK_JWT_PEM_KEY", "").replace(r"\n", "\n")
    CLERK_TOKEN_LEEWAY: int = 300
    CLERK_USER_WEBHOOK_SECRET: str = os.getenv("CLERK_USER_WEBHOOK_SECRET", "")
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")

    DEFAULT_PAGE_LIMIT: int = 20

    LOCAL_TESTING: bool = get_bool_from_string(os.getenv("LOCAL_TESTING", "true"))
    ENABLED_KAFKA_EVENTS: bool = get_bool_from_string(
        os.getenv("ENABLED_KAFKA_EVENTS", "false")
    )

    # Algolia config
    ALGOLA_APP_ID: str = os.getenv("ALGOLA_APP_ID", "")
    ALGOLIA_API_KEY: str = os.getenv("ALGOLIA_API_KEY", "")

    # Kafka config
    KAFKA_BOOTSTRAP_SERVER: str = os.getenv("KAFKA_BOOTSTRAP_SERVER", "")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME", "")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD", "")
    KAFKA_JWT_SECRET: str = os.getenv("KAFKA_JWT_SECRET", "")

    # Sendgrid config
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    SENDGRID_FROM_EMAIL: str = os.getenv("SENDGRID_FROM_EMAIL", "")

    # Sentry config
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_TRACES_RATE: float = 1.0

    class Config:
        env_file = ".env"


SETTINGS = AppSettings()  # type: ignore
