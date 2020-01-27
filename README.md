# terminal-define
Look up any definition from Wikipedia right inside your terminal. 

## Installation
Clone the repository

`git clone https://github.com/joschahenningsen/wikipedia-define-cli ~/wikipedia-define-cli`

Add define as an alias to your bashrc, zshrc, ... Modify this accordingly.

`echo 'alias define="python3 ~/wikipedia-define-cli/define.py"'>>~/.bashrc`

Update your bashrc, zshrc, ... Modify this accordingly.

`source ~/.bashrc`

## Usage
`define stack overflow -de` defines the term stack overflow in german

`define github` defines the term github in english

`define -setlang de` sets the standard language to german
