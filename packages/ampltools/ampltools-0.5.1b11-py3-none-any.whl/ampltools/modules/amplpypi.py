# -*- coding: utf-8 -*-
import sys
import os


def _normalize_modules(modules=[], add_base=False, skip_base=False):
    prefix = "ampl_module_"
    names = [module.replace("-", "_").replace(prefix, "") for module in modules]
    module_names = [prefix + "base"] if add_base else []
    skip = ["ampl", "base"] if add_base or skip_base else []
    module_names += [prefix + name for name in names if name not in skip]
    return module_names


def installed_modules():
    from pkgutil import iter_modules

    prefix = "ampl_module_"
    installed = []
    for (_, name, _) in iter_modules():
        norm = name.replace("-", "_")
        if norm.startswith(prefix):
            installed.append(norm.replace(prefix, ""))
    return installed


def available_modules():
    from requests import get
    from re import findall

    url = "https://pypi.ampl.com/"
    return [
        l.replace("ampl-module-", "")
        for l in findall(">([^<]+)</a>", get(url).text)
        if l.startswith("ampl-module-")
    ]


def _available_bundles():
    from requests import get
    from json import loads

    url = "https://pypi.ampl.com/bundles.json"
    return loads(get(url).text)["bundles"]


def run_command(cmd, show_output=None, return_output=False, verbose=False):
    """
    Run a system command.
    Args:
        cmd: command to run.
        show_output: show the output of running the command.
        verbose: show verbose output if True.
    """
    from subprocess import check_output, STDOUT, CalledProcessError

    if isinstance(cmd, str):
        shell = True
        cmd_str = cmd
    else:
        shell = False
        cmd_str = " ".join(cmd)
    if verbose:
        print("$ " + cmd_str)
    try:
        output = check_output(cmd, stderr=STDOUT, shell=shell).decode("utf-8")
        if show_output or verbose:
            print(output.rstrip("\n"))
        if return_output:
            return 0, output
        return 0
    except CalledProcessError as e:
        output = e.output.decode("utf-8")
        if verbose:
            print(output.rstrip("\n"))
        if return_output:
            return e.returncode, output
        return e.returncode


def _parse_module(module):
    if "=" not in module:
        return module, ""
    name, version = (
        module[: module.find("=")].strip(" ="),
        "==" + module[module.find("=") + 1 :].strip(" ="),
    )
    return name, version


def install_modules(modules=[], reinstall=False, options=[], verbose=False):
    """
    Install AMPL modules for Python.
    Args:
        modules: list of modules to be installed.
        reinstall: reinstall modules if True.
        options: list of options for pip.
        verbose: show verbose output if True.
    """
    if isinstance(modules, str):
        modules = [modules]
    available = None
    try:
        available = set(available_modules())
    except Exception:
        pass
    bundles = None
    try:
        bundles = _available_bundles()
    except Exception:
        pass
    requirements = modules
    if available:
        requirements = []
        for module in modules:
            version = ""
            if "=" in module:
                module, version = _parse_module(module)
            requirement = module + version
            if requirement in requirements or module == "ampl":
                continue
            elif module in available:
                requirements.append(requirement)
            elif not isinstance(bundles, list):
                requirements.append(requirement)
            else:
                for entry in bundles:
                    bundle, includes = None, []
                    try:
                        bundle = entry["module"]
                        includes = entry["includes"]
                    except:
                        pass
                    if module in includes:
                        raise Exception(
                            "AMPL module '{}' is not available. It is included in module '{}'.".format(
                                module, bundle
                            )
                        )
                else:
                    raise Exception("AMPL module '{}' is not available.".format(module))

    modules = _normalize_modules(modules=requirements, add_base=True)
    pip_cmd = [sys.executable, "-m", "pip", "install", "-i", "https://pypi.ampl.com"]
    if reinstall:
        pip_cmd += ["--force-reinstall", "--upgrade", "--no-cache"]
    if run_command(pip_cmd + modules + options, verbose=verbose) != 0:
        raise Exception("Failed to install modules.")


