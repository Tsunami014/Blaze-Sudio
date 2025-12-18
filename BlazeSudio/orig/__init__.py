def Debug(folder):
    import importlib
    import pkgutil
    import sys

    orig_pkg = importlib.import_module(f"BlazeSudio.orig.{folder}")
    sys.modules[f"BlazeSudio.{folder}"] = orig_pkg

    # Walk all submodules in orig.folder
    for mod in pkgutil.walk_packages(orig_pkg.__path__, orig_pkg.__name__ + "."):
        orig_name = mod.name
        redirected_name = orig_name.replace("orig.", "", 1)

        module = importlib.import_module(orig_name)
        sys.modules[redirected_name] = module

