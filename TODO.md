## Reporting
Warn the user if there's a SyntaxError using Vim echoerr


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
