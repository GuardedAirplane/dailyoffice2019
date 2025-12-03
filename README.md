# Daily Office, Book of Common Prayer 2019 (https://www.dailyoffice2019.com)

This project is used to build the website https://www.dailyoffice2019.com. It is a Django application written in
Python (to be installed in a development environment). It is used to produce a static html and javascript site which
can then be deployed to the production environment.

## WHAT IS THE SITE FOR?

The site invites you to join with Christians around the world in praying with the Church, at any time or in any place
you may find yourself. It makes it easy to pray daily morning, midday, evening, and compline (bedtime) prayer without
flipping pages, searching for scripture readings or calendars, or interpreting rubrics. The prayers are presented from
The Book of Common Prayer (2019) of the Anglican Church in North America and reflect the ancient patterns of daily
prayer Christians have used since the earliest days of the church.

## WHAT IS THE DAILY OFFICE?

Daily Morning Prayer and Daily Evening Prayer are the established rites (offices) by which, both corporately and
individually, God’s people annually encounter the whole of the Holy Scriptures, daily confess their sins and praise
Almighty God, and offer timely thanksgivings, petitions, and intercessions.

## Contributing

Pull requests are welcome. Take a look at the Github [issues](https://github.com/blocher/dailyoffice2019/issues) and
see where you might help out. Updates to documentation and tests (both of which are largely missing) are also welcome.

### Requirements

- Python 3.12
- Node 16
- PostgreSQL
- Memcached 1.6

The project is known to work with these versions, although it may also work with more recent versions.

### Setting up a development environment

If you are using macOS, all the above requirements may be installed with Homebrew.

#### Initial project setup

- Clone or fork the project from `https://github.com/blocher/dailyoffice2019`
- `cd dailyoffice2019`
- `cp app/.env.development app/.env.local`
- `cp site/website/.env.example site/website/.env`

#### Import database

- Connect to Postgres `psql -d postgres`
- Create database `create database dailyoffice;`
- Create user `create user dailyoffice with password 'password';`
- Grant permissions `grant all privileges on database dailyoffice to dailyoffice;`
- Exit postgres `\q`
- Import `unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | psql -U dailyoffice dailyoffice`

#### Setup up python environment

- Go to the project's `/site` directory
- Create a Python virtual environment `python3 -m venv env`
- Load virtual environment `source env/bin/activate`
- Install Python Requirements `pip install -r requirements.txt`

#### Run API server (in separate terminal)

- Collect static assets `python manage.py collectstatic`
- Start development server `python manage.py runsslserver`
- The API documentation will be accessible locally at `https://127.0.0.1:8000/api/`

#### Run the client (frontend) server

- Go to the project's `/app` directory
- Follow the setup instructions in the client README: [app/README.md](app/README.md)
- The frontend will be accessible locally at `http://127.0.0.1:8080`

#### Run everything with Podman Compose

- Install Podman and `podman-compose` (tested with Podman 5.6.2 / podman-compose 1.5.0)
- From the repository root run `podman-compose up --build backend` to rebuild and start PostgreSQL, Memcached, and the Django API
- Add the frontend with `podman-compose up frontend`
- The API is served over HTTP at `http://127.0.0.1:8000/`; update any local API URLs by editing `app/.env.development` before launching the frontend container
- Database data persists in the `postgres_data` volume; remove it with `podman volume rm dailyoffice2019_postgres_data`

### Code formatting standard

- Please use `black` to format code with a line length of 119 before submitting a pull request
- `find . -iname "*.py" | xargs black --target-version=py313 --line-length=119` from the `site` directory

### Testing

![Tests](https://img.shields.io/badge/tests-976%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-77%25-yellow)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2.6-green)
![Constitutional Compliance](https://img.shields.io/badge/constitutional%20compliance-Phase%2021%20Complete-success)
![Code Quality](https://img.shields.io/badge/code%20quality-Black%20formatted-black)

The project has comprehensive test coverage following constitutional compliance principles:

#### Running Tests

**Backend tests via podman-compose** (recommended):
```bash
podman-compose run --rm backend bash -c "pytest --cov=office --cov=churchcal --cov=bible --cov=psalter --cov-report=html --cov-report=xml"
```

**Backend tests locally**:
```bash
cd site
source env/bin/activate
pytest --cov=office --cov=churchcal --cov=bible --cov-report=html
```

**Frontend E2E tests**:
```bash
cd app
npm run test:e2e
```

#### Test Suite Status

- **976 tests passing** (100% pass rate for non-skipped tests)
- **49 tests skipped** (unit tests requiring clean database + integration tests)
- **1 expected failure** (known API error handling limitation)
- **Test execution time**: ~105 seconds (backend), ~3 minutes (E2E)
- **Backend Coverage**: 77% overall (12,774 of 16,506 lines)
  - Core office modules: 90-97% coverage
  - Family prayer modules: 100% coverage
  - Church calendar: 91% coverage
  - Bible passage retrieval: 81% coverage

#### Constitutional Compliance

The project follows a constitutional testing approach with phases:

- ✅ **Phase 1-2**: Test infrastructure established
- ✅ **Phase 3-9**: All 7 user stories have comprehensive test coverage
- ✅ **Phase 10-18**: Cross-story integration testing complete
- ✅ **Phase 19**: Performance testing (SC-001: Office page load < 3 seconds)
- ✅ **Phase 20**: Documentation and code quality improvements
- ✅ **Phase 21**: Polish & Cross-Cutting Concerns - All tests passing

See `docs/testing/` for detailed phase documentation.

## Quick overview

The application is built around several Django "apps". The most important are:

- *website*: This is the base site. All settings are defined in `website\settings.py` and all paths are defined
  in `website\routes.py`. Start here.
- *office*: This is where the bulk of the work is down to generate each Office.
- *churchcal*: This is used to build the church calendar. It currently supports both the Anglican Church in North
  America and the Episcopal Church calendars (though only ACNA is currently used for this project)
- *bible*: This is used to retrieve bible passages from various sources (currently only Bible Gateway, but others such
  as the ESV API are coming soon)
- *psalter*: This is used to retrieve passages from the Psalms (currently only the renewed Coverdale translation in the
  Book of Common Prayer 2019)

NOTE: churchcal, bible, and psalter apps may be spun off as separate projects soon and added as dependencies to this
project

## Submitting Issues and Contact

- For feature requests, please submit an issue and label it "enhancement"
- For bug reports, please submit an issue and label it "bug"
- Email the original creator Ben @ feedback@dailyoffice2019.com
- Join the Facebook discussion at: https://www.facebook.com/groups/dailyoffice/
