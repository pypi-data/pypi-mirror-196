import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name="matin",
                 version="0.1",
                 author="anonymous",
                 author_email="anonymous@anonymous.com",
                 description="A handy formatter for matplotlib",
                #  long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="http://www.example.com/~cschultz/bvote/",
                 project_urls={
                     "Bug Tracker": "http://bitbucket.org/tarek/distribute/issues/",
                 },
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 package_dir={"": "src"},
                 packages=setuptools.find_packages(where="src"),
                 python_requires=">=3.6",
                 install_requires=['matplotlib'],
                 package_data={"": ["*.ttf"]})
