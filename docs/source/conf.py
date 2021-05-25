# type: ignore
import sphinx_readable_theme
import os
import sys

current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../.."))
for x in os.walk(target_dir):
    sys.path.insert(0, x[0])
# sys.path.insert(0, target_dir)

# -- Project information -----------------------------------------------------

project = 'Anathema'
copyright = '2021, Jonathan Crum'
author = 'Jonathan Crum'
release = '1.0.0'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.ifconfig']
intersphinx_mapping = {}

templates_path = ['_templates']
exclude_patterns = ['_build']
source_suffix = '.rst'
master_doc = 'index'

html_theme_path = [sphinx_readable_theme.get_html_theme_path()]
html_theme = 'readable'
html_static_path = ['_static']
