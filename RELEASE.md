# PyPI release checklist — django-admin-branding-fdg

## Before publishing

- [ ] Verify ownership of the package name on PyPI (a missing project page does not guarantee availability).
- [ ] Create the public GitHub repository `huachenlihx/django-admin-branding-fdg` on the `main` branch and verify the README and metadata links.
- [ ] Review metadata, license, README, package contents, and version 0.1.0.
- [ ] Run the Django tests on supported Python/Django pairs (5.2 on Python 3.10-3.14, 6.0/6.1 on Python 3.12-3.14, subject to each Django patch release's supported Python versions).
- [ ] Validate the package in a real Django project with `DEBUG=False`, `collectstatic`, and any custom staticfiles backend you intend to support.
- [ ] Run all commands below and verify that every command succeeds.

## Recommended commands (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip 'setuptools>=77' build twine
python -m pip install -e .
python -m django test --settings=tests.settings
rm -rf dist build src/*.egg-info
python -m build
python -m twine check dist/*
```

Inspect `dist/` and confirm there are exactly two intended files for version 0.1.0.
If you run into `ModuleNotFoundError: No module named 'django'`, install the
compatible Django version and rerun the tests.

## TestPyPI (optional)

```bash
python -m twine upload --repository testpypi dist/*
```

TestPyPI is a separate index and account. Dependencies may need to resolve from
regular PyPI when testing installation, so use a clean virtual environment and
`--extra-index-url https://pypi.org/simple/` carefully.

## Production upload

```bash
python -m twine upload dist/*
```

Alternatively configure PyPI Trusted Publishing in your GitHub Actions workflow.
Do not commit or share any PyPI API token. PyPI uploaded release files cannot
be replaced in place: bump the version if you need to upload a corrected file.
