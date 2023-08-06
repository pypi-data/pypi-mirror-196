Very simple Python library for color and formatting in terminal.
Collection of color codes and names for 256 color terminal setups.
The following is a list of 256 colors for Xterm, containing an example
of the displayed color, Xterm Name, Xterm Number and HEX.
The following colors works with most terminals and terminals emulators.
ANSI/VT100 escape sequences can be used in every programming languages.

Attributes:

.. code-block:: bash

    +-----+------------------+
    |Code | Description      |
    +-----+------------------+
    |  1  | bold             |
    |  2  | dim              |
    |  4  | underlined       |
    |  5  | blink            |
    |  7  | reverse          |
    |  8  | hidden           |
    |  0  | reset            |
    |  21 | res_bold         |
    |  22 | res_dim          |
    |  24 | res_underlined   |
    |  25 | res_blink        |
    |  27 | res_reverse      |
    |  28 | res_hidden       |
    +------------------------+

256 Colors Foreground (text):
256 Colors Background:
Installation
------------

.. code-block:: bash

    $ pip install colarise --upgrade

    uninstall

    $ pip uninstall colarise


Dependencies
------------

None, only Python programming language.

Usage Examples
--------------

How to use the module in your own python code:

.. code-block:: bash

    >>> from colarise import fg, bg, attr
    >>>
    >>> print(f'{fg(1)} Hello World !!! {attr(0)}')
     Hello World !!!
    >>>
    >>> print(f'{fg(1)}{bg(15)} Hello World !!! {attr(0)}')
     Hello World !!!

Use description:

.. code-block:: bash

    >>> print(f'{fg("white")}{bg("yellow")} Hello World !!! {attr("reset")}')
     Hello World !!!
    >>>
    >>> print(f'{fg("orchid")}{attr("bold")} Hello World !!! {attr("reset")}')
     Hello World !!!
    >>>
    >>> color = bg('indian_red_1a') + fg('white')
    >>> reset = attr('reset')
    >>> print(color + 'Hello World !!!' + reset)
    Hello World !!!

Or use HEX code:

.. code-block:: bash

    >>> color = fg('#C0C0C0') + bg('#00005f')
    >>> res = attr('reset')
    >>> print(color + "Hello World !!!" + res)
    Hello World !!!

Or the convenient `stylize(text, *styles)` wrapper to save some keystrokes:

.. code-block:: bash

    >>> import colarise
    >>> from colarise import stylize
    >>> print(stylize("This is green.", colarise.fg("green")))
    This is green.
    >>> print("This is not.")
    This is not.
    >>> angry = colarise.fg("red") + colarise.attr("bold")
    >>> print(stylize("This is angry text.", angry))
    This is angry text.
    >>> print(stylize("This is VERY angry text.", angry, colarise.attr("underlined")))
    This is VERY angry text.
    >>> print("But this is not.")
    But this is not.