def uninstall_modules(modules=[], options=[], verbose=False):
    """
    Uninstall AMPL modules for Python.
    Args:
        modules: list of modules to be installed.
        options: list of options for pip.
        verbose: show verbose output if True.
    """
    if isinstance(modules, str):
        modules = [modules]
    skip_base = True
    installed = installed_modules()
    if modules == [] or "all" in modules:
        skip_base = False
        modules = installed
    if skip_base and "base" in modules:
        if set(modules) != set(installed):
            raise Exception(
                "Base module cannot be uninstalled alone. "
                "You need to uninstall all modules."
            )
        else:
            skip_base = False

    unload_modules(modules)
    modules = _normalize_modules(modules=modules, skip_base=skip_base)
    if len(modules) == 0:
        return
    pip_cmd = [sys.executable, "-m", "pip", "uninstall", "-y"]
    if run_command(pip_cmd + modules + options, verbose=verbose) != 0:
        raise Exception("Failed to uninstall modules.")


def _load_ampl_module(module_name):
    from importlib import import_module

    prefix = "ampl_module_"
    if not module_name.startswith(prefix):
        module_name = prefix + module_name
    module = import_module(module_name)
    try:
        from importlib import reload

        reload(module)
    except:
        pass
    if module.__file__ is None or not os.path.isfile(module.__file__):
        raise Exception("Module {} needs to be reinstalled.".format(module_name))
    bin_dir, version = module.bin_dir, module.__version__
    return bin_dir, version


def _locate_modules(modules, verbose=False):
    path_modules = []
    for name in modules:
        module_name = "ampl_module_" + name
        bin_dir = None
        try:
            bin_dir, _ = _load_ampl_module(module_name)
        except:
            if verbose:
                print("Failed to import {}.".format(module_name))
            continue
        if bin_dir not in path_modules:
            path_modules.append(bin_dir)
        if verbose:
            print("Imported {}.".format(module_name))

    return path_modules


def _sort_modules_for_loading(modules=[], add_base=True):
    if isinstance(modules, str):
        modules = [modules]
    if len(modules) == 0 or "all" in modules:
        modules = installed_modules()
    modules = [_parse_module(module)[0] for module in modules]
    if not add_base:
        return modules
    return ["base"] + [module for module in modules if module not in ("ampl", "base")]


def generate_requirements(modules=[]):
    """
    Generate requirements.txt content.
    Args:
        modules: list of modules.
        verbose: show verbose output if True.
    """
    modules = _sort_modules_for_loading(modules)
    requirements = "--index-url https://pypi.ampl.com\n"
    requirements += "--extra-index-url https://pypi.org/simple\n"
    for m in modules:
        try:
            _, version = _load_ampl_module(m)
            requirements += "ampl_module_{}=={}\n".format(m, version)
        except:
            pass
    return requirements


def load_modules(modules=[], head=True, verbose=False):
    """
    Load AMPL modules.
    Args:
        modules: list of modules to be loaded.
        head: add to the head of PATH if True.
        verbose: show verbose output if True.
    """
    path_modules = []
    path_others = []
    for path in os.environ["PATH"].split(os.pathsep):
        if path.endswith("bin") and "ampl_module_" in path:
            path_modules.append(path)
        else:
            path_others.append(path)

    modules = _sort_modules_for_loading(modules)
    for path in _locate_modules(modules, verbose=verbose):
        if path not in path_modules:
            path_modules.append(path)

    if head:
        os.environ["PATH"] = os.pathsep.join(path_modules + path_others)
    else:
        os.environ["PATH"] = os.pathsep.join(path_others + path_modules)


def unload_modules(modules=[]):
    """
    Unload AMPL modules.
    Args:
        modules: list of modules to be unloaded.
    """
    modules = _sort_modules_for_loading(modules, add_base=False)
    to_remove = set(_locate_modules(modules))
    os.environ["PATH"] = os.pathsep.join(
        [path for path in os.environ["PATH"].split(os.pathsep) if path not in to_remove]
    )


def preload_modules(silently=True, verbose=False):
    """
    Load all modules to the end of environment variable PATH.
    Args:
        silently: ignore any errors and just return False
        verbose: show verbose output if True.
    """
    try:
        load_modules(head=False, verbose=verbose)
        return True
    except:
        if not silently:
            raise
        return False


def path(modules=[]):
    """
    Return PATH for AMPL modules.
    Args:
        modules: list of modules to be included.
    """
    modules = _sort_modules_for_loading(modules)
    return os.pathsep.join(_locate_modules(modules, verbose=False))


def activate_license(uuid, verbose=False):
    """
    Activate an AMPL license using the UUID.
    Args:
        uuid: license uuid.
        verbose: show verbose output if True.
    """
    load_modules()
    exit_code = run_command(
        ["amplkey", "activate", "--uuid", uuid],
        verbose=verbose,
    )
    if exit_code != 0:
        raise Exception("The license activation failed.")
