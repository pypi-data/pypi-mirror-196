import magicregex as mre

# NOTE: for testing regex https://regexr.com/


def test_simple() -> None:
    """Smoke test"""
    assert (
        mre.createRegEx(mre.exactly(mre.digit).Before("abc")).match("1abc") is not None
    )
    assert 4 == 4


def test_repeat() -> None:
    """Test repeat feature"""
    reg = mre.exactly(mre.digit).Times(5)
    assert mre.createRegEx(reg).fullmatch("12345") is not None


def test_date() -> None:
    """Test multiple features by matching a date"""
    reg = (
        mre.exactly(mre.digit)
        .TimesBetween(1, 2)
        .And(".")
        .And(mre.exactly(mre.digit).TimesBetween(1, 2))
        .And(".")
        .And(mre.exactly(mre.digit).Times(4))
    )
    assert mre.createRegEx(reg).fullmatch("11.11.1992") is not None


def test_path() -> None:
    """Test multiple features by matching a path"""
    reg = (
        mre.exactly("bar/")
        .TimesAny()
        .And("foo/test.")
        .And(mre.exactly("js").Or(mre.exactly("py")))
    )
    assert mre.createRegEx(reg).match("bar/bar/bar/bar/foo/test.js") is not None
    assert mre.createRegEx(reg).match("bar/foo/test.py") is not None


def test_and() -> None:
    """Test and feature"""
    reg = mre.exactly(mre.digit).Times(2).And("abc")
    assert mre.createRegEx(reg).fullmatch("11abc") is not None
    assert mre.createRegEx(reg).fullmatch("1abc") is None
    assert mre.createRegEx(reg).fullmatch("11bcd") is None


def test_or() -> None:
    """Test or feature"""
    reg = mre.exactly(mre.digit).Or(mre.exactly(mre.char).Times(4))
    assert mre.createRegEx(reg).fullmatch("1") is not None
    assert mre.createRegEx(reg).fullmatch("aaaa") is not None
    assert mre.createRegEx(reg).fullmatch("aaa") is None


def test_after() -> None:
    """Test after feature"""
    reg = mre.createRegEx(mre.exactly(mre.letter).Times(3).After(" "))
    assert len(reg.findall("abc d abc d abc a")) == 2
