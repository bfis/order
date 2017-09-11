<img src="https://raw.githubusercontent.com/riga/order/master/logo.png" alt="order logo" width="250"/>

[![Build Status](https://travis-ci.org/riga/order.svg?branch=master)](https://travis-ci.org/riga/order) [![Documentation Status](https://readthedocs.org/projects/order/badge/?version=latest)](http://order.readthedocs.org/en/latest/?badge=latest) [![Package Status](https://badge.fury.io/py/order.svg)](https://badge.fury.io/py/order)


**Under development**


### Installation and dependencies

Via [pip](https://pypi.python.org/pypi/order):

```bash
pip install order
```

Currently, the only dependency is [scinum](https://github.com/riga/scinum) which is also installed with the above command.


### Contributing

If you like to contribute, I'm happy to receive pull requests. Just make sure to add a new test cases and run them via:

```bash
> python -m unittest tests
```


##### Testing

In general, tests should be run for different environments:

- Python 2.7
- Python 3.5
- Python 3.6


##### Docker

To run tests in a docker container, do:

```bash
git clone https://github.com/riga/order.git
cd order

docker run --rm -v `pwd`:/root/order -w /root/order -e python:3.6 python -m unittest tests
```


### Development

- Source hosted at [GitHub](https://github.com/riga/order)
- Report issues, questions, feature requests on [GitHub Issues](https://github.com/riga/order/issues)


### Authors

- [Marcel R.](https://github.com/riga)


### License

The MIT License (MIT)

Copyright (c) 2017 Marcel R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.