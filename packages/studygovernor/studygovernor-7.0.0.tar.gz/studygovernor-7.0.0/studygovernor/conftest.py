# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib
import pytest

from . import create_app


# Put this in your conftest.py
@pytest.fixture(scope='session')
def celery_config():
    return {
        'task_always_eager': True,
        'task_eager_propagates': True,
    }


@pytest.fixture(scope='session')
def celery_includes():
    return [
        'studygovernor.callbacks.backends.celery_backend',
    ]


@pytest.fixture(scope="session")
def networks_dir():
    return pathlib.Path(__file__).parent / 'tests' / 'networks'


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_uri = 'sqlite:///:memory:'

    # create the app with common test config
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'SECRET_KEY': 'o8[nc2foeu2foe2ij',
        'SECURITY_PASSWORD_SALT': 'sgfms8-tcfm9de2nv',
        'STUDYGOV_CELERY_BROKER': "pyamqp://guest@localhost",
    }, use_sentry=False)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def init_db(app):
    # create the database and load test data
    from .models import db
    db.create_all(app=app)

    yield db

    db.drop_all()
    db.session.commit()


@pytest.fixture(scope="function")
def app_config(app, init_db):
    # Load the config file with initial setup
    config_file = pathlib.Path(__file__).parent / 'tests' / 'config' / 'test_config.yaml'
    from .util.helpers import load_config_file
    load_config_file(app, config_file, silent=True)


@pytest.fixture(scope="function")
def workflow_test_data(app, app_config):
    # Load test workflow
    workflow_file = pathlib.Path(__file__).parent / 'tests' / 'test_workflow.yaml'

    # Make sure the workflow is loaded
    from .util.helpers import initialize_workflow
    initialize_workflow(workflow_file, app=app)


@pytest.fixture(scope="function")
def second_workflow_test_data(app, app_config):
    # Load test workflow
    workflow_file = pathlib.Path(__file__).parent / 'tests' / 'second_workflow.yaml'

    # Make sure the workflow is loaded
    from .util.helpers import initialize_workflow
    initialize_workflow(workflow_file, app=app)


@pytest.fixture(scope="function")
def workflow_with_callbacks_test_data(app, app_config):
    # Load test workflow
    workflow_file = pathlib.Path(__file__).parent / 'tests' / 'test_workflow_callbacks.yaml'

    # Make sure the workflow is loaded
    from .util.helpers import initialize_workflow
    initialize_workflow(workflow_file, app=app)


@pytest.fixture(scope="function")
def cohort_data(init_db):
    from studygovernor.models import Cohort
    from studygovernor.models import db

    # Create a test cohort
    cohort = Cohort(label="test_cohort", description="Some test cohort")
    db.session.add(cohort)
    db.session.commit()

@pytest.fixture(scope="function")
def cohort_subject_data(init_db, workflow_test_data):
    from datetime import date
    from studygovernor.models import Cohort, Subject, Workflow
    from studygovernor.models import db
    from studygovernor.control import create_experiment

    workflow = Workflow.query.order_by(Workflow.id.desc()).first()

    # Create a test cohort
    cohort = Cohort(label="test_cohort", description="Some test cohort")
    for subject_id in range(1, 3):
        subject_label = f"Test_Subject_{subject_id}_cohort"
        subject_dob = date(2019, 1, subject_id)
        subject = Subject(cohort=cohort, label=subject_label, date_of_birth=subject_dob)
        db.session.add(subject)
        db.session.commit()
        for experiment_id in range(1, 3):
            experiment_label = f"Experiment_{subject.id}_{experiment_id}"
            experiment_scandate = date(2019, 1, experiment_id)
            experiment = create_experiment(workflow, subject=subject, label=experiment_label, scandate=experiment_scandate)
            db.session.add(experiment)

    db.session.add(cohort)
    db.session.commit()

@pytest.fixture(scope="function")
def subject_data(cohort_data):
    from datetime import date
    from studygovernor.models import Cohort, Subject
    from studygovernor.models import db

    cohort = Cohort.query.first()
    
    # Create 2 test subjects
    for subject_id in range(1, 3):
        subject_label = f"Test Subject_{subject_id}"
        subject_dob = date(2019, 1, subject_id)
        subject = Subject(label=subject_label, date_of_birth=subject_dob, cohort=cohort)
        db.session.add(subject)
    db.session.commit()


