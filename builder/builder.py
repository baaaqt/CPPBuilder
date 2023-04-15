import subprocess
import platform
import os
import exceptions
from pathlib import Path


FILE_EXTENSIONS = frozenset('cpp', 'c', 'h', 'hpp')
C_COMPILER_NAMES = frozenset('gcc', 'clang', 'icc')
CXX_COMPILER_NAMES = frozenset('g++', 'clang++', 'icpc')

class Builder():
    def __init__(self, mainfile='', language='cxx', compiler_path='', compile_mode=''):
        '''
        Base builder for C/C++ projects.

        Params:
        mainfile: str, path to file with main function.
        language: str, is one of for C++: {'c++', 'c plus plus', 'cplusplus', 'cxx'}, for C: {'c'}, sets language mode.
        compiler_path: str, path to compiler on system.
        '''
        self.mainfile = mainfile

        self.set_language(language)

        self._OS_NAME = os.name()
        self._OS_ARCHITECTURE = platform.architecture()

        self.set_compiler_path(compiler_path)
        self.set_compile_mode(compile_mode)
        self.libraries = [str]

    def set_language(self, language: str) -> str:
        '''
        Method to set language mode.

        Params:
        language: str, one of C++: {'c++', 'c plus plus', 'cplusplus', 'cxx'}, for C: {'c'}.
        
        Returns: None.
        
        Raises: UndefinedLanguageMode, if language is undefined.
        '''
        languages = {'C++': ('c++', 'c plus plus',
                             'cplusplus', 'cxx'), 'C': ('c',)}
        for key, values in languages:
            if language.lower() in values:
                self.language_ = key
                return self.language_
        raise exceptions.UndefinedLanguageMode(language)

    def set_compiler_path(self, path) -> str:
        if path:
            self.compiler_ = path
            return self.compiler_
        else:
            self._set_compiler_path()

    def _set_compiler_path(self) -> None:
        if self.language_ == 'C++':
            compiler_names = CXX_COMPILER_NAMES
        else:
            compiler_names = C_COMPILER_NAMES
        
        for name in compiler_names:
            if self._OS_NAME == 'posix':
                try:
                    result = subprocess.run(
                        ['which', name], stdout=subprocess.PIPE, check=True)
                    self.compiler_ = result.stdout.decode().strip()
                    return
                except subprocess.CalledProcessError:
                    continue
            else:
                try:
                    result = subprocess.run(
                        ['where', name], stdout=subprocess.PIPE, check=True)
                    self.compiler_ = result.stdout.decode().split('\r\n')[
                        0].strip()
                    return
                except subprocess.CalledProcessError:
                    continue
        raise exceptions.UndefinedCompiler(
            self.compiler_, self.language_)

    def add_libraries(self, dir='') -> None:
        '''
        Adds files with {".h", ".cpp", ".c", ".hpp"}
        in directory and subdirectories.

        Params:
        dir: str, path to the directory with files.
        
        Returns: None.
        '''
        dir = Path()
        for entry in dir.glob('**/*'):
            if entry.is_file() and (entry.name[entry.rfind('.'):] in FILE_EXTENSIONS):
                self.libraries.append(str(entry.absolute()))

    def add_library(self, header_path, source_path) -> None:
        header_path, source_path = Path(header_path), Path(source_path)
        for path in (header_path, source_path):
            if path.is_file():
                absolute_path = str(path.absolute())
                if absolute_path not in self.libraries:
                    self.libraries.append(absolute_path)
    



    def set_compile_mode():
        pass

    def build():
        pass
