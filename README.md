
# Sticky :question: :exclamation:
[![Build Status](https://travis-ci.org/croqaz/Sticky.svg?branch=master)](https://travis-ci.org/croqaz/Sticky) [![codecov](https://codecov.io/gh/croqaz/Sticky/branch/master/graph/badge.svg)](https://codecov.io/gh/croqaz/Sticky)

## What is this ?

This library is adding comment headers inside Python source code files.

Before:

```python
import os

print('Yuck')
```

After adding the default header:

```python
#- rev: v1 -
#- hash: 9AUQHT -

import os

print('Yuck')
```

That's it! And it's customisable. You could also add:

* a copyright in all your files
* the last username that changed the file
* the date of the last file change
* a history of all revisions by date and/or user
* imagination is the limit ...

## Why ?

This library is not trying to replace Git, or whatever version control system you're using.

The idea is to have a quick overview of the separate modules (files) you have inside your library, based on the revision number and to automate the creation of standard headers inside all your files.

## How ?

The Python source file is split in 2 parts:

* head = the comments section and possibly some documentation
* tail = the actual code, starting from imports, or function and class definitions

The tail is never modified.
The head is searched for previous "sticky" headers and if there aren't any, they will be added for the first time.
If old headers are found, the HASH of tail is checked with the HASH from the old header and if it matches, it means the file was not changed, so the "sticky" header is just refreshed, in case the header template was changed.
But if the hashes differ, the revision is incremented and the new "sticky" header is written in the source file.

That's it.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Copyright (c) 2017 Cristi Constantin.
