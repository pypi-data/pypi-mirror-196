from loci import LOCI_PROJECT_FILENAME


class LociError(Exception):
    '''A generic Loci error. All other errors inherit from this.
    '''
    default_msg = "Something went wrong in Loci Notes."


class LociClientError(LociError):
    '''A generic Loci client error. This means something is wrong on the host where you tried to run a client.
    '''
    default_msg = "Something went wrong in the Loci Notes client."


class LociServerError(LociError):
    '''A generic Loci server error. This means something went wrong on the server, and you likely need to fix
    something in the data sent to the server.
    '''
    def __init__(self, detail_msg: str):
        self.default_msg = "Something went wrong in the Loci Notes server. " + detail_msg


class LociLocalConfigReadError(LociClientError):
    '''Raised when the configuration file of the localhost could not be read.
    '''

    def __init__(self, config_file_location: str):
        self.default_msg = "Unable to read config file at [bold]" + config_file_location + "[/bold]."
        self.config_file_location = config_file_location


class LociLocalProjectNotFoundError(LociClientError):
    '''Raised when there is no local project found in a given directory (or it's parents).
    '''
    default_msg = "There is no project associated with this directory, use [bold]loci setup project[/bold] "\
                  "in the project working folder to set this correctly."


class LociNoEnvError(LociClientError):
    '''Raised when the ENV of the call could not be determined.
    '''
    default_msg = "Unable to determine the environment of the Loci server to call. For most actions, "\
                  "this likely means that you are not in a project directory, and the [bold]"\
                  f"{LOCI_PROJECT_FILENAME}[/bold] file isn't present. You can also set a default"\
                  " environment in your local Loci config file, or via the LOCI_ENV "\
                  "environment variable."


class LociNoServerError(LociClientError):
    '''Raised when the server of the call could not be found in local config.
    '''
    def __init__(self, env: str):
        self.default_msg = f"Unable to find the server for the [bold]{env}[/bold] environment. You probably "\
                           "need to run [bold]loci setup server[/bold] or [bold]loci setup localhost[/bold]."
        self.env = env


class LociBadServerError(LociClientError):
    '''Raised when the server of the call does not respond.
    '''
    def __init__(self, server: str):
        self.default_msg = "The Loci server did not respond. Is the URL correct and the server at "\
                           f"[bold]{server}[/bold] running?"
        self.server = server


class LociNoApiKeyError(LociClientError):
    '''Raised when the API key of the call could not be found in local config.
    '''
    def __init__(self, env: str):
        self.default_msg = f"Unable to find an API key for the [bold]{env}[/bold] environment. You probably"\
                           " need to run [bold]setup server[/bold] or [bold]setup localhost[/bold]."
        self.env = env


class LociServerInputError(LociServerError):
    '''Raised on a server 400.
    '''
    def __init__(self, detail_msg: str = None):
        self.default_msg = "The data passed to the server was incorrect, please check your inputs. "
        if detail_msg is not None:
            self.default_msg += detail_msg


class LociServerAuthenticationError(LociServerError):
    '''Raised on a server 401.
    '''
    def __init__(self, detail_msg: str = None):
        self.default_msg = "The credentials passed to the server were incorrect, or none were given. The call "\
                  "requires authentication. " + detail_msg


class LociServerAuthorizationError(LociServerError):
    '''Raised on a server 403.
    '''
    def __init__(self, detail_msg: str = None):
        self.default_msg = "You do not have permission to perform that action. " + detail_msg


class LociServerObjectNotFoundError(LociServerError):
    '''Raised on a server 404.
    '''
    def __init__(self, detail_msg: str = None):
        self.default_msg = "Not found. " + detail_msg


class LociServerUnknownError(LociServerError):
    '''Raised on a server 500, or something else going wrong.
    '''
    def __init__(self, code: int, detail_msg: str = None):
        if detail_msg:
            self.default_msg = "Something went wrong in the Loci Notes server. Please check the error log for more "\
                          "details. Code =" + code + " - Details: " + detail_msg
        else:
            self.default_msg = "Something went wrong in the Loci Notes server. Please check the error log for more "\
                          "details. Code =" + code
