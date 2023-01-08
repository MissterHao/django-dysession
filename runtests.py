"""
This code provides a mechanism for running django_ses' internal
test suite without having a full Django project.  It sets up the
global configuration, then dispatches out to `call_command` to
kick off the test suite.
## The Code
"""

# Setup and configure the minimal settings necessary to
# run the test suite.  Note that Django requires that the
# `DATABASES` value be present and configured in order to
# do anything.

from argparse import ArgumentParser

import django
from django.conf import settings
from django.core.management import call_command

if __name__ == "__main__":

    # Run test args parse
    parser = ArgumentParser()
    parser.add_argument(
        "-v", "--verbosity", action="count", help="increase output verbosity", default=0
    )
    args = parser.parse_args()

    # Django Setup
    settings.configure(
        INSTALLED_APPS=[
            "dysession",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        MIDDLEWARE_CLASSES=(
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
        ),
        SECRET_KEY="not-secret",
    )

    django.setup()
    # Start the test suite now that the settings are configured.
    call_command("test", "tests", verbosity=args.verbosity)
