from setuptools import setup, find_packages

setup(
    name='langproxy',
    version='0.0.1',
    description='Language Model Proxy',
    author='jaypark',
    author_email='jaypark@gmail.com',
    url='https://github.com/jinto/langproxy',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['chatbot','ai','ml','llm'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
