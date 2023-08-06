from setuptools import setup, find_packages

# with open('requirements.txt', 'r', encoding='utf-8') as f:
#     requirements = f.readlines()
# requirements = [r.strip() for r in requirements if not r.startswith('#')]

# # Remove version numbers
# requirements = [r.split('==')[0] for r in requirements]

setup(
    name='pixeo',
    version='1.0.0',
    use_scm_version=True,
    packages=find_packages(),
    # install_requires=requirements,
    url='https://github.com/furacas/pixeo',
    license='',
    author='furacas',
    author_email='s.furacas@outlook.com',
    description='An automated game scripting framework',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
)
