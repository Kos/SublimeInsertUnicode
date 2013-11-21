import sublime
import sublime_plugin
import collections
import os
from os.path import dirname, realpath

PACKAGE_NAME = 'InsertUnicode'
PACKAGE_DIR = dirname(realpath(__file__))

UNICODEDATA_FILENAME = os.path.join(PACKAGE_DIR, 'UnicodeData.txt')
BLOCKS_FILENAME = os.path.join(PACKAGE_DIR, 'Blocks.txt')
SETTINGS_FILENAME = 'InsertUnicode.sublime-settings'

UnicodeBlock = collections.namedtuple('UnicodeBlock', 'min max name')


def _read_block(line):
    minmax, name = line.split('; ')
    min_code, max_code = minmax.split('..')
    min_code = int(min_code, 16)
    max_code = int(max_code, 16)
    return UnicodeBlock(min=min_code, max=max_code, name=name)


def _read_blocks(lines):
    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            continue

        yield _read_block(line)


def _read_unicodedata_names(lines):
    for line in lines:
        line = line.strip()

        if not line:
            continue

        data = line.split(';')
        code = data[0]
        name = data[1]
        oldname = data[10]

        if name == '<control>':
            name = '<control>: {0}'.format(oldname)

        code = int(code, 16)
        yield (code, name)


_BLOCKS = list(_read_blocks(open(BLOCKS_FILENAME).readlines()))
_NAMES = dict(_read_unicodedata_names(open(UNICODEDATA_FILENAME).readlines()))


def _get_label(codeunit, fallback):
    """
    Returns a pretty label for the given code unit.
    Uses a fallback name if not found in data
    """

    name = _NAMES.get(codeunit, fallback)
    char = chr(codeunit)
    code = hex(codeunit)
    return '[{code}] {char} {name}'.format(name=name, char=char, code=code)


def _insert_char(view, codeunits, code):
    if code == -1:
        return
    else:
        codeunit = codeunits[code]
        insertion = chr(codeunit)
        view.run_command('insert', {'characters': insertion})


class InsertUnicodeShowBlockListCommand(sublime_plugin.TextCommand):
    def _show_block_list(self):
        block_names = [b.name for b in _BLOCKS]

        def show_block(block):
            if block == -1:
                return
            else:
                codeunits = range(_BLOCKS[block].min, _BLOCKS[block].max - 1)
                block_names = [_get_label(codeunit, fallback='(unknown)')
                               for codeunit in codeunits]

                sublime.set_timeout(
                    lambda: self.view.window().show_quick_panel(
                        block_names,
                        lambda code: _insert_char(self.view, codeunits, code),
                        0),
                    10)

        self.view.window().show_quick_panel(block_names, show_block, 0)

    def run(self, edit):
        if _BLOCKS is None:
            sublime.status_message('{0}: Unicode _blocks not loaded'.format(
                PACKAGE_NAME))
            return
        else:
            self._show_block_list()


_SETTINGS = sublime.load_settings(SETTINGS_FILENAME)
_USER_CHARS = [int(char, 16) for char in _SETTINGS.get('user_characters')]


class InsertUnicodeShowUserListCommand(sublime_plugin.TextCommand):
    def run (self, edit):
        block_names = [_get_label(codeunit, fallback='(unknown)')
                       for codeunit in _USER_CHARS]

        self.view.window().show_quick_panel(
            block_names, 
            lambda code: _insert_char(self.view, _USER_CHARS, code),
            0)
