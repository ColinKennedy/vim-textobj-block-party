textobj-block-party
===================

Vim has many tools for Python. There are text objects for indentation, classes,
functions, and more. But have you ever wanted to delete an try/except block in
Python and found it difficult? If so, Block Party is hear to help!

Usage
-----

- Open any Python file.
- Position your cursor inside a Python block that you want to select (like an
  if statement, for example).
- Press "vab" or whatever your mappings are set to.
- The block will now be selected!

Here's Block Party, in action:
TODO: Put a GIF or asciinema here


Note: If the Python file being operated upon has a SyntaxError then the file
cannot be parsed and block selection will fail.


Requirements
------------

* [textobj-user][1] Vim plugin, at least version AUTHORNOTE which version?

[1]: https://github.com/kana/vim-textobj-user


Installation
------------

Install everything in the "Requirements" section and then install
vim-textobj-block-party using a plugin manager or manually.

Plugin Manager Installation
---------------------------

I use [vim-plug](TODO: URL HERE) to install all of my plugins. The code to add
it below looks like this:

```vim
TODO
```

Manual Installation
-------------------

Clone this repository:

```bash
TODO
```
Move the files to their respective folders in your `~/.vim` directory
(or your `$HOME\vimfiles` directory if you're on Windows)


Contributing
------------

TODO
