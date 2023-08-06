from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class TokensValidator(Validator):
    """
    Required, defaults to token sets for `.tex` and `.ly`.
    """

    def __init__(self):
        self._key = "tokens"
        self._semantic = Semantic.REQUIRED

    def validate(self, value: dict[str, dict[str, str]]) -> bool:
        invalid_keys = []

        for k, v in value.items():
            if not k.startswith("."):
                invalid_keys.append(k)

            if (
                "placeholder_prefix" in v
                and "placeholder_suffix" in v
                and "single_line_comment_prefix" in v
                and "block_comment_prefix" in v
                and "block_comment_suffix" in v
            ):
                pass
            else:
                invalid_keys.append(k)

        for key in invalid_keys:
            value.pop(key)

        if ".tex" in value:
            return True
        else:
            return False

    def default(self) -> dict[str, dict[str, str]]:
        return {
            ".tex": {
                "placeholder_prefix": "<<",
                "placeholder_suffix": ">>",
                "single_line_comment_prefix": "%",
                "block_comment_prefix": "\\\\iffalse",  # \iffalse
                "block_comment_suffix": "\\\\fi",  # \fi
            },
            ".ly": {
                "placeholder_prefix": "<<",
                "placeholder_suffix": ">>",
                "single_line_comment_prefix": "%",
                "block_comment_prefix": "%{",
                "block_comment_suffix": "%}",
            },
        }
