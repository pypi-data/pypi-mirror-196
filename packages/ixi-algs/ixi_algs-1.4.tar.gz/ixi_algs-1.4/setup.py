from setuptools import setup
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='ixi_algs',
      version='1.4',
      description='ixi_algs',
      packages=['ixi_algs'],
      author_email='zxcbbtihs37docxh@yandex.ru',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ixslea/ixi_algs",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
      ],
    
      python_requires='>=3.6')