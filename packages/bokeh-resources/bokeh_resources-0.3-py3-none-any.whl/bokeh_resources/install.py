import os
import sys
from pathlib import Path
import bokeh
from notebook.nbextensions import install_nbextension

os.chdir(Path(__file__).parent)
alias = Path(install_nbextension('bokeh_resources')) / 'static'
target = Path(bokeh.__file__).parent / 'server' / 'static'
print(f'Creating symlink {alias}\n     pointing to {target}')
if alias.exists():
    if len(sys.argv) > 1 and sys.argv[1] in ('-f', '--force'):
        alias.unlink()
        print(f'Deleted symlink {alias}')
    else:
        print('Symlink already exists, exiting (use -f/--force to overwrite).')
        sys.exit(1)
if sys.platform == 'win32':
    os.system(f'mklink /j {alias} {target}')
else:
    alias.symlink_to(target)
print('Symlink created')
