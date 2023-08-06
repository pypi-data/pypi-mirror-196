Module margo_parser.api
=======================
The main API for Margo Parser

Sub-modules
-----------
* margo_parser.api.classes
* margo_parser.api.utils

Classes
-------

`MargoAssignment(name: str, value)`
:   A Margo statement
    
    :param statement_type: MargoStatementTypes.DECLARATION or
        MargoStatementTypes.DIRECTIVE
    :param name: the name of the statement
    :param value: the value of the statement
    @raises MargoLangException if parameters are invalid

    ### Ancestors (in MRO)

    * margo_parser.api.classes.MargoStatement.MargoStatement
    * abc.ABC

`MargoBlock(source: str)`
:   A collection of Margo statements.
    
    Parses source immediately, raising an exception if parsing
    fails.
    :param source: The source code string
    :raises: MargoParseException if the source string cannot be parsed
    :raises: MargoLangException if there's some other error

    ### Descendants

    * margo_parser.api.classes.MargoMarkdownCellPrambleBlock.MargoMarkdownCellPreambleBlock
    * margo_parser.api.classes.MargoPythonCellPreambleBlock.MargoPythonCellPreambleBlock

    ### Instance variables

    `statements: List[margo_parser.api.classes.MargoStatement.MargoStatement]`
    :   List of Margo statements

`MargoDirective(name: str)`
:   A Margo statement
    
    :param statement_type: MargoStatementTypes.DECLARATION or
        MargoStatementTypes.DIRECTIVE
    :param name: the name of the statement
    :param value: the value of the statement
    @raises MargoLangException if parameters are invalid

    ### Ancestors (in MRO)

    * margo_parser.api.classes.MargoStatement.MargoStatement
    * abc.ABC

`MargoMarkdownCellPreambleBlock(source: str)`
:   A helper to process just the Margo preamble (if any) of a Markdown
    cell. Instead of using MargoBlock directly, which requires the source
    string to only be valid Margo, this will extract the preamble from the
    cell contents.
    
    :param source: The entire source of a Markdown cell

    ### Ancestors (in MRO)

    * margo_parser.api.classes.MargoBlock.MargoBlock

`MargoParseException(*args, **kwargs)`
:   Parsing source code failed

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`MargoPythonCellPreambleBlock(source: str)`
:   A helper to process just the Margo preamble (if any) of a Python cell.
    Instead of using MargoBlock directly, which requires the source string to
    only be valid Margo, this will extract the preamble from the cell contents.
    
    :param source: The entire source of a Python cell

    ### Ancestors (in MRO)

    * margo_parser.api.classes.MargoBlock.MargoBlock

`MargoStatement(statement_type: str, name: str, value=None)`
:   A Margo statement
    
    :param statement_type: MargoStatementTypes.DECLARATION or
        MargoStatementTypes.DIRECTIVE
    :param name: the name of the statement
    :param value: the value of the statement
    @raises MargoLangException if parameters are invalid

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * margo_parser.api.classes.MargoAssignment.MargoAssignment
    * margo_parser.api.classes.MargoDirective.MargoDirective

    ### Instance variables

    `name: str`
    :   The name of the statement

    `type: str`
    :   'DIRECTIVE' or 'DECLARATION'

    `value: <built-in function any>`
    :   Any value. Should be None for directives

`MargoStatementTypes()`
:   Supported types of Margo statements

    ### Class variables

    `DECLARATION`
    :

    `DIRECTIVE`
    :

    `VALID_TYPES`
    :

    ### Static methods

    `is_valid_type(statement_type: str) ‑> bool`
    :   Determine if a string is a valid margo statement type