#!/usr/bin/env python3
import curses
import os
import re

ALIAS_FILE = os.path.expanduser('~/.bash_aliases')

def load_aliases():
    aliases = []
    commands = []
    if os.path.exists(ALIAS_FILE):
        with open(ALIAS_FILE, 'r') as f:
            for line in f:
                match = re.match(r"alias\s+(\w+)=['\"](.*)['\"]", line.strip())
                if match:
                    aliases.append(match.group(1))
                    commands.append(match.group(2))
    return aliases, commands

def save_aliases(aliases, commands):
    with open(ALIAS_FILE, 'w') as f:
        f.write("# ~/.bash_aliases\n")
        for alias, cmd in zip(aliases, commands):
            f.write(f"alias {alias}='{cmd}'\n")

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    aliases, commands = load_aliases()

    current_row = 0
    mode = 'navigate'  # or 'edit'
    edit_col = None
    edit_text = ""

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Define box dimensions
        alias_box_x = 1
        alias_box_y = 1
        alias_box_width = (width // 2) - 2
        alias_box_height = height - 4

        command_box_x = width // 2 + 1
        command_box_y = 1
        command_box_width = (width // 2) - 2
        command_box_height = height - 4

        # Draw full rectangle border around alias box
        # Top border
        stdscr.addch(alias_box_y, alias_box_x, curses.ACS_ULCORNER)
        stdscr.hline(alias_box_y, alias_box_x + 1, curses.ACS_HLINE, alias_box_width - 1)
        stdscr.addch(alias_box_y, alias_box_x + alias_box_width, curses.ACS_URCORNER)

        # Bottom border
        stdscr.addch(alias_box_y + alias_box_height, alias_box_x, curses.ACS_LLCORNER)
        stdscr.hline(alias_box_y + alias_box_height, alias_box_x + 1, curses.ACS_HLINE, alias_box_width - 1)
        stdscr.addch(alias_box_y + alias_box_height, alias_box_x + alias_box_width, curses.ACS_LRCORNER)

        # Left and right borders
        for y in range(alias_box_y + 1, alias_box_y + alias_box_height):
            stdscr.addch(y, alias_box_x, curses.ACS_VLINE)
            stdscr.addch(y, alias_box_x + alias_box_width, curses.ACS_VLINE)

        # Draw full rectangle border around command box
        stdscr.addch(command_box_y, command_box_x, curses.ACS_ULCORNER)
        stdscr.hline(command_box_y, command_box_x + 1, curses.ACS_HLINE, command_box_width - 1)
        stdscr.addch(command_box_y, command_box_x + command_box_width, curses.ACS_URCORNER)

        stdscr.addch(command_box_y + command_box_height, command_box_x, curses.ACS_LLCORNER)
        stdscr.hline(command_box_y + command_box_height, command_box_x + 1, curses.ACS_HLINE, command_box_width - 1)
        stdscr.addch(command_box_y + command_box_height, command_box_x + command_box_width, curses.ACS_LRCORNER)

        for y in range(command_box_y + 1, command_box_y + command_box_height):
            stdscr.addch(y, command_box_x, curses.ACS_VLINE)
            stdscr.addch(y, command_box_x + command_box_width, curses.ACS_VLINE)

        # Titles
        stdscr.addstr(0, 2, "Aliases", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(0, width // 2 + 2, "Commands", curses.A_BOLD | curses.A_UNDERLINE)

        # Display entries
        for idx, (alias, cmd) in enumerate(zip(aliases, commands)):
            y = idx + alias_box_y + 2
            if y >= alias_box_y + alias_box_height - 1:
                break
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
            # Alias column
            stdscr.addstr(y, alias_box_x + 1, alias[:alias_box_width - 2])
            # Command column
            stdscr.addstr(y, command_box_x + 1, cmd[:command_box_width - 2])
            if idx == current_row:
                stdscr.attroff(curses.A_REVERSE)

        # Instructions
        stdscr.addstr(height - 2, 2, "Arrows: navigate | Enter: edit | A: add | D: delete | Q: quit | Bash Alias Editor v1.0 (BAE)", curses.A_DIM)

        if mode == 'navigate':
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current_row = max(0, current_row - 1)
            elif key == curses.KEY_DOWN:
                current_row = min(len(aliases) - 1, current_row + 1)
            elif key == ord('q') or key == ord('Q'):
                break
            elif key == ord('a') or key == ord('A'):
                # Add new alias
                aliases.append("new_alias")
                commands.append("command")
                current_row = len(aliases) -1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # Edit alias
                mode = 'edit'
                edit_col = 'alias'
                edit_text = aliases[current_row]
            elif key == curses.KEY_RIGHT:
                # Edit command
                mode = 'edit'
                edit_col = 'command'
                edit_text = commands[current_row]
            elif key == ord('d') or key == ord('D'):
                # Delete current alias
                if aliases:
                    # Confirm deletion
                    confirm = curses.newwin(3, 50, height//2 - 1, width//2 - 25)
                    confirm.box()
                    confirm.addstr(1, 2, f"Delete '{aliases[current_row]}'? (y/n)")
                    confirm.refresh()
                    c = confirm.getch()
                    if c in [ord('y'), ord('Y')]:
                        del aliases[current_row]
                        del commands[current_row]
                        if current_row >= len(aliases):
                            current_row = max(0, len(aliases) - 1)
                    del confirm
        elif mode == 'edit':
            curses.curs_set(1)
            stdscr.addstr(height -1, 2, f"Editing {edit_col}: {edit_text}")
            stdscr.clrtoeol()
            curses.echo()
            stdscr.move(height -1, len(f"Editing {edit_col}: ") + 2)
            new_text = stdscr.getstr().decode('utf-8')
            curses.noecho()
            curses.curs_set(0)
            if edit_col == 'alias':
                aliases[current_row] = new_text
            else:
                commands[current_row] = new_text
            mode = 'navigate'

        stdscr.refresh()

    # Save on exit
    save_aliases(aliases, commands)

if __name__ == '__main__':
    curses.wrapper(main)
