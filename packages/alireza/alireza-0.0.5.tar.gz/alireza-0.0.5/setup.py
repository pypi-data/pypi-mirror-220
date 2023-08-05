from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Comprehensive Toolkit for Boosting Productivity in Python Frameworks Development'
LONG_DESCRIPTION = """This extensive toolkit is specifically designed to enhance productivity and streamline the development process 
when working with Python frameworks. With a wide range of powerful and time-saving tools at your disposal, it empowers developers to tackle 
complex challenges efficiently and effectively.From scaffolding projects to automating repetitive tasks, this toolkit offers an array of features that 
simplify common development workflows. It provides seamless integration with popular Python frameworks, 
offering an extensive collection of utilities, libraries, and modules tailored to enhance the capabilities of your chosen framework.
Unlock the potential of this comprehensive toolkit and enjoy benefits such as code generation, 
and much more. Whether you are working on web development, data science, or any other domain, this toolkit serves as a 
valuable companion throughout the entire development lifecycle.
Accelerate your Python framework projects, reduce development time, and increase code quality with this indispensable toolkit that caters 
to the diverse needs of developers, allowing them to focus on delivering exceptional results.
"""

# Setting up
setup(
    name="alireza",
    version=VERSION,
    author="Alireza Soroush",
    author_email="alirezasoroush@hotmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    keywords=['python', 'tools', 'framework', 'django',],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
