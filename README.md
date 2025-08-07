# LCD Text Display FSM Generator

This project generates VHDL code for a Finite State Machine (FSM) that displays custom text on an LCD module (such as a 16x2 alphanumeric LCD). The FSM automatically handles LCD initialization and writes each character using correct control signals.

## Features

- Converts input text into a sequence of VHDL FSM states to control an LCD.
- Supports common ASCII characters and special symbols (`!`, `?`, `.`, `,`, `:`, `;`, space, etc.).
- Supports line breaks using `\n`.
- Automatically generates LCD initialization sequence.
- FSM states manage `RS`, `RW`, `EN`, and `DATA` signals.
- Outputs fully synthesizable VHDL code.

## How to Use

1. Run the Python script.
2. Enter the text you want to display (use `\\n` for new lines).
3. The script will generate a file:
   - `lcd_autogenerado.vhd`: VHDL file with the complete FSM.

### Example Input
Hello, world!\nLCD ready.


### Example Output

The generated VHDL code:
- Initializes the LCD (Function Set, Display ON, Clear Display, Entry Mode Set).
- Sends each character to the display using a 3-state sequence per character.
- Ends with a final state that resets the FSM.


## Requirements

- Python 3.x

## Output Files

- `lcd_autogenerado.vhd`: Synthesizable FSM-based VHDL code for displaying the text.

## Author

Julian Marquez Gutierrez  
Email: julianmarquezgtz@gmail.com  
GitHub: [julianmarquezgtz-eng](https://github.com/julianmarquezgtz-eng)
