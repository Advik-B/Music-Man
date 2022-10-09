import os
def add_path(path: str, on_top: bool = False):
    if on_top:
        os.environ["PATH"] = f"{path}{os.pathsep}{os.environ['PATH']}"
    else:
        os.environ["PATH"] += f"{os.pathsep}{path}"