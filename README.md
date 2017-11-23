
# Sticky :question: :exclamation:
[![Build Status](https://travis-ci.org/ShinyTrinkets/Sticky.svg?branch=master)](https://travis-ci.org/ShinyTrinkets/Sticky) [![codecov](https://codecov.io/gh/ShinyTrinkets/Sticky/branch/master/graph/badge.svg)](https://codecov.io/gh/ShinyTrinkets/Sticky) ![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)

> Library for adding "sticky" comment headers inside Python source code files.


## Installation

This project uses [Python 3.5+](https://www.python.org/) and [pip](https://pip.pypa.io/). A [virtual environment](https://virtualenv.pypa.io/) is strongly encouraged.

```sh
$ pip install git+https://github.com/ShinyTrinkets/Sticky
```


## Usage

An example is worth 1000 words.

The source file, before:

```python
import os

print('Yuck')
```

Call the Sticky library:

```sh
$ python3 -m sticky.cli -s yourfile.py
```

The file, after the default header was added:

```python
#- rev: v1 -
#- hash: 9AUQHT -

import os

print('Yuck')
```

The header is customizable (work in progress). In the future, you might also add:

* a copyright in all your files
* the last username that changed the file
* the date of the last file change
* a history of all revisions by date and/or user
* imagination is the limit ...


## Why ?

This library is not trying to replace Git, or whatever version control system you're using.

In case of a normal Python library, the "sticky" headears allow quick overview of the separate modules (files) from that library, based on the revision number.
Also, in case of hundreds of modules, it's easy to automate the creation of standard headers inside all the files.

In this case, the development flow would be: lint the code, test the code. When it's ready to commit, call the "sticky icky" library to update the old comment headers.

But a better use-case is when the source file is shared in a place where versioning is not possible, or is hard to check. For example, a Gist-like/ Pastebin-like website, or an [IPFS](https://ipfs.io/)-like link. In that case, ideally the "sticky" header would consist of: the revision number, the name of the author, maybe an e-mail, but most important, a verifiable signature of that source file, easy to validate with the public key of the author.


## How ?

The source file is split in 2 parts:

* head = the comments section and possibly some documentation
* tail = the actual code, starting from imports, or function and class definitions

The tail is never modified.
The head is searched for previous "sticky" headers and if there aren't any, they will be added for the first time.
If old headers are found, the HASH of tail is checked with the HASH from the old header and if it matches, it means the file was not changed, so the "sticky" header is just refreshed, in case the header template was changed.
But if the hashes differ, the revision is incremented and the new "sticky" header is written in the source file.

That's it.


## License

[MIT](LICENSE) © 2017 Cristi Constantin.
