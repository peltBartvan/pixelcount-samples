import os
from pkg_resources import resource_string

ipynb_path = resource_string(__name__, 'frontend.ipynb')
os.system('voila ' + ipynb_path)
