import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="tic_tac_game",
    version="0.0.1",
    author="Bekhruz",
    author_email="iutstudent2022@gmail.com",
    packages=["tic_tac_game"],
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/BehruzYBF/tic_tac_game",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)