from setuptools import setup, find_packages

setup(
    name='proplogic',
    version='0.0.2',
    url = "https://github.com/ryoryon66/propositional_logic_expr_parser",
    author = "ryoryon66",
    description="A simple propositional logic parser and visualizer",
    long_description="A simple propositional logic parser and visualizer. Evaluation is implemented in visiter pattern.",
    license="MIT",
    packages=find_packages(),
    install_requires = [
                        "networkx==3.0",
                        "pygraphviz==1.10",
                        "pytest==7.2.2",
        ],
)