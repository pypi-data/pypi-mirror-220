from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Simple tui slurm job viewer.'
LONG_DESCRIPTION = 'Simple tui slurm job viewer. Using /etc/hosts and ssh to get CPU and RAM utilization of all cluster nodes. Distrubuted using PIP and writen in python.'

# Setting up
setup(
        name="shtop", 
        version=VERSION,
        author="Lukáš Plevač",
        author_email="<lukas@plevac.eu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 

        scripts=['scripts/shtop'],

        keywords=['python', 'slurm', 'shtop', 'top', 'htop'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3"
        ]
)