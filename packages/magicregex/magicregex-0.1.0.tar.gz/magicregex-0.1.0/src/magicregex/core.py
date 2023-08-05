# FIXME variable length lookups need to use regex package instead of re
import regex as re
import typing as t

ESCAPE_REPLACE_RE = r"[.*+?^${}()|[\]\\/]"

GROUPED_AS_REPLACE_RE = r"^(?:\(\?:(.+)\)|(\(?.+\)?))$"
GROUPED_REPLACE_RE = r"^(?:\(\?:(.+)\)([?+*]|{[\d,]+})?|(.+))$"


class CreateInput:
    def __init__(self, s: t.Union[str, "CreateInput"]) -> None:
        """Wraps a chain of CreateInput objects that will get compiled into an RegEx.
        The class provided methods for chaining.

        Args:
            s: str or CreateInput to be wrapped.
        """
        self.s = s

    def AndReferenceTo(self, groupName: str) -> "CreateInput":
        """Creates a reference to the predecessor group.

        Args:
            groupName: name used for the group

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{self.s}\\k<{groupName}>")

    def And(self, input: t.Union[str, "CreateInput"]) -> "CreateInput":
        """Extend the pattern with input.

        Args:
            input: pattern that has to follow

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{self.s}{exactly(input)}")

    def Or(self, input: t.Union[str, "CreateInput"]) -> "CreateInput":
        """Either this or the input pattern is valid.

        Args:
            input: pattern that is an alternative to the current pattern.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"(?:{self.s}|{exactly(input)})")

    def After(self, input: t.Union[str, "CreateInput"]) -> "CreateInput":
        """Perform positive lookbehind.

        Args:
            input: pattern that has to be before the matching pattern.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"(?<={exactly(input)}){self.s}")

    def Before(self, input: t.Union[str, "CreateInput"]) -> "CreateInput":
        """Perform positive lookahead.

        Args:
            input: pattern that has to be after the matching pattern.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{self.s}(?={exactly(input)})")

    def NotAfter(self, input: t.Union[str, "CreateInput"]) -> "CreateInput":
        """Perform negative lookbehind.

        Args:
            input: pattern that should not be before the matching pattern.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"(?<!{exactly(input)}){self.s}")

    def NotBefore(self, input: t.Union[str, "CreateInput"]) -> "CreateInput":
        """Perform negative lookahead.

        Args:
            input: pattern that should not be after the matching pattern.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{self.s}(?!{exactly(input)})")

    def GroupedAs(self, key: str) -> "CreateInput":
        """This defines the entire input so far as a named capture group.

        Args:
            key: name of the created group.

        Returns:
            resulting CreateInput object
        """
        input = re.sub(GROUPED_AS_REPLACE_RE, r"\g<1>\g<2>", self.s)
        return CreateInput(f"(?<{key}>{input})")

    def Grouped(self) -> "CreateInput":
        """This defines the entire input so far as an anonymous group.

        Returns:
            resulting CreateInput object
        """
        input = re.sub(GROUPED_REPLACE_RE, r"(\g<1>\g<3>)\g<2>", self.s)
        return CreateInput(input)

    def AtLineStart(self) -> "CreateInput":
        """This allows you to match beginning of lines.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"^{self.s}")

    def AtLineEnd(self) -> "CreateInput":
        """This allows you to match end of lines.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{self.s}$")

    def Optionally(self) -> "CreateInput":
        """This is a function you can call to mark the current input as optional.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{_wrap(self.s)}?")

    def Times(self, number: int) -> "CreateInput":
        """This is a function you can call directly to repeat the previous pattern an exact number of times.

        Args:
            number: number of expected repeats.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{_wrap(self.s)}{{{number}}}")

    def TimesAny(self) -> "CreateInput":
        """This is a function indicates the pattern can repeat any number of times, including none

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{_wrap(self.s)}*")

    def TimesAtLeast(self, min: int) -> "CreateInput":
        """This is a function indicates the pattern must repeat at least x times

        Args:
            min: minimum number of repeats.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{_wrap(self.s)}{{{min},}}")

    def TimesBetween(self, min: int, max: int) -> "CreateInput":
        """This is a function indicates the pattern must repeat between min and max times.

        Args:
            min: minimum number of repeats.
            max: maximum number of repeats.

        Returns:
            resulting CreateInput object
        """
        return CreateInput(f"{_wrap(self.s)}{{{min},{max}}}")

    def __str__(self) -> str:
        """Convert to string"""
        return self.s

    def __repr__(self) -> str:
        """Convert to string"""
        return self.__str__()


NO_WRAP_RE = r"^(\(.*\)|\\?.)$"


def _wrap(input: t.Union[str, CreateInput]) -> str:
    v = str(input)
    if re.match(NO_WRAP_RE, v):
        return v
    return f"(?:{v})"


def charIn(chars: str) -> CreateInput:
    """This matches any character in the string provided.

    Args:
        chars: strings of chars that match

    Returns:
        resulting CreateInput object
    """
    v = re.sub(r"/[-\\^\]]/g", lambda x: f"\\{x.group(0)}", chars)
    return CreateInput(f"[{v}]")


def charNotIn(chars: str) -> CreateInput:
    """This doesn't match any character in the string provided.

    Args:
        chars: strings of chars that do not match

    Returns:
        resulting CreateInput object
    """
    v = re.sub(r"/[-\\^\]]/g", lambda x: f"\\{x.group(0)}", chars)
    return CreateInput(f"[^{v}]")


def anyOf(input: t.Set[str]) -> CreateInput:
    """This takes a set of inputs and matches any of them.

    Args:
        input: set of string that match

    Returns:
        resulting CreateInput object
    """
    anys = [exactly(a) for a in input].join("|")
    return CreateInput(f"(?:{anys})")


def mayBe(input: t.Union[str, CreateInput]) -> CreateInput:
    """Equivalent to ? - this marks the input as optional.

    Args:
        input: pattern to wrap

    Returns:
        resulting CreateInput object
    """
    return CreateInput(f"{_wrap(exactly(input))}?")


def exactly(input: str) -> CreateInput:
    """This escapes a string input to match it exactly.

    Args:
        input: str to wrap

    Returns:
        resulting CreateInput object
    """
    if isinstance(input, str):
        return CreateInput(
            re.sub(ESCAPE_REPLACE_RE, lambda x: f"\\{x.group(0)}", input)
        )
    return input


def oneOrMore(input: t.Union[str, CreateInput]) -> CreateInput:
    """Equivalent to + - this marks the input as repeatable, any number of times but at least once.

    Args:
        input: pattern to wrap

    Returns:
        resulting CreateInput object
    """
    return CreateInput(f"{_wrap(exactly(input))}+")


# frequently used patterns
char = CreateInput(".")
word = CreateInput("\\b\\w+\\b")
wordChar = CreateInput("\\w")
wordBoundary = CreateInput("\\b")
digit = CreateInput("\\d")
whitespace = CreateInput("\\s")
letter = CreateInput("[a-zA-Z]")
lowercase = CreateInput("[a-z]")
uppercase = CreateInput("[A-Z]")
tab = CreateInput("\\t")
linefeed = CreateInput("\\n")
carriageReturn = CreateInput("\\r")

# negated variants
notWordChar = CreateInput("\\W")
notWordBoundary = CreateInput("\\B")
notDigit = CreateInput("\\D")
notWhitespace = CreateInput("\\S")
notLetter = CreateInput("[^a-zA-Z]")
notLowercase = CreateInput("[^a-z]")
notUppercase = CreateInput("[^A-Z]")
notTab = CreateInput("[^\\t]")
notLinefeed = CreateInput("[^\\n]")
notCarriageReturn = CreateInput("[^\\r]")


def createRegEx(
    input: t.Union[str, CreateInput], flags: re.RegexFlag = 0
) -> re.Pattern:
    """Compiles CreateInput object into pattern object.

    Args:
        input: input that gets compiled into RegEx
        flags: flags that get forwarded to re.compile
    """
    return re.compile(exactly(input).__str__(), flags)
