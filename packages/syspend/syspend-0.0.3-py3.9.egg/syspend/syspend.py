import sys
import pathlib

def syspend(file_name:str='SYSPEND_ROOT', relative_path:str='./'):
    _syspend(file_name, relative_path, pathlib.Path().resolve(), 'add')

def get_path(file_name:str='SYSPEND_ROOT', relative_path:str='./'):
    return _syspend(file_name, relative_path, pathlib.Path().resolve(), 'get')

def _syspend(file_name:str, relative_path:str, p, mode):
    if (p/file_name).exists():
        path = (p/relative_path).resolve()
        if mode == 'add':
            sys.path.append(path)
        elif mode == 'get':
            return str(path)
    else:
        if p == p.parent:
            sys.exit(f'syspend package error: {file_name} File Not Found.\r\n')
        else:
            return _syspend(file_name, relative_path, p.parent, mode)

# soon after calling import syspend, executes syspend method.
syspend()

if __name__ == "__main__":
    print(get_path())
    print(get_path('SYSPEND_ROOT', '../tools'))