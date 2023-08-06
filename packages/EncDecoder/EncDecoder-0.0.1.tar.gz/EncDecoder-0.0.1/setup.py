from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Enncode Or Decode Everything'
LONGDESCRIPTION = "You Can Encode Anything By Using (enc(File Address.txt or .mp4 or...)) And Decode That With (dec(File Address.txt or .mp4 or...))"

# Setting up
setup(
    name="EncDecoder",
    version=VERSION,
    author="DrMowz",
    author_email="<drmowz8585@gmail.com>",
    description=DESCRIPTION,
    long_description=LONGDESCRIPTION,
    packages=find_packages(),
    install_requires=['cryptography'],
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