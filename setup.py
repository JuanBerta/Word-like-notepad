from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
    "include_files": ["icons/"],
}

setup(
    name="Word_like_notepad",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("Word-like-notepad.py", base="gui", icon="./icons/program_icon.ico")
    ],
)
