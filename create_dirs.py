import os

dirs = [
    'static',
    'static/css',
    'static/js',
    'static/images',
    'templates'
]

for dir in dirs:
    os.makedirs(dir, exist_ok=True)
