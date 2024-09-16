MLServerMLflowRuntime: str
MLServerDefaultModelName: str

def get_cmd(model_uri: str, port: int = None, host: str = None, timeout: int = None, nworkers: int = None) -> tuple[str, dict[str, str]]: ...
