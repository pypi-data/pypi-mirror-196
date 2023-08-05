installify
Installify is a Python package that allows you to easily create a setup file for your Python program. With Installify, you can quickly create a self-contained installer that includes your program and all its dependencies, making it easy to distribute your program to others.

Installation
You can install Installify using pip:

pip install installify

Usage:

import installify

installify.install("https://example.com/myprogram.zip", "MyCompany", "MyProgram")
The install function takes three arguments:

url: The URL of the zip file to be downloaded and extracted.
company: The name of the company that developed the program.
program: The name of the program to be installed.

Example:

import installify

installify.install("https://example.com/myprogram.zip", "MyCompany", "MyProgram")

This will download the zip file from https://example.com/myprogram.zip, extract it, create a new folder named MyCompany in the AppData\Roaming directory, and extract the contents of the zip file to a new folder named MyProgram inside the MyCompany folder.