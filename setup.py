from setuptools import setup
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name='git-svn-merge',
    version='1.0.0',
    description='Automate Git branch merge into SVN trunk with interactive conflict resolution',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/git-svn-merge-automation',
    py_modules=['merge_to_svn'],
    entry_points={
        'console_scripts': [
            'merge-svn=merge_to_svn:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    keywords='git svn merge automation tortoisegit version-control',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/git-svn-merge-automation/issues',
        'Source': 'https://github.com/yourusername/git-svn-merge-automation',
        'Donate': 'https://paypal.me/ruggierocarlo',
    },
)
