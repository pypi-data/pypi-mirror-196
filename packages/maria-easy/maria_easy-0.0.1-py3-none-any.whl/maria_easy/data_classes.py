#!/usr/bin/env python
# -*-coding:UTF-8 -*
#
# Olivier Locard
"""
Module for data classe objects
"""

from dataclasses import dataclass, field


@dataclass
class Response:
    """
    This data class handles the result of a query execution.
    """
    values: list = field(default_factory=list)
    status: str = field(default_factory=str)

    def __str__(self):
        if self.status:
            return str(self.status)
        return str(self.values)