@pytest.fixture(scope="function")
def experiment_data(workflow_test_data, subject_data):
    from datetime import date
    from studygovernor.models import Subject
    from studygovernor.models import db
    from studygovernor.models import Workflow
    from studygovernor.control import create_experiment

    workflows = Workflow.query.all()
    print(f"workflows found: {len(workflows)}")
    for workflow in workflows:
        print(workflow)

    workflow = Workflow.query.order_by(Workflow.id.desc()).first()

    # Create 2 test experiments per test subject
    subjects = Subject.query.filter(Subject.label.startswith('Test Subject_')).all()
    for subject in subjects:
        for experiment_id in range(1, 3):
            experiment_label = f"Experiment_{subject.id}_{experiment_id}"
            experiment_scandate = date(2019, 1, experiment_id)
            experiment = create_experiment(workflow, subject=subject, label=experiment_label, scandate=experiment_scandate)
            db.session.add(experiment)
    db.session.commit()


@pytest.fixture(scope="function")
def experiment_data_with_callback(workflow_with_callbacks_test_data, subject_data):
    from datetime import date
    from studygovernor.models import Subject
    from studygovernor.models import db
    from studygovernor.models import Workflow
    from studygovernor.control import create_experiment

    workflows = Workflow.query.all()
    print(f"workflows found: {len(workflows)}")
    for workflow in workflows:
        print(workflow)

    workflow = Workflow.query.order_by(Workflow.id.desc()).first()

    # Create 2 test experiments per test subject
    subjects = Subject.query.filter(Subject.label.startswith('Test Subject_')).all()
    for subject in subjects:
        for experiment_id in range(1, 3):
            experiment_label = f"Experiment_{subject.id}_{experiment_id}"
            experiment_scandate = date(2019, 1, experiment_id)
            experiment = create_experiment(workflow, subject=subject, label=experiment_label, scandate=experiment_scandate)
            db.session.add(experiment)
    db.session.commit()


@pytest.fixture(scope="function")
def externalsystem(init_db):
    from studygovernor.models import ExternalSystem
    from studygovernor.models import db
    # Create 3 external systems
    for externalsystem_id in range(1, 4):
        system_name = f'NewSystemName_{externalsystem_id}'
        system_url = f'http://system-{externalsystem_id}.url'

        external_system = ExternalSystem(system_name=system_name, url=system_url)
        db.session.add(external_system)
    db.session.commit()


@pytest.fixture(scope="function")
def subject_links(subject_data, externalsystem):
    # Link External systems to Subject
    from studygovernor.models import ExternalSystem
    from studygovernor.models import Subject, Cohort
    from studygovernor.models import ExternalSubjectLinks
    from studygovernor.models import db

    # Get data
    subjects = Subject.query.all()
    externalsystems = ExternalSystem.query.all()

    # Define links
    externalsystem_links = [
        (externalsystems[0], subjects[0], 1),  # Link externalsystem[0] to subject[0]
        (externalsystems[1], subjects[1], 2),  # Link externalsystem[1] to subject[1]
        (externalsystems[2], subjects[1], 2),  # Link externalsystem[2] to subject[1]
    ]

    # link subjects to external_data
    for externalsystem_link in externalsystem_links:
        external_link = ExternalSubjectLinks(
            f'External_SubjectID_{externalsystem_link[2]}',
            externalsystem_link[1],
            external_system=externalsystem_link[0])
        db.session.add(external_link)
    db.session.commit()


@pytest.fixture(scope="function")
def experiment_links(experiment_data, externalsystem):
    # Link External systems to Experiment
    from studygovernor.models import ExternalSystem
    from studygovernor.models import Experiment
    from studygovernor.models import ExternalExperimentLinks
    from studygovernor.models import db

    # Get data
    experiments = Experiment.query.all()
    externalsystems = ExternalSystem.query.all()

    # Define links
    externalsystem_links = [
        (externalsystems[0], experiments[0], 1),  # Link externalsystem[0] to subject[0]
        (externalsystems[1], experiments[1], 2),  # Link externalsystem[1] to subject[0]
        (externalsystems[2], experiments[1], 2),  # Link externalsystem[3] to subject[0]
    ]

    # link experiments to external_data
    for externalsystem_link in externalsystem_links:
        external_link = ExternalExperimentLinks(
            f'External_ExperimentID_{externalsystem_link[2]}',
            externalsystem_link[1],
            external_system=externalsystem_link[0])
        db.session.add(external_link)
    db.session.commit()


