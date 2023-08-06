from setuptools import setup, find_packages

setup(
    name='proplogic',
    version='0.0.3',
    url = "https://github.com/ryoryon66/propositional_logic_expr_parser",
    author = "ryoryon66",
    description="A simple propositional logic parser and visualizer",
    long_description="""
    A simple propositional logic parser and visualizer. You can visualize AST of expressions by using visualize_logical_expression function. Propositional variables should be written string with alphabets.Evaluation is implemented in visiter pattern.
    """,
    license="MIT",
    packages=find_packages(),
    install_requires = [
                        "networkx==3.0",
                        "pygraphviz==1.10",
                        "pytest==7.2.2",
        ],
)