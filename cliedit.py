import curses
import os
import sys

def editor(stdscr, filename):
    # Clear screen
    stdscr.clear()
    
    # Set up initial variables
    text = []
    current_line = 0
    current_col = 0
    viewport_start = 0  # Start of the visible text area

    # Define color pairs for bold text and white background
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Regular text with white background
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Bold text
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Filename text on white background
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_GREEN)


    def load_file():
        nonlocal text, current_line, current_col, viewport_start
        if os.path.exists(filename):
            text = [""]
            with open(filename, 'r') as f:
                text = f.readlines()
            text = [line.rstrip('\n') for line in text]
            current_line = 0
            current_col = 0
            viewport_start = 0  # Reset viewport when loading a file
        else:
            text = [""]  # Start with an empty line if the file doesn't exist

    def save_file():
        with open(filename, 'w') as f:
            for line in text:
                f.write(line + '\n')

    load_file()

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()  # Get terminal size
        
        # Display the filename in the middle with a white background
        filename_str = f"Editing: {filename}"
        filename_x = (width - len(filename_str)) // 2
        
        # Fill the entire line with a white background
        stdscr.attron(curses.color_pair(3))  # Use the white background color
        stdscr.addstr(0, 0, ' ' * (width - 1))  # Fill the line with spaces
        stdscr.attroff(curses.color_pair(3))  # Turn off the white background color
        
        # Print the filename in bold
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)  # Bold for the filename
        stdscr.addstr(0, filename_x, f"Editing: {filename}", curses.color_pair(4) | curses.A_BOLD)  # Bold filename
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)  # Turn off the bold

        # Display the text with line length limitation
        for i in range(viewport_start, min(viewport_start + height - 2, len(text))):  # Limit lines to screen height
            line = text[i][:width - 1]  # Limit line length to screen width
            
            if line.startswith(">>>"):  # Check if line starts with '>>>'
                stdscr.addstr(i - viewport_start + 1, 0, line, curses.A_BOLD)  # Add as bold
            elif line.startswith("*"):  # Check if line starts with '*'
                # Replace '*' with '•' and space out the item
                item_line = "  •  " + line[1:]  # Create spaced-out item line
                stdscr.addstr(i - viewport_start + 1, 0, item_line)  # Add as bold item
            elif line.startswith("-"):  # Check if line starts with '-'
                # Replace '-' with '•' and space out the item
                item_line = "  •  " + line[1:]  # Create spaced-out item line
                stdscr.addstr(i - viewport_start + 1, 0, item_line)  # Add as bold item
            else:
                stdscr.addstr(i - viewport_start + 1, 0, line)  # Add as normal text

        # Display shortcuts at the bottom with appropriate colors
        stdscr.attron(curses.color_pair(3))  # Color for F2 and F3
        stdscr.addstr(height - 1, 0, "")
        stdscr.addstr("ESC", curses.color_pair(3))  # F2 in color_pair(4)
        stdscr.attroff(curses.color_pair(3))
        stdscr.addstr(" Exit ")
        stdscr.attron(curses.color_pair(3))  # Color for F3
        stdscr.addstr("F2", curses.color_pair(3))  # F3 in color_pair(4)
        stdscr.attroff(curses.color_pair(3))
        stdscr.addstr(" Save ")
        stdscr.attron(curses.color_pair(3))  # Color for F3
        stdscr.addstr("F3", curses.color_pair(3))  # F3 in color_pair(4)
        stdscr.attroff(curses.color_pair(3))
        stdscr.addstr(" Load")

        # Display line and column numbers at the bottom right
        line_col_str = f"Line: {current_line + 1}, Col: {current_col + 1}"  # +1 to display human-readable positions
        stdscr.addstr(height - 1, width - len(line_col_str) - 1, line_col_str)

        # Ensure current_line is within bounds
        if current_line < len(text):
            # Correct position for items
            if text[current_line].startswith("*"):
                stdscr.move(current_line - viewport_start + 1, current_col + 4)  # Move cursor after the bullet point
            else:
                stdscr.move(current_line - viewport_start + 1, current_col)  # Move cursor to current position
        else:
            current_line = len(text) - 1
            current_col = len(text[current_line]) if text else 0
            stdscr.move(current_line - viewport_start + 1, current_col)

        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Handle different keys
        if key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
            if current_col > 0:
                if text[current_line].startswith("*") and current_col <= 4:
                    # If backspacing within the bullet point area, treat it specially
                    current_col = 0
                    text[current_line] = text[current_line][4:]  # Remove bullet point
                else:
                    text[current_line] = text[current_line][:current_col - 1] + text[current_line][current_col:]
                    current_col -= 1
            elif current_line > 0:
                current_col = len(text[current_line - 1])
                text[current_line - 1] += text[current_line]
                del text[current_line]
                current_line -= 1

        elif key == curses.KEY_DC:  # Handle delete
            if current_col < len(text[current_line]):
                text[current_line] = text[current_line][:current_col] + text[current_line][current_col + 1:]

        elif key == curses.KEY_LEFT:  # Move cursor left
            if current_col > 0:
                current_col -= 1
            elif current_line > 0:
                current_line -= 1
                current_col = len(text[current_line])

        elif key == curses.KEY_RIGHT:  # Move cursor right
            if current_col < len(text[current_line]):
                current_col += 1
            elif current_line < len(text) - 1:
                current_line += 1
                current_col = 0

        elif key == curses.KEY_UP:  # Move cursor up
            if current_line > 0:
                current_line -= 1
                current_col = min(current_col, len(text[current_line]))

        elif key == curses.KEY_DOWN:  # Move cursor down
            if current_line < len(text) - 1:
                current_line += 1
                current_col = min(current_col, len(text[current_line]))

        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            # Add new line
            text.insert(current_line + 1, text[current_line][current_col:])
            text[current_line] = text[current_line][:current_col]
            current_line += 1
            current_col = 0

        elif key == 27:  # Escape key to exit
            break

        elif key == curses.KEY_F2:  # Save file
            save_file()  #   Editing: {filename}
            stdscr.attron(curses.color_pair(6))
            filename_str = f"     File saved.    "
            filename_x = (width - len(filename_str)) // 2
            stdscr.addstr(0, filename_x, filename_str) 
            stdscr.refresh()
            stdscr.attroff(curses.color_pair(6))
            curses.napms(300)
            filename_str = f"Editing: {filename}"  
            filename_x = (width - len(filename_str)) // 2
            stdscr.addstr(0, filename_x, filename_str)  
            stdscr.refresh()         

        elif key == curses.KEY_F3:  # Load file
            load_file()
            stdscr.attron(curses.color_pair(6))
            filename_str = f"    File loaded.    "
            filename_x = (width - len(filename_str)) // 2
            stdscr.addstr(0, filename_x, filename_str) 
            stdscr.refresh()
            stdscr.attroff(curses.color_pair(6))
            curses.napms(300)
            filename_str = f"Editing: {filename}"  
            filename_x = (width - len(filename_str)) // 2
            stdscr.addstr(0, filename_x, filename_str)  
            stdscr.refresh()         

        elif 32 <= key <= 126:  # ASCII printable characters
            # Insert character at the current position
            if current_line < len(text):
                # Insert correctly based on line type
                if text[current_line].startswith("*"):
                    if current_col == 0:
                        # Inserting into bullet point area, just ignore
                        continue
                    elif current_col <= 4:
                        # Inserting in the space after bullet point
                        text[current_line] = text[current_line][:current_col + 4] + chr(key) + text[current_line][current_col + 4:]
                        current_col += 1
                    else:
                        text[current_line] = text[current_line][:current_col] + chr(key) + text[current_line][current_col:]
                        current_col += 1
                else:
                    text[current_line] = text[current_line][:current_col] + chr(key) + text[current_line][current_col:]
                    current_col += 1

        # Adjust viewport
        if current_line < viewport_start:
            viewport_start = current_line
        elif current_line - viewport_start >= height - 3:  # Avoid the shortcut line
            viewport_start = current_line - height + 3  # Adjust by 3 to avoid last 2 lines



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python editor.py <filename>")
    else:
        curses.wrapper(editor, sys.argv[1])

