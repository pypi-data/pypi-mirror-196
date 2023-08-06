from setuptools import setup, find_packages

with open('README.rst',encoding='utf-8') as f:
    long_description = f.read()
print(find_packages()) 
setup(
    name='mk-blender-scr',
    packages=find_packages(),
    install_requires=[
        "ase",
        "ipywidgets<8.0",
        "Jinja2",
        "click",
        "nglview",
        "pandas",
        "ipython",
        "numpy"
        ], 
    version='1.0.8',
    author='Kato Taisetsu',
    url='https://shimi-lab.github.io/mk-blender-scr_Document/',
    description='Create a Python script for Blender from Atoms of ASE.',
    long_description=long_description,
    long_description_content_type='text/x-rst', # 'text/plain', 'text/x-rst', 'text/markdown'
    keywords='blender ase',
    entry_points={"console_scripts": ["mk-blender-scr = mk_blender_scr.command.cli:main"]},
)