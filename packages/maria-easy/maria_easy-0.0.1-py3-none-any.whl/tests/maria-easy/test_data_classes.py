#!/usr/bin/env python
# -*-coding:UTF-8 -*
#
# Olivier Locard


def test_response(response):
    assert hasattr(response, "values") is True
    assert hasattr(response, "status") is True
    assert str(response) == str([])
    response.status = 'test'
    assert str(response) == 'test'
