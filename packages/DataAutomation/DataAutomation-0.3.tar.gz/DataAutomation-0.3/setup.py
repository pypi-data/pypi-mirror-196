from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name = 'DataAutomation',
      version= '0.3',
      description= "Data Automation tool which helps to automate the boring process of data science task",
      packages= ['DataAutomation'],
      author= 'Himanshu R Singh',
      zip_safe= False,
	long_description=long_description,
      long_description_content_type="text/markdown",
)
