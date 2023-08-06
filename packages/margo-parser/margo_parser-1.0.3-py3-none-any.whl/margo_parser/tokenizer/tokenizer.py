from lark import Lark, Tree
from .margo_transformer import MargoTransformer
from ..exceptions import MargoParseException
import os


def grammar() -> Lark:
    """Get the Margo Lark grammar"""
    grammar_file_path = os.path.join(os.path.split(__file__)[0], "margo.lark")
    grammar_content = open(grammar_file_path).read()
    return Lark(grammar_content, start="block", regex=True)


def get_tree(source: str) -> Tree:
    """Parse source and return a Lark Tree"""
    return grammar().parse(source)


def transform(tree: Tree):
    """Transform a Lark Tree into a Margo dict"""
    return MargoTransformer().transform(tree)


def tokenize(source: str):
    """Given a source file, return a Margo dict"""
    try:
        return transform(get_tree(source))
    except Exception as e:
        raise MargoParseException(e)
