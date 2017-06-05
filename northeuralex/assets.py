from clldutils.path import Path
from clld.web.assets import environment

import northeuralex


environment.append_path(
    Path(northeuralex.__file__).parent.joinpath('static').as_posix(),
    url='/northeuralex:static/')
environment.load_path = list(reversed(environment.load_path))
