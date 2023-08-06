from setuptools import setup, find_packages

setup(
    name='zuicorn',
    version='1.0.4',
    description='A WSGI server designed & developed for ZYLO Python web Framework.',
    author='Pawan kumar',
    author_email='control@vvfin.in',
    url='https://github.com/E491K7/zuicorn',
    packages=find_packages(),
    install_requires=['gevent', 'colorama', 'python-daemon', 'zylo-admin', 'zylo'],  
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "zuicorn = zuicorn.wsgi:main"
        ]
    },
)
