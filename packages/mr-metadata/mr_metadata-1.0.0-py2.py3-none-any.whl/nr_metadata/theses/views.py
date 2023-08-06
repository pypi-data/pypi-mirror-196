from flask import Blueprint


def create_blueprint_from_app_theses(app):
    """Create  blueprint."""
    blueprint = app.extensions["theses"].resource.as_blueprint()
    blueprint.record_once(init_create_blueprint_from_app_theses)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_theses") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_blueprint_from_app_theses(state):
    """Init app."""
    app = state.app
    ext = app.extensions["theses"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.service, service_id="theses")

    # Register indexer
    if hasattr(ext.service, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(ext.service.indexer, indexer_id="theses")


def create_blueprint_from_app_thesesExt(app):
    """Create -ext blueprint."""
    blueprint = Blueprint("theses-ext", __name__, url_prefix="theses")
    blueprint.record_once(init_create_blueprint_from_app_theses)

    # calls record_once for all other functions starting with "init_app_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_app_addons_theses") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint
