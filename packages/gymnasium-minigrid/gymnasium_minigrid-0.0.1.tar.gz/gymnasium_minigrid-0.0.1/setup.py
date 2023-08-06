from setuptools import setup, find_packages

def get_description():
    """Gets the description from the readme."""
    with open("README.md") as fh:
        long_description = ""
        header_count = 0
        for line in fh:
            if line.startswith("##"):
                header_count += 1
            if header_count < 2:
                long_description += line
            else:
                break
    return long_description
print(get_description())
setup(
    name='gymnasium_minigrid',
    version='0.0.1',
    description='A mini grid environment for OpenAI Gym and Gymnasium',
    author='Lucas Bertola',
    # author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'pygame==2.1.3',
        'gymnasium==0.28.1',
    ]
)