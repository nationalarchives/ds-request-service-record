# TNA Python Flask Application

## Quickstart

```sh
# Build and start the container
docker compose up -d
```

### Add the static assets

During the first time install, your `app/static/assets` directory will be empty.

As you mount the project directory to the `/app` volume, the static assets from TNA Frontend installed inside the container will be "overwritten" by your empty directory.

To add back in the static assets, run:

```sh
docker compose exec app cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets /app/app/static
```

### Run tests

```sh
docker compose exec app poetry run python -m pytest
```

### Format and lint code

```sh
docker compose exec app format
```

### Run WireMock server for local development

For local development, you can use a mock server instead of connecting to external APIs.

The server will run on `http://localhost:65519` and is visible to your app on `http://mock-record-copying-service-api:8080/`. Set this in your `.env`:

```
RECORD_COPYING_SERVICE_API_URL=http://mock-record-copying-service-api:8080/
```

## Environment variables

In addition to the [base Docker image variables](https://github.com/nationalarchives/docker/blob/main/docker/tna-python/README.md#environment-variables), this application has support for:

| Variable                         | Purpose                                                                                          | Default                                                   |
| -------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| `CONFIG`                         | The configuration to use                                                                         | `config.Production`                                       |
| `DEBUG`                          | If true, allow debugging[^1]                                                                     | `False`                                                   |
| `SENTRY_DSN`                     | The Sentry DSN (project code)                                                                    | _none_                                                    |
| `SENTRY_JS_ID`                   | The ID of the Sentry client project to catch issues                                              | _none_                                                    |
| `SENTRY_SAMPLE_RATE`             | How often to sample traces and profiles (0-1.0)                                                  | production: `0.1`, staging: `1`, develop: `0`             |
| `COOKIE_DOMAIN`                  | The domain to save cookie preferences against                                                    | _none_                                                    |
| `CSP_IMG_SRC`                    | A comma separated list of CSP rules for `img-src`                                                | `'self'`                                                  |
| `CSP_SCRIPT_SRC`                 | A comma separated list of CSP rules for `script-src`                                             | `'self'`                                                  |
| `CSP_STYLE_SRC`                  | A comma separated list of CSP rules for `style-src`                                              | `'self'`                                                  |
| `CSP_FONT_SRC`                   | A comma separated list of CSP rules for `font-src`                                               | `'self'`                                                  |
| `CSP_CONNECT_SRC`                | A comma separated list of CSP rules for `connect-src`                                            | `'self'`                                                  |
| `CSP_MEDIA_SRC`                  | A comma separated list of CSP rules for `media-src`                                              | `'self'`                                                  |
| `CSP_WORKER_SRC`                 | A comma separated list of CSP rules for `worker-src`                                             | `'self'`                                                  |
| `CSP_FRAME_SRC`                  | A comma separated list of CSP rules for `frame-src`                                              | `'self'`                                                  |
| `CSP_FEATURE_FULLSCREEN`         | A comma separated list of rules for the `fullscreen` feature policy                              | `'self'`                                                  |
| `CSP_FEATURE_PICTURE_IN_PICTURE` | A comma separated list of rules for the `picture-in-picture` feature policy                      | `'self'`                                                  |
| `FORCE_HTTPS`                    | Redirect requests to HTTPS as part of the CSP                                                    | _none_                                                    |
| `CACHE_TYPE`                     | https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching                        | _none_                                                    |
| `CACHE_DEFAULT_TIMEOUT`          | The number of seconds to cache pages for                                                         | production: `300`, staging: `60`, develop: `0`, test: `0` |
| `CACHE_DIR`                      | Directory for storing cached responses when using `FileSystemCache`                              | `/tmp`                                                    |
| `CACHE_REDIS_URL`                | The connection string for Redis when using `CACHE_TYPE=RedisCache`                               | _none_                                                    |
| `GA4_ID`                         | The Google Analytics 4 ID                                                                        | _none_                                                    |
| `GOV_UK_PAY_API_KEY`             | GOV.UK Pay API key                                                                               | _none_ (required for payments)                            |
| `GOV_UK_PAY_API_URL`             | GOV.UK Pay create payment endpoint URL                                                           | _none_ (required for payments)                            |
| `SQLALCHEMY_DATABASE_URI`        | SQLAlchemy database connection string                                                            | _none_ (required)                                         |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | SQLAlchemy event system toggle                                                                   | `False`                                                   |
| `SESSION_REDIS_URL`              | Redis URL connection string for sessions                                                         | _none_                                                    |
| `AWS_DEFAULT_REGION`             | AWS region for clients (SES/S3)                                                                  | `eu-west-2`                                               |
| `PROOF_OF_DEATH_BUCKET_NAME`     | S3 bucket location for uploaded proof-of-death files                                             | _none_ (required for file uploads)                        |
| `MAX_UPLOAD_ATTEMPTS`            | Number of retry attempts for S3 uploads                                                          | `3`                                                       |
| `EMAIL_FROM`                     | The address which SES will send emails from                                                      | _none_                                                    |
| `DYNAMICS_INBOX`                 | The address which SES will send Dynamics emails to                                               | _none_                                                    |
| `RECORD_COPYING_SERVICE_API_URL` | The URL of the Record Copying Service API                                                        |                                                           |
| `MOD_COPYING_API_URL`            | The URL of the MOD Record Copying Service API, which receives notification of the second payment |                                                           |

[^1] [Debugging in Flask](https://flask.palletsprojects.com/en/2.3.x/debugging/)
