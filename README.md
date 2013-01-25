# Sublime InsertUnicode

This module allows to find and insert Unicode characters by their name.

## HOWTO

Basic:

- Run "InsertUnicode: Show all blocks" to view the list of all Unicode blocks.
- Select a block to view its contents.
- Select a code point from the list to insert it under the cursor.

Still basic, but more comfy:

- Run "InsertUnicode: General punctuation" or another to directly jump into the given block.
- Open the `Default.sublime-commands` file to change which blocks are displayed in your command palette.
- Make some key bindings to the palettes you often use.

Use Sublime Text's fuzzy matching to find interesting symbols in the lists.

## Known issues

There's a [known bug][udb] in Sublime Text 2 that sometimes makes it impossible to import the `unicodedata` module. I'll try to work around that.

[udb]: www.sublimetext.com/forum/viewtopic.php?f=3&t=3462
