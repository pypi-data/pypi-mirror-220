
from setuptools import setup

setup()

"""Below is DEPRECATED for pyproject.toml"""
# from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
# with open("requirements.txt", "r", encoding="utf-8") as fh:
#     requirements = fh.read()

# setup(
#     name='pycompall',
#     version='0.1.13',
#     author='Kim Yongbeom',
#     author_email='yongbeom.kim@u.nus.edu',
#     license='<the license you chose>',
#     description='Wrapper around the python compileall utility.',
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url='https://github.com/Yongbeom-Kim/py-compiler',
#     py_modules=['pycompall', 'app.application'],
#     packages=find_packages(),
#     install_requires=[requirements],
#     python_requires='>=3.7',
#     classifiers=[
#         "Programming Language :: Python :: 3.11",
#         "Operating System :: OS Independent",
#     ],
#     entry_points='''
#         [console_scripts]
#         pycompall=pycompall:cli
#     '''
# )
