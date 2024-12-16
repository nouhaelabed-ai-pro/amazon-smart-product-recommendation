import os

screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)
