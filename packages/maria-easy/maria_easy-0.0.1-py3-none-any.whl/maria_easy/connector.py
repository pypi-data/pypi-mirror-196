#!/usr/bin/env python
# -*-coding:UTF-8 -*
#
# Olivier Locard
"""
MariaDB Connector/Python Connection Module
Handles the connection to a MariaDB database server.
"""

from time import sleep
from typing import Union

import mariadb

from .data_classes import Response


class Connector:
    """
    MariaDB Connector/Python Connection Object
    Handles the connection to a MariaDB database server.
    """
    default_host = 'localhost'
    default_max_reconn = 1
    default_delay_reconn = 1
    default_max_retry = 3

    def __init__(self, user: str, password: str, database: Union[str, None] = None,
                 host: Union[str, None] = None):
        self.user = user
        self.password = password
        self.host = host or Connector.default_host
        self.database = database
        self.connection = self._connection
        self.max_reconn = Connector.default_max_reconn
        self.delay_reconn = Connector.default_delay_reconn
        self.max_retry = Connector.default_max_retry

    @property
    def _conn_params(self) -> dict:
        return {"user": self.user,
                "password": self.password,
                "host": self.host,
                "database": self.database,
                "reconnect": True}

    @property
    def _connection(self) -> Union[mariadb.Connection, None]:
        try:
            return mariadb.connect(**self._conn_params)
        except mariadb.Error as err:
            print(err)
            return None

    def close(self) -> None:
        """
        Close a connection.
        """
        if self.connection is not None:
            self.connection.close()

    def commit(self) -> None:
        """
        Commit a connection.
        """
        if self.connection is not None:
            self.connection.commit()

    def connect(self, attempts: int = None, delay: int = None) -> mariadb.Connection | None:
        """
        Try to connect to a MariaDB database server.
        :param attempts: Number of attempts
        :param delay: Delay between each attempt
        :return: A MariaDB connection
        """
        if attempts is None:
            attempts = self.max_reconn
        if delay is None:
            delay = self.delay_reconn
        counter = 1
        while counter <= attempts:
            try:
                return mariadb.connect(**self._conn_params)
            except mariadb.Error:
                counter += 1
                sleep(delay)
                continue
        return None

    def _cursor_execute(self, statement: str) -> Response:
        """
        Execute a statement
        :param statement: The statement to execute
        :return: a Response dataclass containing values and/or status
        """
        response = Response()
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement)
            if statement.lower().startswith('select'):
                fetched = cursor.fetchall()
                for row in fetched:
                    response.values.append(row)
            self.commit()
            cursor.close()
        except mariadb.Error as err:
            response.status = err
        return response

    def execute(self, statement: str, retry: int = 1) -> Response | None:
        """
        Execute a statement with a ping and a reconnect precaution.
        :param retry: How much time to retry to connect and execute
        :param statement: The statement to execute
        :return: a Response dataclass containing values and/or status
        """
        try:
            return self._cursor_execute(statement)
        except mariadb.OperationalError:
            try:
                self.connection.ping()
            except mariadb.InterfaceError:
                self.connect()
            if retry <= self.max_retry:
                self.execute(statement, retry + 1)
            return None
