import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'aiy_voice', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version

setup(
    name='aiy_voice',
    version=get_version(),
    packages=['aiy_voice'],
    url='https://github.com/builderjer/aiy-voice-python',
    install_requires=["requirements.txt"],
    package_data={'': package_files('aiy_voice')},
    include_package_data=True,
    license='Apache-2.0',
    author='builderjer',
    author_email='builderjer@gmail.com',
    description='Scripts from google-aiyprojects collected into voice package',
    long_description='Scripts from google-aiyprojects without google-assistant requirements'
)
