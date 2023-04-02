import subprocess
import platform
import os
import exceptions


class Builder():
    def __init__(self, language='cxx', compiler_path=''):
        '''
        Base builder for C/C++ projects.\n
        Params:\n
        language - str is one of for C++: {'c++', 'c plus plus', 'cplusplus', 'cxx'}, for C: {'c'}, sets language mode;\n
        compiler
        '''
        self.set_language(language)
        self._OS_NAME = os.name()
        self._OS_ARCHITECTURE = platform.architecture()
        
        self.set_compiler_path(compiler_path)
        

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
                return key
        raise Exception()

  

    def set_compiler_path(self, path) -> str:
        if path:
            self._compiler = path
            return self._compiler
        else:
            self._set_compiler_path()

    def _set_compiler_path(self) -> None:
        compiler_names = tuple()
        if self._language == 'C++':
            compiler_names = ('g++', 'clang++', 'icpc')
        else:
            compiler_names = ('gcc', 'clang', 'icc')
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
        raise exceptions.UndefinedCompilerException(self._compiler, self._language)

        