# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fishbones', 'fishbones.decompiler_builtins']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fishbones',
    'version': '0.3.1',
    'description': 'Library for implementing decompiled code.',
    'long_description': "# Fishbones\n\n[![build](https://github.com/sledgeh4w/fishbones/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/sledgeh4w/fishbones/actions/workflows/tests.yml)\n![PyPI](https://img.shields.io/pypi/v/fishbones)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fishbones)\n[![GitHub license](https://img.shields.io/github/license/sledgeh4w/fishbones)](https://github.com/sledgeh4w/fishbones/blob/main/LICENSE)\n\nFishbones is a library for implementing decompiled code with Python.\n\n## Requirements\n\n- Python 3.6+\n\n## Installation\n\n```\n$ pip install fishbones\n```\n\n## Usage\n\nFishbones defines some integer types with fixed size. You can use shorthand functions (`int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`) to create them.\n\n```python\nfrom fishbones import uint8\n\nv = uint8(0x53)\n```\n\nPointer operations are common in the decompiled code.\n\n```c\nunsigned __int8 data[8] = {71, 114, 97, 118, 105, 116, 117, 109};\n\nunsigned __int8 *p = data;\nunsigned __int8 v = p[4];\n\n*((unsigned __int32 *)p + 1) = v;\n```\n\nSo Fishbones provides `vptr`.\n\n```python\nfrom fishbones import vptr\n\ndata = bytearray([71, 114, 97, 118, 105, 116, 117, 109])\n\np = vptr(data, 'uint8')\nv = p.add(4).read()\n\np.cast('uint32').add(1).write(v)\n```\n\nIn some cases, decompilers may use their built-in functions in the output. Fishbones implements some of them. You can look up from `fishbones.decompiler_builtins`.\n\n```python\nfrom fishbones import uint32\nfrom fishbones.decompiler_builtins.ida import ror4\n\nv = uint32(0x53683477)\nv = ror4(v, 2)\n```\n",
    'author': 'Sh4w',
    'author_email': 'sh4w0911@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
