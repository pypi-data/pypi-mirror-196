from margo_parser.tokenizer.tokenizer import tokenize


def test_empty_source():
    tokenized = tokenize("")
    assert type(tokenized) == dict
    assert tokenized["TYPE"] == "BLOCK"
    assert tokenized["SYNTAX"] == "MARGO"

    assert len(tokenized["BODY"]) == 0


def test_only_endblocks():
    tokenized = tokenize(":: :: :: ::")
    assert len(tokenized["BODY"]) == 0


def test_ignore_cell():
    tokenized = tokenize("ignore-cell ::")
    assert len(tokenized["BODY"]) == 1
    assert tokenized["BODY"][0]["TYPE"] == "DIRECTIVE"
    assert tokenized["BODY"][0]["NAME"] == "ignore-cell"


def test_basic_declaration():
    """
    If no language is specified, a declaration is treated
    as a JSON array without the enclosing brackets required
    """

    tokenized = tokenize(
        """
        hello_basic: "world!!!",
        1,
        true, 3, false, null, ::
    """
    )

    assert len(tokenized["BODY"]) == 1
    declaration = tokenized["BODY"][0]
    assert declaration["TYPE"] == "DECLARATION"
    assert declaration["NAME"] == "hello_basic"
    assert declaration["VALUE"] == ["world!!!", 1, True, 3, False, None]


def test_json_declaration():
    """
    Users can assert that a declaration is valid JSON,
    and it will be parsed (or fail)
    """

    tokenized = tokenize(
        """
    hello [json]: '["world!!",
    1,
    true,
    3,
    false,
    null]'
    ::
    """
    )
    declaration = tokenized["BODY"][0]
    assert declaration["VALUE"] == ["world!!", 1, True, 3, False, None]


def test_yaml_declaration():
    tokenized = tokenize(
        """
    hello [yaml]: '
    - "world!!"
    - 1
    - true
    - 3
    - false
    - null'
    ::
    """
    )
    declaration = tokenized["BODY"][0]
    assert declaration["VALUE"] == ["world!!", 1, True, 3, False, None]


def test_raw_declaration():
    inner_string = "hello world!! 1 true 3 false null"
    test_string = f"""
    hello [raw]: '{inner_string}' ::
    """
    tokenized = tokenize(test_string)

    declaration = tokenized["BODY"][0]
    assert declaration["VALUE"] == inner_string
