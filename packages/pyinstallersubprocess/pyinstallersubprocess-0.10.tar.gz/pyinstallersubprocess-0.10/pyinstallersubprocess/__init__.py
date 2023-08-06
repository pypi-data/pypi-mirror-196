import os
import subprocess
import sys
import shutil


def subprocess_no_console_devnull(module, entry, *args, **kwargs):
    DEVNULL = open(os.devnull, "wb")
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if getattr(sys, "frozen", False):

        subprocess.run(
            [os.path.join(sys._MEIPASS, entry)],
            startupinfo=startupinfo,
            stdout=DEVNULL,
            stderr=DEVNULL,
            stdin=DEVNULL,
            *args,
            **kwargs,
        )
    else:
        subprocess.run(
            [sys.executable, "-m", f"{module}.{entry}"],
            startupinfo=startupinfo,
            stdout=DEVNULL,
            stderr=DEVNULL,
            stdin=DEVNULL,
            *args,
            **kwargs,
        )


def subprocess_no_console_popen(module, entry, *args, **kwargs):

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if getattr(sys, "frozen", False):

        process = subprocess.run(
            [os.path.join(sys._MEIPASS, entry)],
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    else:
        process = subprocess.run(
            [sys.executable, "-m", f"{module}.{entry}"],
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    return process


def subprocess_no_console_stdout_read(module, entry, *args, **kwargs):

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if getattr(sys, "frozen", False):

        process = subprocess.run(
            [os.path.join(sys._MEIPASS, entry)],
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    else:
        process = subprocess.run(
            [sys.executable, "-m", f"{module}.{entry}"],
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    return process.stdout.read()


def subprocess_console_devnull(module, entry, *args, **kwargs):
    DEVNULL = open(os.devnull, "wb")
    if getattr(sys, "frozen", False):

        subprocess.run(
            [os.path.join(sys._MEIPASS, entry)],
            stdout=DEVNULL,
            stderr=DEVNULL,
            stdin=DEVNULL,
            *args,
            **kwargs,
        )
    else:
        subprocess.run(
            [sys.executable, "-m", f"{module}.{entry}"],
            stdout=DEVNULL,
            stderr=DEVNULL,
            stdin=DEVNULL,
            *args,
            **kwargs,
        )


def subprocess_console_popen(module, entry, *args, **kwargs):

    if getattr(sys, "frozen", False):

        process = subprocess.run(
            [os.path.join(sys._MEIPASS, entry)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    else:
        process = subprocess.run(
            [sys.executable, "-m", f"{module}.{entry}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    return process


def subprocess_console_stdout_read(module, entry, *args, **kwargs):

    if getattr(sys, "frozen", False):

        process = subprocess.run(
            [os.path.join(sys._MEIPASS, entry)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    else:
        process = subprocess.run(
            [sys.executable, "-m", f"{module}.{entry}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            *args,
            **kwargs,
        )
    return process.stdout.read()


def subprocess_console(module, entry, *args, **kwargs):

    if getattr(sys, "frozen", False):

        process = subprocess.run(
            [os.path.join(sys._MEIPASS, entry)],
            *args,
            **kwargs,
        )
    else:
        process = subprocess.run(
            [sys.executable, "-m", f"{module}.{entry}"],
            *args,
            **kwargs,
        )
    return process


def convert_py_file_to_module(
    modulename,
    pythonfile,
    rename_pyfile=True,
    overwrite_existing=False,
    add_main_entry=True,
):

    mainfolder = os.path.normpath(f"{os.sep}".join(sys.executable.split(os.sep)[:-1]))

    pythonfileold = pythonfile[:-3] + ".old"
    entry = pythonfile.split(os.sep)[-1].split(".")[0]
    folderformod = os.path.normpath(os.path.join(mainfolder, modulename))
    initfile = os.path.normpath(os.path.join(mainfolder, modulename, "__init__.py"))
    pyfi = os.path.normpath(os.path.join(mainfolder, modulename, f"{entry}.py"))
    if not os.path.exists(folderformod):
        os.makedirs(folderformod)
    else:
        if not overwrite_existing:
            raise OSError("Folder already exists!")
    with open(initfile, mode="w", encoding="utf-8") as f:
        f.write("")
    shutil.copy(pythonfile, pyfi)
    with open(pyfi, mode="r", encoding="utf-8") as f:
        data = f.read()
    if "__name__" not in data and "__main__" not in data:
        if add_main_entry:
            print("No entry point, creating one")
            data = 'if __name__ == "__main__":\n    pass\n' + data
            with open(pyfi, mode="w", encoding="utf-8") as f:
                f.write(data)
    if rename_pyfile:
        try:
            os.rename(pythonfile, pythonfileold)
            print(f"{pythonfile} -> {pythonfileold}")
        except Exception as fe:
            print("File could not be renamed")
    return modulename, entry


