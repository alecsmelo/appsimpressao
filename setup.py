from cx_Freeze import setup, Executable
setup(
    name = "Tabuletas Exiba",
    version = "0.2.5",
    author = "Alecsandro Ferreira Melo",
    options = {"build_exe": {
        'packages': ["sqlite3","tkinter"],
        'include_files': ['icone.ico','DB_Exiba.db','logoexiba.png'],
        'include_msvcr': True,
    }},
    executables = [Executable("Tabuletas Exiba.py",base="Win32GUI", icon="icone.ico")]
    )
