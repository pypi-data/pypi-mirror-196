import setuptools

install_requires = [
   "setuptools",
   "pydantic",
   "numpy"
]


setuptools.setup(
   name='xclientai',
   version='0.0.4',
   author='Marcos Rivera Martínez, Sarthak Langde, Glenn Ko, Subhash G N, Toan Do, Roman Ageev',
   author_email='marcos.rm@stochastic.ai, sarthak.langde@stochastic.ai, glenn@stochastic.ai, subhash.gn@stochastic.ai',
   description='',
   long_description_content_type="text/markdown",
   url="",
   classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
   ],
   package_dir={"": "src"},
   packages=setuptools.find_packages(where="src"),
   python_requires=">=3.6",
   install_requires=install_requires
)