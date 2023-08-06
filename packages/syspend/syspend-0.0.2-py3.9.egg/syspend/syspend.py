import sys
import pathlib

def syspend(file_name:str='SYSPEND_ROOT', relative_path:str='./'):
    _syspend(file_name, relative_path, _get_search_path(), 'add')

def get_path(file_name:str='SYSPEND_ROOT', relative_path:str='./'):
    return _syspend(file_name, relative_path, _get_search_path(), 'get')

def _get_search_path():
    if '__file__' in globals():
        path = pathlib.Path(__file__).parent.resolve()
    else:
        path = pathlib.Path().resolve()
    return path

def _syspend(file_name:str, relative_path:str, p, mode):
    if (p/file_name).exists():
        if mode == 'add':
            sys.path.append(str(p/relative_path))
        elif mode == 'get':
            return str(p/relative_path)
    else:
        if p == p.parent:
            sys.exit(f'syspend package error: {file_name} File Not Found.\r\n')
        else:
            return _syspend(file_name, relative_path, p.parent, mode)

# syspend を import したと同時に SYSPEND_ROOT があるフォルダを sys.append します。
syspend()

if __name__ == "__main__":
    print(get_path())