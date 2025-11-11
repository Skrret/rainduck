# RainDuck

A simple BrainFuck extension with macros transpiled to BrainFuck.

## Installation

Use `pip` to install RainDuck.
```bash
pip install rainduck
```

## Usage

```bash
# transpiles code to BrainFuck
rainduck my-program.rd

# use your favourite BrainFuck compiler or interpreter
brainfuck my-program.bf

# or use pipe
rainduck my-program.rd --stdout | brainfuck
```

Run `rainduck --help` for more options.

### Basic Syntax

```rainduck
// comments are created with '//'
let // if you want to define macros, you must start with the word 'let'
#import(../folder/file.rd) // imports all global macros in ../folder/file.rd
clear = {[-]} // macro without arguments
five_left = {5<} // integer repeats given string
ten_right = {-2five_left} // negative integer reverses string and turns > <-> < and + <-> -
error = {-3[+]} // loop cannot be inverted, this raises an error...
no_error = {-1 error} // ...but double iversion doesn't have effect, this raises no error
// using ?<element>:<element> syntax, you can specify normal and inverted version of some code:
move_left_to_zero = {?{<[<]}:{>[>]}}
move_right_to_zero = {-1move_left_to_zero} // >[>]
move_cell(
    from;
    to = < // default value for this argument
) = {from [- -1from to + -1to from] -1from}

// most whitespace characters are optional
copy_cell(from={};to={};storage=<)={from[--1from storage+-1storage to+-1to from]move(storage)-1from}
in // end of macro definitions
// follows executed code
move( // macro call
    { // code blocks are created with curly brackets...
        let five_left={5{<<>}} in // ...and can contain local macro definition...
        3 {five_left >} // ...but don't have to
    };
    >
)

// `@<character>` is treated as a number equal to ASCII/UNICODE code of the character.
@B+ . @B- @F+ . @F- @! .
#comment(This comment will be also in final brainfuck code.)
```

## Contributing

Pull requests are welcome. I also welcome remarks about anything I've done incorrectly or improperly.

## License

[MIT](https://choosealicense.com/licenses/mit/)
