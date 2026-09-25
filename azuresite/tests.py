import os
import secrets
import subprocess
import sys
import textwrap
from pathlib import Path
from unittest import TestCase


class ConfigurationTests(TestCase):
    def run_python(self, code, **overrides):
        environment = {
            **os.environ,
            'PYTHONOPTIMIZE': '0',
            'DJANGO_ENV': 'development',
            'DJANGO_SETTINGS_MODULE': 'azuresite.production',
            'DJANGO_SECRET_KEY': secrets.token_urlsafe(64),
            'AZURE_POSTGRESQL_NAME': 'configuration_tests',
            'AZURE_POSTGRESQL_HOST': 'localhost',
            'AZURE_POSTGRESQL_USER': 'configuration_tests',
            'AZURE_POSTGRESQL_PASSWORD': secrets.token_urlsafe(32),
            'WEBSITE_SITE_NAME': 'configuration-tests',
        }
        for name, value in overrides.items():
            if value is None:
                environment.pop(name, None)
            else:
                environment[name] = value
        return subprocess.run(
            [sys.executable, '-c', textwrap.dedent(code)],
            cwd=str(Path(__file__).resolve().parent.parent), env=environment,
            capture_output=True, text=True, timeout=30,
        )

    def test_missing_or_blank_secret_prevents_startup(self):
        for module in ('azuresite.settings', 'azuresite.production'):
            for value in (None, '', ' \t\r\n'):
                with self.subTest(module=module, value=value):
                    result = self.run_python(
                        'import ' + module, DJANGO_SECRET_KEY=value,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('ImproperlyConfigured', result.stderr)
                    self.assertIn('DJANGO_SECRET_KEY must be configured', result.stderr)

    def test_production_uses_supplied_key_and_disables_debugging(self):
        result = self.run_python("""
            import os
            from azuresite import settings, production
            assert settings.SECRET_KEY == os.environ['DJANGO_SECRET_KEY']
            assert production.SECRET_KEY == settings.SECRET_KEY
            assert production.DEBUG is False
        """)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_production_error_responses_hide_debug_details(self):
        result = self.run_python("""
            import logging
            import os
            from django.conf import settings
            from django.core.wsgi import get_wsgi_application
            from django.test import RequestFactory, override_settings
            from django.urls import path

            get_wsgi_application()
            assert settings.DEBUG is False
            logging.disable(logging.CRITICAL)
            marker = os.environ['DJANGO_SECRET_KEY']

            def error_view(request):
                private_value = marker
                raise RuntimeError('intentional-response-test-error')

            urlpatterns = [path('security-error/', error_view)]
            for debug_control in (False, True):
                with override_settings(ROOT_URLCONF=__name__, DEBUG=debug_control):
                    application = get_wsgi_application()
                    for target, status, detail in (
                        ('/unknown-route/', 404, 'security-error/'),
                        ('/security-error/', 500, marker),
                    ):
                        request = RequestFactory().get(
                            target, HTTP_HOST='configuration-tests.azurewebsites.net',
                        )
                        response = application.get_response(request)
                        assert response.status_code == status
                        assert (detail in response.content.decode('utf-8')) == debug_control
        """)
        self.assertEqual(result.returncode, 0, result.stderr)
