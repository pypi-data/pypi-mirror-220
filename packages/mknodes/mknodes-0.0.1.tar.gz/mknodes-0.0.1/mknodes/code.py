from __future__ import annotations

import inspect
import logging
import textwrap
import types

from typing_extensions import Self

from mknodes import markdownnode, utils


logger = logging.getLogger(__name__)


class Code(markdownnode.Text):
    """Class representing a Code block."""

    REQUIRED_EXTENSIONS = [
        "pymdownx.highlight",
        "pymdownx.inlinehilite",
        "pymdownx.snippets",
        "pymdownx.superfences",
    ]

    def __init__(
        self,
        language: str,
        code: str | markdownnode.MkNode = "",
        *,
        title: str = "",
        header: str = "",
        linenums: int | None = None,
        highlight_lines: list[int] | None = None,
        parent=None,
    ):
        if isinstance(code, Code):
            code = textwrap.indent(str(code), "    ")
        super().__init__(code, header=header, parent=parent)
        self.language = language
        self.title = title
        self.linenums = linenums
        self.highlight_lines = highlight_lines

    def _to_markdown(self) -> str:
        title = f" title={self.title!r}" if self.title else ""
        return f"``` {self.language}{title}\n{self.text}\n```"

    @staticmethod
    def examples():
        yield dict(language="python", code="a = 1 + 2")
        yield dict(language="js", code="var z = x + y;", title="JavaScript")

    @classmethod
    def for_object(
        cls,
        obj: types.ModuleType
        | type
        | types.MethodType
        | types.FunctionType
        | types.TracebackType
        | types.FrameType
        | types.CodeType,
        *,
        dedent: bool = True,
        extract_body: bool = False,
        header: str = "",
    ) -> Self:
        if extract_body and isinstance(obj, type | types.FunctionType | types.MethodType):
            code = utils.get_function_body(obj)
        elif extract_body:
            raise TypeError("Can only extract body from Functions, Methods and classes")
        else:
            code = inspect.getsource(obj)
        code = textwrap.dedent(code) if dedent else code
        return cls(language="py", code=code, header=header)


if __name__ == "__main__":
    code = Code.for_object(Code, extract_body=True)
    print(code)
