from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Spam Anything Anywhere You Want :)'
LONGDESCRIPTION = """import bomb
bomb.spam("Text", Number , Time (The Time That You Need To Choose The Target))"""

# Setting up
setup(
    name="bomper",
    version=VERSION,
    author="DrMowz",
    author_email="<drmowz8585@gmail.com>",
    description=DESCRIPTION,
    long_description=LONGDESCRIPTION,
    packages=find_packages(),
    install_requires=['pyautogui'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)