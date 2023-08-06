from distutils.core import setup

setup(
    name='lemonbar',
    packages=['lemonbar'],
    version='0.6.0',
    license='MIT',
    description='A Python API for interacting with Lemonbar',
    author='Ori Harel',
    author_email='oeharel@gmail.com',
    url='https://github.com/Heknon/lemonbar-api',
    download_url='https://github.com/Heknon/lemonbar-api/archive/refs/tags/v0.6.0.tar.gz',
    keywords=['lemonbar', 'api', 'lemonbar-api', "arch", "linux"],
    install_requires=[
        'pydantic',
        'screeninfo',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
)
