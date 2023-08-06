from setuptools import setup, find_packages

setup(
    name='passwgeneration',       # Replace with the name of your package
    version='1.1.7',                # Replace with the version number of your package
    author='kanchan',             # Replace with the author's name
    author_email='kanchanbora321@gmail.com',  # Replace with the author's email
    description='Python package to generate random passwords of maximum length 12, avoiding names present in specified files.',
    long_description='generate password',  # Use README.md content or plain text
    long_description_content_type='text/plain',  # Specify the type of long description (text/plain, text/markdown, etc.)
    url='https://github.com/kanchann23/genUniquePassw',  # Replace with the URL of your package's repository
    license='MIT',                  # Replace with the license type of your package
    keywords=['security', 'password'],  # Replace with relevant keywords related to your package
    packages=find_packages(),       # Automatically find and include all packages in the project
   
    classifiers=[                   # List of classifiers to categorize your package on PyPI
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

