# cliedit
Uploading this to GitHub because i lost this code several times...

# Features
- **Text Navigation**: Use arrow keys to move the cursor up, down, left, and right.
- **File Operations**:
  - Save the file with `F2`.
  - Load the file with `F3`.
- **Special Formatting**:
  - Lines starting with `>>>` are displayed in bold.
  - Lines starting with `*` or `-` are automatically formatted as bullet points.
- **Cursor Position Display**: Shows the current line and column at the bottom-right corner.
- **Filename Display**: Displays the name of the file being edited at the top of the editor.

# Usage
## Prerequisites
- Python 3.x
- Terminal that supports curses

## Running the Editor
1. Save the script as editor.py (or any filename you want).
2. Run the script from the terminal, providing the name of the file you want to edit:
```bash
python editor.py <filename>
```
If the file doesn't exist, it will be created when you save.

## Controls

| Key | Action |
|-------------|-------------|
| Arrow Keys |	Move the cursor up, down, left, or right. |
| Enter |	Insert a new line at the cursor position. |
| Backspace	| Delete the character before the cursor. |
| Delete | Delete the character under the cursor. |
| F2 | Save the file. |
| F3 | Reload the file. |
| ESC |	Exit the editor. |

## Special Formatting Rules
- Lines starting with `>>>` are rendered in bold.
- Lines starting with `*` or `-` are treated as list items and rendered with a bullet (•) and proper spacing.

## Example
### Input
```text
>>> This is a bold line.
* This is a bullet point.
- Another bullet point.
Regular text here.
```
### Display
- note for me, put a picture here
  
# Limitations
- Only ASCII characters are supported for input.
- No support for mouse interactions.
- Does not handle very large files efficiently due to lack of optimized scrolling.

# License
This project is open-source and distributed under the MIT License.
