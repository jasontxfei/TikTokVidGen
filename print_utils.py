import builtins
colors = {'black': '\033[30m', 'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m', 'blue': '\033[34m', 'magenta':'3\033[5m', 'cyan': '\033[36m', 'white': '\033[37m', 'default': '\033[39m', 'reset': '\033[0m'}
bg_colors = {'black': '\033[40m', 'red': '\033[41m', 'green': '\033[42m', 'yellow': '\033[43m', 'blue': '\033[44m', 'magenta':'4\033[5m', 'cyan': '\033[46m', 'white': '\033[47m', 'default': '\033[49m'}

def print(*values, color=None, bg_color=None, replace=None, sep=None, end=None, file=None, flush=None):
    '''Custom print function with replacement and coloring.'''
    if replace: builtins.print('\033[1A\033[2K', end='', file=file, flush=flush)
    builtins.print(colors[color if color else 'default'], end='', file=file, flush=flush)
    builtins.print(bg_colors[bg_color if bg_color else 'default'], end='', file=file, flush=flush)
    builtins.print(*values, sep=sep, end=end, file=file, flush=flush)
    builtins.print(colors['default'], end='', file=file, flush=flush)
    builtins.print(bg_colors['default'], end='', file=file, flush=flush)

def printr(*values):
    '''Custom print function with replacement.'''
    builtins.print('\033[1A\033[2K', end='')
    builtins.print(*values)
    
def printc(*values, color: str = None, bg_color: str = None):
    '''Custom print function with coloring.'''
    builtins.print(colors[color if color else 'default'], end='')
    builtins.print(bg_colors[bg_color if bg_color else 'default'], end='')
    builtins.print(*values)
    builtins.print(colors['default'], end='')
    builtins.print(bg_colors['default'], end='')

def saveCursor():
    '''Saves cursor position in terminal. Use `restoreCursor()` to move the cursor back.'''
    builtins.print('\033[s', end='')

def restoreCursor():
    '''Restores cursor position to the previously saved position with `saveCursor()`. Clears text printed in terminal up
       to saved cursor position.'''
    builtins.print('\033[u\033[0J', end='') 