import pathlib
dir = pathlib.Path('')
[print(str(entry.name)) for entry in dir.glob('**/*') if entry.is_file()]