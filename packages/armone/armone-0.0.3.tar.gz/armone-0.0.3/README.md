# Armone

A powerful command-line tool to obfuscate python scripts effectively!

## Installation
```sh
pip install pipx
pipx ensurepath
pipx install armone
```
## Usage
Obfuscate `my_code.py` and generate a new file `obfuscated.py` in the cwd:
```sh
armone my_code.py
```
Specify the output file:
```sh
armone my_code.py -o obfuscated.py
```