# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from typing import Generator

from flask import Flask

import svc_reg


def factory_with_cleanup() -> Generator[int, None, None]:
    yield 1


reg = svc_reg.Registry()

app = Flask("tests")
app = svc_reg.flask.init_app(app, reg)
app = svc_reg.flask.init_app(app)

svc_reg.flask.replace_value(int, 1)
svc_reg.flask.replace_value(int, 1, ping=lambda: None)

svc_reg.flask.register_value(app, int, 1)
svc_reg.flask.register_value(app, int, 1, ping=lambda: None)

svc_reg.flask.replace_factory(str, str)
svc_reg.flask.replace_value(str, str, ping=lambda: None)

svc_reg.flask.register_factory(app, str, str)
svc_reg.flask.register_factory(app, int, factory_with_cleanup)
svc_reg.flask.register_value(app, str, str, ping=lambda: None)

# The type checker believes whatever we tell it.
o1: object = svc_reg.flask.get(object)
o2: int = svc_reg.flask.get(object)
