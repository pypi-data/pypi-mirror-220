#
# Microlog. Copyright (c) 2023 laffra, dcharbon. All rights reserved.
#

from __future__ import annotations

from microlog.api import symbols
from microlog import log

class Meta():
    def __init__(self, kind: int, when:float, main: str):
        self.when = when
        self.kind = kind
        self.main = main

    @classmethod
    def unmarshall(cls, event: list) -> Meta:
        kind, when, mainIndex = event
        return Meta(
            kind,
            when,
            symbols.get(mainIndex),
        )

    def marshall(self):
        log.put([
            self.kind,
            self.when,
            symbols.index(self.main),
        ])
