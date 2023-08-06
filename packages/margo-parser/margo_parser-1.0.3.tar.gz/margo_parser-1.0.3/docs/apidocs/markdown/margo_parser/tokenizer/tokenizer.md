Module margo_parser.tokenizer.tokenizer
=======================================

Functions
---------

    
`get_tree(source: str) ‑> lark.tree.Tree`
:   Parse source and return a Lark Tree

    
`grammar() ‑> lark.lark.Lark`
:   Get the Margo Lark grammar

    
`tokenize(source: str)`
:   Given a source file, return a Margo dict

    
`transform(tree: lark.tree.Tree)`
:   Transform a Lark Tree into a Margo dict