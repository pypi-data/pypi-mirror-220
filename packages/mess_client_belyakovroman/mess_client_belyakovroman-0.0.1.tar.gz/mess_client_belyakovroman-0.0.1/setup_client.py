from setuptools import setup, find_packages

setup(name="mess_client_belyakovroman",
      version="0.0.1",
      description="mess_client_belyakovroman",
      author="Roman Belyakov",
      author_email="belyakov1981@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
