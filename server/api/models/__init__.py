import sys

try:
    from server.api.models.models import UserQueries  # noqa: F401
    from server.api.models.irbis_models import IrbisPerson  # noqa: F401

    sys.modules.setdefault('api.models.models', sys.modules.get('server.api.models.models'))
    sys.modules.setdefault('api.models.irbis_models', sys.modules.get('server.api.models.irbis_models'))
except ImportError:
    pass
