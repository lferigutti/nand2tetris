from pathlib import Path


class XmlWriter:
    def __init__(self, indent: str = "  "):
        self._indent = indent
        self._lines: list[str] = []
        self._open_tags: list[str] = []

    def open_tag(self, name: str) -> None:
        self._validate_tag_name(name)
        self._lines.append(f"{self._current_indentation}<{name}>")
        self._open_tags.append(name)

    def close_tag(self, name: str) -> None:
        self._validate_tag_name(name)

        if not self._open_tags:
            raise ValueError(f"Cannot close tag '{name}': no tags are currently open")

        current_tag = self._open_tags.pop()
        if current_tag != name:
            raise ValueError(
                f"Cannot close tag '{name}': expected closing tag for '{current_tag}'"
            )

        self._lines.append(f"{self._current_indentation}</{name}>")

    def leaf(self, name: str, value: str) -> None:
        self._validate_tag_name(name)
        escaped_value = self._escape(value)
        self._lines.append(f"{self._current_indentation}<{name}> {escaped_value} </{name}>")

    def render(self) -> str:
        if self._open_tags:
            raise ValueError(
                "Cannot render XML with unclosed tags: "
                + ", ".join(self._open_tags)
            )

        if not self._lines:
            return ""

        return "\n".join(self._lines) + "\n"

    def write_to(self, output_path: Path) -> None:
        output_path.write_text(self.render())

    @property
    def _current_indentation(self) -> str:
        return self._indent * len(self._open_tags)

    @staticmethod
    def _escape(value: str) -> str:
        return (
            value.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    @staticmethod
    def _validate_tag_name(name: str) -> None:
        if not name:
            raise ValueError("Tag name cannot be empty")