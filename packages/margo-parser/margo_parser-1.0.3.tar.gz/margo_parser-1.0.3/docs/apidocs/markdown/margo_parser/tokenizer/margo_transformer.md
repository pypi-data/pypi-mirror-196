Module margo_parser.tokenizer.margo_transformer
===============================================
Lark Transformer for Margo syntax

Classes
-------

`MargoTransformer(visit_tokens=True)`
:   Lark Transformer for Margo syntax

    ### Ancestors (in MRO)

    * lark.visitors.Transformer
    * lark.visitors._Decoratable

    ### Methods

    `ENDBLOCK(self, eb)`
    :

    `IGNORE_CELL(self, _)`
    :

    `KEY(self, k)`
    :

    `QSTRING(self, s)`
    :

    `argument_list(self, al)`
    :

    `block(self, b)`
    :   *Transform a Margo block*
        
        A Margo block is a sequence of statements separated by endblocks, i.e.:
        
        ```margo
        {statement-1} ::
        {statement-2} ::
        {statement-3} ::
        ```

    `builtin(self, s)`
    :

    `directive(self, d)`
    :   *Transform a Margo directive*
        
        A directive is a statement that makes no assignment, i.e.:
        
        ```margo
        ignore-cell ::
        ```
        
        In the above example, `ignore-cell` is the directive statement
        and `::` is the endblock.

    `evf_assignment(self, c)`
    :   *Transform an external value format assignment*
        
        External value formats include:
        * JSON
        * YAML
        * raw (plain text)
        
        Example:
        
        ```margo
        requirements [yaml]:'
            - nbformat
            - requests
        ' ::
        ```
        
        In the above example:
        * `requirements` is the name
        * `[yaml]` specifies the format
        * The quoted string following the colon is the value
        assigned to the name.

    `expression(self, e: lark.tree.Tree)`
    :

    `false(self, _)`
    :

    `function(self, f)`
    :

    `function_name(self, fn)`
    :

    `mvf_assignment(self, kvp)`
    :

    `null(self, _)`
    :

    `number(self, n)`
    :

    `statement(self, s: lark.tree.Tree)`
    :

    `string(self, s)`
    :

    `true(self, _)`
    :

    `value(self, v)`
    :