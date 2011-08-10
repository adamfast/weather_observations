from distutils.core import setup

setup(
    name = "weather_observations",
    url = "http://github.com/adamfast/weather_observations",
    author = "Adam Fast",
    author_email = "adamfast@gmail.com",
    version = "0.1",
    license = "BSD",
    packages = ["weathertracking"],
    description = "Utilities for collecting weather information.",
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)