textobj-block-party
===================

Vim has many tools for Python. There are text objects for indentation, classes,
functions, and more. But have you ever wanted to delete an try/except block in
Python and found it difficult? If so, Block Party is here to help!

Using Block Party, to delete this block of code, you just need to type `dab`.


```python
for index in range(10):
    if index in self.thing:
        print('breaking')

        run_something()

        break
else:
    print('Did not break')
```

To delete the next block, you type `dab`.


```python
while True:
    print('doing stuff')

    time.sleep(1)
```

How about this try/except/else/finally block? Still `dab`!


```python
try:
    some_function()

    self.foo = 8
except ValueError:
    # Don't worry about it
    pass
except TypeError:
    # You ain't my type!

    pass
else:
    print('you get the point')

    print('the block is complicated')
finally:



    LOGGER.info('Loggin stuff and what not')
```

Alright, lets see if you can guess what you need to type to delete
this if-elif-else block.

```python
if foo():
    print('Got foo')
elif bar():
    print('Got bar')
else:
    print('Game over man! Game over!')
```

That's right! It's `dab` again!

![](http://pithytees.com/wp-content/uploads/2017/03/mmj-dab-bad-weed-wear-that-design.jpg)

You'll be `dab`ing all day and night at the Block Party!


Usage
-----

- Open any Python file.
- Position your cursor inside a Python block that you want to select (like an
  if statement, for example).
- Type `vab`
- The block will now be selected!
- Pressing `d` will delete the selected text. Or just use `dab`, as a short-hand.

Here's Block Party, in action:

[![asciicast](https://asciinema.org/a/206550.png)](https://asciinema.org/a/206550)

The full list of supported Python block types:

    for
    if
    try
    while

Note: If the Python file being operated upon has a SyntaxError then the file
cannot be parsed and block selection will fail.


Requirements
------------

* [parso][1] A Python parser which is the main work-horse of this plugin
* [textobj-user][2] A Vim plugin which creates our mappings

[1]: https://pypi.org/project/parso
[2]: https://github.com/kana/vim-textobj-user

Note:
    If no parso can be found, Block Party will try to provide its own. But
    it's better to just install parso, properly.


Installation
------------

Install everything in the "Requirements" section and then install
vim-textobj-block-party using a plugin manager or manually.


Plugin Manager Installation
---------------------------

I use [vim-plug](https://github.com/junegunn/vim-plug) to install
all of my plugins. The code to add it below looks like this:

```vim
Plug 'ColinKennedy/vim-textobj-block-party'
```

However this plugin should work with any plugin manager.


Manual Installation
-------------------

Clone this repository:

```bash
git clone https://github.com/ColinKennedy/vim-textobj-block-party
```

Move the files to their respective folders in your `~/.vim` directory
(or your `$HOME\vimfiles` directory if you're on Windows)


Customizations
--------------

Block Party exposes the following mappings

    +--------+--------------------------------------------+
    |  Keys  |                  Mapping                   |
    +--------+--------------------------------------------+
    | ib     | <Plug>(textobj-block-party-shallow-i)      |
    | ab     | <Plug>(textobj-block-party-shallow-a)      |
    | iB     | <Plug>(textobj-block-party-deep-i)         |
    | aB     | <Plug>(textobj-block-party-deep-a)         |
    | Ab     | <Plug>(textobj-block-party-two-way-a)      |
    | AB     | <Plug>(textobj-block-party-deep-two-way-a) |
    +--------+--------------------------------------------+

Each mapping does slightly different things. The diagram below should give a
good idea of each mapping's properties.

    import os
                                                                -+   -+
                                                                 |    |
    # Some list of items                                         |    |
    # Honestly it could say anything though.                     |    |
    #                                                            |    |
    items = ['foo', 'bar', 'end', 'start']                       |    |
                                                    -+   -+      |    |
                                                     |    |      |    |
                                                     |    |      |    |
    for item in items:                         -+    |    |      |    |
        # Some information                      |    |    |      |    |
        print('Item {}'.format(item))           |    |    |      |    |
                                                |    |    |      |    |
        item += '.'                             |    |    |      |    |
        >                                       | ib | ab | Ab   | aB | AB
        if item == 'end.':                      |    |    |      |    |
            break                               |    |    |      |    |
                                                |    |    |      |    |
    else:                                       |    |    |      |    |
        print('Break never executed')          -+   -+    |     -+    |
                                                          |           |
                                                         -+          -+
    more = 'code'


Please note that `ab`, `aB`, `Ab`, and `AB` mappings have slightly different
results, depending on your set configuration. See the
[docs page](/doc/textobj-block-party.txt) for more details about that.

    +--------------------------------------+---------+-----------------------------+
    |               Variable               | Default |         Description         |
    +--------------------------------------+---------+-----------------------------+
    | g:vim_block_party_include_comments   |   '1'   | Look for comments above     |
    |                                      |         | the current block           |
    |                                      |         |                             |
    | g:vim_block_party_include_whitespace |   '1'   | Look for whitespace         |
    |                                      |         |                             |
    | g:vim_block_party_search             |   '1'   | Look for source-code that's |
    |                                      |         | related to the block        |
    |                                      |         |                             |
    | g:vim_block_party_greedy             |   '0'   | If 0 search for source-code |
    |                                      |         | If 1 search the block's     |
    |                                      |         | contents for source-code    |
    +--------------------------------------+---------+-----------------------------+


## Feature Request And Bug Reports
Feature requests and bug fixes should both follow the same format:

If the post is related to how blocks are selected or deleted and is a bug,
for example, it's best to post a block of code and show where the block
selection starts and ends and then show where you expected that block to
start and end. Then explain why you think it's an error.

Please use `|start|` to make the start of a block, `|cursor|` to make where the
user's cursor would be, and `|end|` for where the block ends.

Finally, run `BlockPartyDebug` in your Vim session and add its output to the post.

This is an example bug report:

    Hi,

    Block Party isn't working properly with this block of code:

    What I expected:

        def foo():
            |start|for _ in range(10):
                # Some comment here
                |cursor|
                pass|end|


    What actually happened:

        def foo():
            for _ in range(10):
                |start|# Some comment here
                |cursor|
                pass|end|

    BlockPartyDebug Output:

        Block Party Version: 1.0.0
        let g:vim_block_party_include_comments = '1'
        let g:vim_block_party_include_whitespace = '1'
        let g:vim_block_party_search = '1'
        let g:vim_block_party_greedy = '0'


## Contributing
If you have improvements that you'd like to add, please feel free to fork this
repo, and submit a PR with your edits. Contributions are welcome!
