"""Exercise deployment environment migration without running the deploy shell."""

import ast
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
DEPLOY = (ROOT / "scripts/deploy.sh").read_text()
ENV_SETUP = DEPLOY.split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]


class DeploymentEnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.env_dir = Path(self.directory.name)
        self.frontend = (
            "# Keep unrelated settings\n"
            "VITE_BACKEND_URL=https://pay-per.me/\n"
            "VITE_FRONTEND_URL=https://pay-per.me/\n"
            "VITE_MEDIA_URL=https://pay-per.me\n"
            "VITE_CUSTOM_FEATURE=enabled\n"
        )
        self.backend = (
            "SECRET_KEY='test-only-secret$#with-symbols'\n"
            "DB_PASSWORD=test-only-database-password\n"
            "EMAIL_HOST_PASSWORD=test-only-smtp-password\n"
            'ALLOWED_HOSTS="localhost  pay-per.me www.pay-per.me custom.example"\n'
            "CORS_ALLOWED_ORIGINS='https://pay-per.me https://custom.example'\n"
            "CSRF_TRUSTED_ORIGINS=https://pay-per.me\n"
            "STATIC_URL=https://pay-per.me/static/\n"
        )
        self.database = "POSTGRES_PASSWORD=test-only-database-password\n"
        for name, value in (
            ("frontend_env", self.frontend),
            ("backend_env", self.backend),
            ("database_env", self.database),
        ):
            (self.env_dir / name).write_text(value)

    def run_setup(self, timestamp="test"):
        return subprocess.run(
            [sys.executable, "-", str(self.env_dir), timestamp],
            input=ENV_SETUP,
            text=True,
            capture_output=True,
        )

    def test_updates_urls_and_preserves_credentials_and_custom_domains(self):
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        frontend = (self.env_dir / "frontend_env").read_text()
        backend = (self.env_dir / "backend_env").read_text()
        self.assertIn("STATIC_URL=/static/\n", backend)
        self.assertNotIn("https://pay-per.me/static/", backend)
        for entry in (
            "VITE_BACKEND_URL=/\n",
            "VITE_PUBLIC_URL=/\n",
            "VITE_FRONTEND_URL=https://pay-per.in/\n",
            "VITE_MEDIA_URL=https://pay-per.in\n",
            "VITE_CUSTOM_FEATURE=enabled\n",
        ):
            self.assertIn(entry, frontend)
        for line in self.backend.splitlines(keepends=True)[:3]:
            self.assertIn(line, backend)
        self.assertIn(
            "ALLOWED_HOSTS=localhost pay-per.me www.pay-per.me custom.example "
            "pay-per.in www.pay-per.in\n", backend
        )
        self.assertIn(
            "CORS_ALLOWED_ORIGINS=https://pay-per.me https://custom.example "
            "https://pay-per.in https://www.pay-per.in\n", backend
        )
        self.assertEqual((self.env_dir / "database_env").read_text(), self.database)
        backup = self.env_dir / "before-domain-update-test"
        self.assertEqual(backup.stat().st_mode & 0o777, 0o700)
        self.assertEqual((backup / "frontend_env").read_text(), self.frontend)
        self.assertEqual((backup / "backend_env").read_text(), self.backend)
        self.assertNotIn("test-only-secret", result.stdout + result.stderr)

    def test_repeated_run_is_idempotent(self):
        self.assertEqual(self.run_setup().returncode, 0)
        before = {p.name: p.read_bytes() for p in self.env_dir.glob("*_env")}
        result = self.run_setup("second")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            before, {p.name: p.read_bytes() for p in self.env_dir.glob("*_env")}
        )
        self.assertFalse((self.env_dir / "before-domain-update-second").exists())

    def test_missing_saved_file_does_not_modify_other_files(self):
        (self.env_dir / "database_env").unlink()
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.env_dir / "frontend_env").read_text(), self.frontend)
        self.assertEqual((self.env_dir / "backend_env").read_text(), self.backend)

    def test_duplicate_backend_entry_does_not_partially_update_frontend(self):
        backend = self.backend + "ALLOWED_HOSTS=duplicate.example\n"
        (self.env_dir / "backend_env").write_text(backend)
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Duplicate production environment entry", result.stderr)
        self.assertEqual((self.env_dir / "frontend_env").read_text(), self.frontend)
        self.assertEqual((self.env_dir / "backend_env").read_text(), backend)

    def test_missing_keys_are_added_even_without_final_newline(self):
        (self.env_dir / "frontend_env").write_text("CUSTOM_FRONTEND=keep")
        (self.env_dir / "backend_env").write_text("CUSTOM_BACKEND=keep")
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "CUSTOM_FRONTEND=keep\nVITE_BACKEND_URL=/\n",
            (self.env_dir / "frontend_env").read_text(),
        )
        self.assertIn(
            "CUSTOM_BACKEND=keep\nALLOWED_HOSTS=pay-per.in www.pay-per.in\n",
            (self.env_dir / "backend_env").read_text(),
        )
        self.assertIn(
            "STATIC_URL=/static/\n",
            (self.env_dir / "backend_env").read_text(),
        )

    def test_quoted_empty_and_commented_values(self):
        (self.env_dir / "backend_env").write_text(
            "export ALLOWED_HOSTS='localhost\tpay-per.in' # keep localhost\n"
            'CORS_ALLOWED_ORIGINS=""\n'
            "CSRF_TRUSTED_ORIGINS=   # no configured origins\n"
        )
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        backend = (self.env_dir / "backend_env").read_text()
        self.assertIn("ALLOWED_HOSTS=localhost pay-per.in www.pay-per.in\n", backend)
        self.assertIn(
            "CSRF_TRUSTED_ORIGINS=https://pay-per.in https://www.pay-per.in\n",
            backend,
        )


class DomainSettingsTests(unittest.TestCase):
    def test_domain_lists_handle_missing_empty_and_mixed_whitespace(self):
        keys = {"ALLOWED_HOSTS", "CORS_ALLOWED_ORIGINS", "CSRF_TRUSTED_ORIGINS"}
        tree = ast.parse(
            (ROOT / "backend/payroll_system/payroll_system/settings.py").read_text()
        )
        assignments = [
            node for node in tree.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id in keys
                    for target in node.targets)
        ]
        code = compile(ast.Module(body=assignments, type_ignores=[]), "settings", "exec")
        self.assertEqual(len(assignments), 3)
        for value, expected in (
            (None, []),
            ("", []),
            ("  one\t two\nthree  ", ["one", "two", "three"]),
        ):
            with self.subTest(value=value):
                environment = {} if value is None else {key: value for key in keys}
                with patch.dict(os.environ, environment, clear=True):
                    namespace = {"os": os}
                    exec(code, namespace)
                for key in keys:
                    self.assertEqual(namespace[key], expected)


if __name__ == "__main__":
    unittest.main()
