import subprocess
import platform
import os
import exceptions
from pathlib import Path


FILE_EXTENSIONS = ('cpp', 'c', 'h', 'hpp')
C_COMPILER_NAMES = ('gcc', 'clang', 'icc')
CXX_COMPILER_NAMES = ('g++', 'clang++', 'icc')

class Builder():
    def __init__(self, mainfile='', language='cxx', compiler_path='', compile_mode=''):
        '''
        Base builder for C/C++ projects.\n
        Params:
        mainfile - path to file with main function;
        language - str is one of for C++: {'c++', 'c plus plus', 'cplusplus', 'cxx'}, for C: {'c'}, sets language mode;
        compiler_path - path to compiler on computer.
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
        Method to set language mode.\n
        language is one of C++: {'c++', 'c plus plus', 'cplusplus', 'cxx'}, for C: {'c'}\n
        Returns language.\n
        Raises exception if language is undefined.\n
        '''
        languages = {'C++': ('c++', 'c plus plus',
                             'cplusplus', 'cxx'), 'C': ('c',)}
        for key, values in languages:
            if language.lower() in values:
                self._language = key
                return self._language
        raise exceptions.UndefinedLanguageMode(language)

    def set_compiler_path(self, path) -> str:
        if path:
            self._compiler = path
            return self._compiler
        else:
            self._set_compiler_path()

    def _set_compiler_path(self) -> None:
        if self._language == 'C++':
            compiler_names = CXX_COMPILER_NAMES
        else:
            compiler_names = C_COMPILER_NAMES
        
        for name in compiler_names:
            if self._OS_NAME == 'posix':
                try:
                    result = subprocess.run(
                        ['which', name], stdout=subprocess.PIPE, check=True)
                    self._compiler = result.stdout.decode().strip()
                    return
                except subprocess.CalledProcessError:
                    continue
            else:
                try:
                    result = subprocess.run(
                        ['where', name], stdout=subprocess.PIPE, check=True)
                    self._compiler = result.stdout.decode().split('\r\n')[
                        0].strip()
                    return
                except subprocess.CalledProcessError:
                    continue
        raise exceptions.UndefinedCompiler(
            self._compiler, self._language)

    def add_libraries(self, dir='') -> None:
        dir = Path()
        for entry in dir.glob('**/*'):
            if entry.is_file() and (entry.name[entry.rfind('.'):] in FILE_EXTENSIONS):
                self.libraries.append(str(entry.absolute()))

    # def add_library(self, header_path, source_path) -> None:
    #     header_path, source_path = Path(header_path), Path(source_path)
    #     if header_path.is_file() and (header_path.name.split('.')[-1] in FILE_EXTENSIONS):
    #         self.libraries.append(header_path.absolute())
    #     else:
    #         pass



    def set_compile_mode():
        pass

    def build():
        pass
