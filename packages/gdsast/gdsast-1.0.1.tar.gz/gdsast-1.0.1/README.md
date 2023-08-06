# gdsast python package (implements GDS <-> AST translation)


## GDS <-> AST translation

This package provides GDS serialization functions.

It implements schema for parsing GDS binary data into JSON like structure.

Parser implemented as strict state machine according to latest GDS file format specs.

gds_read function returns AST that could be directly saved to JSON with json.dump

gds_write saves AST into binary GDS data file

With AST it becomes easy to browse, analyze, modify, add, remove GDS file structures and elements.
