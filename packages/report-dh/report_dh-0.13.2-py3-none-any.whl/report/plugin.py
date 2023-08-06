import pytest
from ._data import parse
from ._internal import Launch
import asyncio


def add_fixtures_to_teardown(fixture_name, teardown_name):
    item_id = Launch.create_report_item(
            name=fixture_name,
            parent_item=teardown_name,
            type='step',
            description='',
            has_stats=False)

    Launch.add_item(fixture_name, item_id)


def pytest_configure(config):
    config.addinivalue_line("markers", "feature()")
    config.addinivalue_line("markers", "story")


def pytest_addoption(parser):
    parser.addoption("--report", action="store_true")


def pytest_collection_finish(session):
    if session.config.getoption("--report"):
        parse()
        Launch.start_launch()

# def pytest_collection_modifyitems(config, items):
#     for item in items:
#         if item.get_closest_marker(name="feature"):
#             # Perform your actions here
#             item.cls.new_setup_class()  # replace with your actual setup function call


def pytest_sessionfinish(session, exitstatus):
    script_path = session.config.getoption("--report")
    for item in Launch.items().keys():
        Launch.finish_item(item)

    Launch.finish_launch()
    if script_path:
        for item in Launch.items().keys():
            Launch.finish_item(item)

        Launch.finish_launch()

        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                loop.close()

        except RuntimeError as e:
           pass


@pytest.hookimpl(tryfirst=True)
def pytest_fixture_setup(fixturedef, request):
    fixture_name = request.fixturename
    if fixture_name and '_xunit_setup_class' not in fixture_name:
        if request.scope in ['class', 'function']:
            required_fixture = getattr(request.cls, request.fixturename, None)
            new_fixture_name = getattr(required_fixture, '__new_name__', request.fixturename)

        else:
            function_fixture = request._fixturedef.func
            new_fixture_name = getattr(function_fixture, '__new_name__', request.fixturename)

        fixture_values = {}
        for fixture in request.fixturenames:
            if '{{{}}}'.format(fixture) in new_fixture_name:
                fixture_values[fixture] = request.getfixturevalue(fixture)

        parent = f'{request._pyfuncitem.name}_Setup'
        formatted_name = new_fixture_name.format(**fixture_values)
        item_id = Launch.create_report_item(
                name=formatted_name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description='')
    
        Launch.add_item(request.fixturename, item_id)

def add_items(item):
    available_items = Launch.items()
    markers = item.parent.own_markers.copy()
    markers.reverse()
    for index in range(len(markers)):
        marker = markers[index]
        marker_name = marker.kwargs['name']
        marker_class_name = marker.kwargs['class_name']
        parent = markers[index - 1] if index > 0 else None
        parent_name = parent.kwargs['name'] if parent else ''
        type = 'suite' if marker.name == 'feature' else 'story'
        if marker_class_name not in available_items:
            item_id = Launch.create_report_item(
                name=marker_name,
                parent_item=parent_name,
                type=type,
                attributes=[],
                description='',
                has_stats=True)

            Launch.add_item(marker_name, item_id)
            Launch.add_item(marker_class_name, item_id)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    test_name = getattr(item.function, '__new_name__', item.name)
    add_items(item)
    if item.name not in Launch.items() and item.parent is not None:
        attributes = [marker.name for marker in item.iter_markers()]
        
        try:
            params = item.callspec.params
            params_list = [{"key": param, "value": str(value)} for param, value in params.items()]
            if 'parametrize' in attributes:
                attributes.remove('parametrize')

            if 'feature' in attributes:
                attributes.remove('feature')

            if 'story' in attributes:
                attributes.remove('story')

        except:
            params_list = []

        item_id = Launch.create_report_item(
            name=test_name,
            parent_item=item.parent.name,
            type='test',
            has_stats=True,
            description='',
            attributes=attributes,
            parameters=params_list)

        Launch.add_item(item.name, item_id)
        item_is_not_skipped = 'skip' not in attributes
        
        if not item_is_not_skipped:
            marker = item.get_closest_marker("skip")
            skip_reason = marker.kwargs.get("reason")
            Launch.finish_skipped_item(item.name, skip_reason)
        
        if item_is_not_skipped:
            item_setup_name = f'Setup'
            item_id = Launch.create_report_item(
                name=item_setup_name,
                parent_item=item.name,
                type='before_test',
                has_stats=True,
                description='')

            Launch.add_item(f'{item.name}_{item_setup_name}', item_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    item_teardown_name = 'Teardown'
    attributes = [marker.name for marker in item.iter_markers()]
    item_is_not_skipped = 'skip' not in attributes
    if item_is_not_skipped:
        item_id = Launch.create_report_item(
            name=item_teardown_name,
            parent_item=item.name,
            type='after_test',
            has_stats=True,
            description='')

        teardown_name = f'{item.name}_{item_teardown_name}'
        Launch.add_item(teardown_name, item_id)

        for fixture_name in item.fixturenames:
            if 'request' not in fixture_name:
                if '_xunit_setup_class' not in fixture_name:
                    add_fixtures_to_teardown(fixture_name, teardown_name)
                    required_fixture = item._fixtureinfo.name2fixturedefs[fixture_name][0]
                    required_fixture.addfinalizer(lambda fixture_name=fixture_name: Launch.finish_item(fixture_name))


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    excinfo = call.excinfo
    attributes = [marker.name for marker in item.iter_markers()]
    item_is_not_skipped = 'skip' not in attributes
    if item_is_not_skipped:
        if call.when == 'setup':
            run_item_teardown(f'{item.name}_Setup', excinfo)

        if call.when == 'call':
            run_item_teardown(f'{item.name}_Execution', excinfo)

        if call.when == 'teardown':
            run_item_teardown(f'{item.name}_Teardown', excinfo)
        

def pytest_exception_interact(node, call, report):
    __tracebackhide__ = True
    item_name = Launch.get_latest_item()

    excinfo = call.excinfo
    traceback = getattr(report.longrepr, 'reprtraceback', None)
    formatted_traceback = traceback.reprentries[-1].reprfileloc if traceback else ''
    traceback_str = str(formatted_traceback)
    traceback_str = f'{traceback_str}\n\n-------------------------------------------------------------\n\n'
    traceback_str = f'{traceback_str}{report.longreprtext}'
    Launch.finish_failed_item(item_name, message=excinfo.typename, reason=traceback_str)


def run_item_teardown(item_name: str, excinfo):
    if excinfo is None:
        Launch.finish_passed_item(item_name)
        if 'Setup' in item_name:
            required_item = item_name.split('_Setup')[0]
            add_item_execution(required_item)

        if 'Teardown' in item_name:
            required_item = item_name.split('_Teardown')[0]
            Launch.finish_passed_item(required_item)

def add_item_execution(item_name):
    item_execution_name = 'Execution'
    item_id = Launch.create_report_item(
        name=item_execution_name,
        parent_item=item_name,
        type='scenario',
        has_stats=True,
        description='')

    Launch.add_item(f'{item_name}_{item_execution_name}', item_id)