#!/usr/bin/env python
# -*-coding:UTF-8 -*
#
# Olivier Locard
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import mariadb

from fixtures.mocks import MockConnection, MockCursor
from maria_easy.connector import Connector
from maria_easy.data_classes import Response


def test_connector(connector):
    assert isinstance(connector, Connector) is True
    assert hasattr(connector, "user") is True
    assert hasattr(connector, "password") is True
    assert hasattr(connector, "host") is True
    assert hasattr(connector, "database") is True
    assert connector.host == 'localhost'


def test_connector_conn_params(connector):
    assert isinstance(connector._conn_params, dict) is True  # pylint: disable=protected-access


def test_connector_connection(connector, mocked_connector):
    assert mocked_connector.connection is not None
    assert connector.connection is None


def test_connector_close(mocked_connector):
    assert mocked_connector.close() is None


def test_connector_commit(mocked_connector):
    assert mocked_connector.commit() is None


def test_connector_connect(connector):
    assert connector.connect() is None


def test_connector_cursor_execute(connector, mocked_connector, monkeypatch):
    try:
        connector._cursor_execute('')  # pylint: disable=protected-access
    except Exception as err:  # pylint: disable=broad-exception-caught
        assert isinstance(err, AttributeError) is True
        assert str(err) == "'NoneType' object has no attribute 'cursor'"

    assert mocked_connector._cursor_execute('statement') == Response(values=[], status='')
    assert mocked_connector._cursor_execute('select * from test') == Response(values=[(1,), (42,)],
                                                                              status='')

    def mock_execute(*args, **kwargs):
        raise mariadb.Error('test_error')

    monkeypatch.setattr(MockCursor, "execute", mock_execute)
    assert str(mocked_connector._cursor_execute('statement')) == 'test_error'


def test_connector_execute(connector, mocked_connector, monkeypatch):
    try:
        connector.execute('')
    except Exception as err:  # pylint: disable=broad-exception-caught
        assert isinstance(err, AttributeError) is True
        assert str(err) == "'NoneType' object has no attribute 'cursor'"
    assert isinstance(mocked_connector.execute(''), Response) is True

    def mock_cursor_execute(*args, **kwargs):
        raise mariadb.OperationalError

    monkeypatch.setattr(mocked_connector, "_cursor_execute", mock_cursor_execute)
    assert mocked_connector.execute('') is None

    def mock_ping(*args, **kwargs):
        raise mariadb.InterfaceError

    monkeypatch.setattr(MockConnection, "ping", mock_ping)
    assert mocked_connector.execute('') is None
