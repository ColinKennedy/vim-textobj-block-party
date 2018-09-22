- Rename this repo to 'vim-textobj-block-party'
- Implement source-code line searching
- Implement the "search disabled" mappings
- Implement per-block config


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
