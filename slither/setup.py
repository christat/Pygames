import cx_Freeze


executables = [cx_Freeze.Executable("slither.py")]

cx_Freeze.setup(
        name="Slither",
        options={"build_exe":{"packages":["pygame"],"include_files":["sprites/","fonts/"]}},
        description="Slither game tutorial",
        executables = executables
        )
cx_Freeze.buildOptions = {"includes": ["encodings.utf_8","encodings.ascii"]}