@pytest.fixture(scope="function")
def cohort_links(cohort_data, externalsystem):
    from studygovernor.models import Cohort, ExternalSystem, ExternalCohortUrls, db

    # Add second cohort to test handling of empty external_ids dictionary
    second_cohort = Cohort(label="second_cohort", description="Second test cohort")
    db.session.add(second_cohort)
    db.session.commit()

    test_cohort = Cohort.query.first()
    
    externalsystems = ExternalSystem.query.all()
    externalcohort_urls = [
        (externalsystems[0], test_cohort, "test_cohort"),
        (externalsystems[1], test_cohort, "test_cohort")
    ]

    for externalcohort_url in externalcohort_urls:
        external_url = ExternalCohortUrls(
            url=f'https://external-url/{externalcohort_url[2]}',
            cohort=externalcohort_url[1],
            external_system=externalcohort_url[0]
        )
        db.session.add(external_url)
    db.session.commit()


@pytest.fixture(scope="function")
def scan_data(experiment_data):
    from studygovernor.models import Experiment, Scan, Scantype
    from studygovernor.models import db

    experiment_with_scans = Experiment.query.first()
    
    #Create scantypes and scans
    CT = Scantype(modality="CT", protocol="Head")
    FLAIR = Scantype(modality="MR", protocol="FLAIR")
    
    scan_1 = Scan(experiment_with_scans, CT)
    scan_2 = Scan(experiment_with_scans, FLAIR)

    db.session.add(CT)
    db.session.add(FLAIR)
    db.session.add(scan_1) 
    db.session.add(scan_2)
    db.session.commit()


@pytest.fixture
def client(app, app_config):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="module")
def no_db_app():
    """ Create and configure a new app instance with an invalid database. """
    db_uri = 'mysql+pymysql://user:password@localhost/non_existing_db'

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'SECRET_KEY': 'o8[nc2foeu2foe2ij',
        'SECURITY_PASSWORD_SALT': 'sgfms8-tcfm9de2nv',
        'STUDYGOV_CELERY_BROKER': "pyamqp://guest@localhost",
    }, use_sentry=False)

    yield app


@pytest.fixture
def no_db_client(no_db_app):
    """ A test client without a db. """
    return no_db_app.test_client()


@pytest.fixture
def callback_execution_data():
    cohort = {
        'description': None,
        'external_ids': None,
        'label': 'TestCohort',
        'subjects': ['api/v1/subjects/1'],
        'uri': '/api/v1/cohorts/0'
    }

    subject = {
        'cohort': '/api/v1/cohorts/0',
        'date_of_birth': '2019-01-01',
        'experiments': ['/api/v1/experiments/1',
                        '/api/v1/experiments/2'],
        'external_ids': {
            'XNAT': 'XNAT_SUB_ID'
        },
        'label': 'Test Subject_1',
        'uri': '/api/v1/subjects/1',
        'api_uri': 'http://localhost/api/v1/subjects/1',
        'web_uri': 'http://localhost/subjects/1'
    }

    experiment = {
        'external_ids': {
            'XNAT': 'XNAT_EXP_ID'
        },
        'variable_map': {
            'test': 42,
            'tag_var': ['tag1', 'tag2'],
            'tag_var2': 'extra_tag',
            'tag_var3': 13.37,
        },
        'label': 'Experiment_1_1',
        'scandate': '2019-01-01T00:00:00',
        'state': '/api/v1/experiments/1/state',
        'subject': '/api/v1/subjects/1',
        'uri': '/api/v1/experiments/1',
        'api_uri': 'http://localhost/api/v1/experiments/1',
        'web_uri': 'http://localhost/experiments/1',
    }

    external_systems = {
        'XNAT': 'https://xnat.example.com/',
        'TASKMANAGER': 'https://taskmanager.example.com/',
    }

    action = {
        'end_time': None,
        'executions': ['/api/v1/callback_executions/1',
                        '/api/v1/callback_executions/2'],
        'experiment': '/api/v1/experiments/1',
        'freetext': 'Transition triggered by setting state to step2 (3)',
        'return_value': None,
        'start_time': '2022-08-10T10:58:04.865224',
        'success': False,
        'transition': '/api/v1/transitions/2',
        'uri': '/api/v1/actions/5',
        'api_uri': 'http://localhost/api/v1/actions/5',
        'web_uri': 'http://localhost/actions/5',
    }

    _callback_exection_data = {
        'created': '2022-06-22T16:21:00',
        'finished': None,
        'result': 'none',
        'result_log': None,
        'result_values': None,
        'run_log': None,
        'run_start': None,
        'status': 'created',
        'uri': '/api/v1/callback_executions/1',
        'api_uri': 'http://localhost/api/v1/callback_executions/1',
        'web_uri': 'http://localhost/callback_executions/1',
        'wait_start': None,
        'secret': 'ncsnipcaklsdfj',
        'cohort': cohort,
        'subject': subject,
        'experiment': experiment,
        'external_systems': external_systems,
        'action': action,
    }

    return _callback_exection_data