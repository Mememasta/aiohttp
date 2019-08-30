import pathlib

class BaseConfig:

    debug = True
    app_name = 'Social Blog'
    secret_key = b'TyzLMReLCWUiPsTFMActw_0dtEU7kAcFXHNYYm64DNI='
    database_name = 'my_database'

    PROJECT_ROOT = pathlib.Path(__file__).parent.parent
    static_dir = str(PROJECT_ROOT / 'static')