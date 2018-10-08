- Make the tool not require you to be on the exact indent for it to grab the
  current block!
- Add functions and classes as "blocks"
- Add `parso` directly to this plugin
- Implement per-block config
- Warn the user if there's a SyntaxError using Vim echoerr


## Block searching needs improvement

Right now, the row and column of the cursor is being used to determine which
block to select. This is very annoying and time-consuming because it means that
you have to be on the right indent to make the tool work.

Change it to just use rows, instead!


## Search Customization

Right now, searching only goes in this order:

whitespace
source-code
comments

If the selection is affected if things appear out of order.

Either it should not care what order it finds blocks in or, at the very least,
there should be a setting so that the user can customize searching for how they
like to work.


## Block Identifier Definitions
vaB should grab neighboring blocks if they ONLY define identifiers in the
current block.

But they should not if they definte the block + do other things

Example 1:
	|start|try:
		functions = SETTINGS[key][block]
	except KeyError:
		functions = []

	for function in functions:
		|cursor|
		try:
			return function()
		except Exception:  # pylint: disable=broad-except
			pass|end|


Example 2:
	|start|try:
		functions = SETTINGS[key][block]
	except KeyError:
		functions = []

	for function in functions:
		|cursor|
		try:
			return function()
		except Exception:  # pylint: disable=broad-except
			pass|end|


Fix this error


```python
while False:
    # asdfasdfasdf
    asdfsd = 8

    for _ in range(10):

        asdfas

        # asdfasdfasdf
        # asdfasfd
        # thing

        if True:
            thing = 8
        elif False:

            pass

        elif True:
            another = '1232'

        else:
            # adfabsdf adf
            # asdfasfdasdf


            pass
        # asdfafsd

    whatever = "asdfsaf"
```

```python
def main():
    '''Run the main execution of the current script.'''

    thing = 0


    for index in range(10):
        index *= 2.02

        # No matter where the block is located or how complex the block is,
        # the tool will select the correct boundary for that block
        #

        try:
            for _ in range(0):
                |start|thing = 8  # <-- This doesn't work with vAb

                # vab = "Select the block plus the whitespace/comments above"
                # vAb = "Select the block plus the whitespace/comments above and whitespace below"
                # vib = "Select only the block (no whitespace/comments)"
                #

                if False:
                    pass

                    print('asdfasd')
                elif True:
                    print('asdfasd')
                else:

                    # asdfasdf
                    # asdfasdf

                    print()


                # More comments

            # And it works for the outer try/except, too
            thing = 0
        except Exception:
            pass
        else:
            print('asfasdf')

            # whatever
        finally:

            print('Okay. Now we are done')

    # The tool supports all of the following:
    #
    # 1. For-loops
    # 2. While-loops
    # 3. Try blocks
    # 4. If blocks
    #
    thing = 8


if __name__ == '__main__':
    main()
```
