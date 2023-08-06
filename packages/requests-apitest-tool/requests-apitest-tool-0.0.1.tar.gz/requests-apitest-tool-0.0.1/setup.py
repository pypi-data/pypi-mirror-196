from setuptools import setup

setup(
    name="requests-apitest-tool",
    version="0.0.1",
    packages=['requests_apitest_tool'],
    install_requires=['requests'],
    author="ydd9090",
    author_email="hello2ydd9090@gmail.com",
    keywords=("interface", "automation", "testing", "requests"),
    description="Simplify interface testing",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ydd9090/requests-apitest-tool",
    include_package_data=True,
    platforms="any",
    entry_points='''
    [console_scripts]
    apitest-tool=requests_apitest_tool.cli:cli
    '''
)