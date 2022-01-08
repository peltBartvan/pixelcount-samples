import os

os.chdir(os.path.dirname(__file__))
command = 'voila ' + 'frontend.ipynb'
os.system(command)
