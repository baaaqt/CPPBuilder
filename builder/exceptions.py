class UndefinedCompilerException(Exception):
    def __init__(self, compiler_path: str, language: str) -> None:
        self._message = f'''Error: undefined compiler.\n
        Language mode: {language}.\n
        Compiler path: {compiler_path}.\n
        Please set correct language mode or path to compiler.
        '''

    def __str__(self) -> str:
        return self._message
