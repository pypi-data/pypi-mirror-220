from setuptools import setup, find_packages

setup(name="message_client_learning_proj",
      version="0.0.1",
      description="message_client_learning_proj",
      author="Alexandr Nikiforov",
      author_email="8712060@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )