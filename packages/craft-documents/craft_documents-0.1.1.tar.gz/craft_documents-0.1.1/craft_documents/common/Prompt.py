import collections.abc
from abc import ABC
from enum import Enum

# from typing import List as ListType
from typing import Any, Callable, Dict

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Separator, Validator

Answers = Dict[str, Any]


class Prompt(dict, ABC):
    """
    Dictonary representing a PyInquirer prompt.

    Use the specific subclasses that represent
    the different types of prompt.
    """

    class Type(Enum):
        list = "list"
        rawlist = "rawlist"
        expand = "expand"
        checkbox = "checkbox"
        confirm = "confirm"
        input = "input"
        password = "password"
        editor = "editor"

    def __init__(
        self,
        type: "Prompt.Type",
        name: str,
        message: str | None = None,
        when: Callable[[Answers], bool] | bool = True,
    ):
        self["type"] = type.name
        self["name"] = name
        self["message"] = (
            message if message is not None else "Please provide the '%s'." % name
        )
        if isinstance(when, bool) and not when:
            self["when"] = when
        elif not isinstance(when, bool):
            self["when"] = when


class List(Prompt):
    """
    A list prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/list.py

    Take `type`, `name`, `message`, `choices`[, `default`, `filter`] properties.
    (Note that default must be the choice index in the array or a choice value.)
    """

    def __init__(
        self,
        name: str,
        choices: list[str | Separator],
        message: str | None = None,
        when: Callable[[Answers], bool] | bool = True,
        default: int | str | Callable[[Answers], str | int] | None = None,
        filter: Callable[[str], str] | None = None,
    ):
        super().__init__(Prompt.Type.list, name, message, when)

        self["choices"] = choices

        if filter is not None:
            self["filter"] = filter

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value < len(choices):
                        self["default"] = value
                case str(value):
                    if value in choices:
                        self["default"] = value
                case _:
                    self["default"] = default


class RawList(Prompt):
    """
    A rawlist prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/rawlist.py

    Take `type`, `name`, `message`, `choices`[, `default`, `filter`] properties.
    (Note that default must the choice index in the array.)
    """

    def __init__(
        self,
        name: str,
        choices: list[str | Separator],
        message: str | None = None,
        when: Callable[[Answers], bool] | bool = True,
        default: int | Callable[[Answers], int] | None = None,
        filter: Callable[[str], str] | None = None,
    ):
        super().__init__(Prompt.Type.rawlist, name, message, when)

        self["choices"] = choices

        if filter is not None:
            self["filter"] = filter

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value < len(choices):
                        self["default"] = value
                case _:
                    self["default"] = default


class Expand(Prompt):
    """
    An expand prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/expand.py

    Take `type`, `name`, `message`, `choices`[, `default`] properties.
    (Note that default must be the choice index in the array or a key.
    If default key not provided, then help will be used as default choice.)

    Note that the choices object will take an extra parameter
    called key for the expand prompt. This parameter must be a
    single (lowercased) character. The `h` option is added by the
    prompt and shouldn't be defined by the user.
    """

    class Choice(dict):
        def __init__(self, name: str, key: str, value: str | None = None):
            self["name"] = name
            self["key"] = key
            if value is not None:
                self["value"] = value

    def __init__(
        self,
        name: str,
        choices: list[Choice | Separator],
        message: str | None = None,
        default: str | int | Callable[[Answers], str | int] | None = None,
        when: Callable[[Answers], bool] | bool = True,
    ):
        super().__init__(Prompt.Type.expand, name, message, when)

        self["choices"] = choices

        # Validate default value
        if default is not None:
            match default:
                case int(value):
                    if value < len(choices):
                        self["default"] = value
                case str(value):
                    keys = [
                        choice.get("key", "")
                        for choice in choices
                        if isinstance(choice, Expand.Choice)
                    ]
                    if value in keys:
                        self["default"] = value
                case _:
                    self["default"] = default


class Checkbox(Prompt):
    """
    A checkbox prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/checkbox.py

    Take `type`, `name`, `message`, `choices`[, `qmark`, `filter`, `validate`] properties.

    Choices marked as {'checked': True} will be checked by default.

    Choices whose property `disabled` is True will be unselectable.
    If `disabled` is a string, then the string will be outputted next
    to the disabled choice, otherwise it'll default to "Disabled".
    The disabled property can also be a synchronous function
    receiving the current answers as argument and returning a boolean
    or a string.

    The `pointer_index` kwarg can be used to specify initial pointer position.
    """

    class Choice(dict):
        def __init__(
            self,
            name: str,
            value: str | None = None,
            checked: bool | None = None,
            disabled: bool | str | Callable[[Answers], bool | str] | None = None,
        ):
            self["name"] = name
            if value is not None:
                self["value"] = value
            if checked is not None:
                self["checked"] = checked
            if disabled is not None:
                self["disable"] = disabled

    def __init__(
        self,
        name: str,
        choices: list[Choice | Separator],
        message: str | None = None,
        qmark: str | None = None,
        when: Callable[[Answers], bool] | bool = True,
        filter: Callable[[str], str] | None = None,
        validate: Callable[[str], bool | str] | Validator | None = None,
    ):
        super().__init__(Prompt.Type.checkbox, name, message, when)
        self["choices"] = choices
        if qmark is not None:
            self["qmark"] = qmark
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate


class Confirm(Prompt):
    """
    A confirmation prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/confirm.py

    Take `type`, `name`, `message`[, `default`] properties.
    `default` is expected to be a boolean if used.
    """

    def __init__(
        self,
        name: str,
        message: str | None = None,
        default: bool | Callable[[Answers], bool] | None = None,
        when: Callable[[Answers], bool] | bool = True,
    ):
        super().__init__(Prompt.Type.confirm, name, message, when)

        if default is not None:
            self["default"] = default


class Input(Prompt):
    """
    An input prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/input.py

    Take `type`, `name`, `message`[, `default`, `filter`, `validate`] properties.
    """

    def __init__(
        self,
        name: str,
        message: str | None = None,
        default: str | Callable[[Answers], str] | None = None,
        filter: Callable[[str], str] | None = None,
        when: Callable[[Answers], bool] | bool = True,
        validate: Callable[[str], bool | str] | Validator | None = None,
    ):
        super().__init__(Prompt.Type.input, name, message, when)

        if default is not None:
            self["default"] = default
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate


class Password(Prompt):
    """
    A password prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/password.py

    Take `type`, `name`, `message`[, `default`, `filter`, `validate`] properties.
    """

    def __init__(
        self,
        name: str,
        message: str | None = None,
        default: str | Callable[[Answers], str] | None = None,
        filter: Callable[[str], str] | None = None,
        when: Callable[[Answers], bool] | bool = True,
        validate: Callable[[str], bool | str] | Validator | None = None,
    ):
        super().__init__(Prompt.Type.password, name, message, when)

        if default is not None:
            self["default"] = default
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate


class Editor(Prompt):
    """
    An editor prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/editor.py

    Take `type`, `name`, `message`[, `default`, `filter`, `validate`, `eargs`]
    properties.

    ### Editor Arguments - `eargs`
    Opens an empty or edits the default text in the defined editor.
    If an editor is given (should be the full path to the executable
    but the regular operating system search path is used for finding
    the executable) it overrides the detected editor.
    Optionally, some environment variables can be used. If the editor
    is closed without changes, None is returned. In case a file is
    edited directly the return value is always None and `save` and `ext`
    are ignored.

    Takes:

    - `editor`: accepts default to get the default platform editor.
        But you can also provide the path to an editor e.g vi.
    - `ext`: the extension to tell the editor about. This defaults
        to .txt but changing this might change syntax highlighting e.g ".py"
    - `save`: accepts True or False to determine to save a file.
    - `filename`: accepts the path of a file you'd like to edit.
    - `env`: accepts any given environment variables to pass to the editor

    Launches an instance of the users preferred editor on a temporary file.
    Once the user exits their editor, the contents of the temporary file
    are read in as the result. The editor to use is determined by reading
    the `VISUAL` or `EDITOR` environment variables. If neither of
    those are present, `notepad` (on Windows) or `vim` (Linux or Mac) is used.
    """

    class Eargs(dict):
        def __init__(
            self,
            editor: str | None = None,
            ext: str | None = None,
            save: bool | None = None,
            filename: str | None = None,
            env: list[str] | None = None,
        ):
            if editor is not None:
                self["editor"] = editor
            if ext is not None:
                self["ext"] = ext
            if save is not None:
                self["save"] = save
            if filename is not None:
                self["filename"] = filename
            if env is not None:
                self["env"] = env

    def __init__(
        self,
        name: str,
        message: str | None = None,
        default: str | Callable[[Answers], str] | None = None,
        filter: Callable[[str], str] | None = None,
        when: Callable[[Answers], bool] | bool = True,
        validate: Callable[[str], bool | str] | Validator | None = None,
        eargs: Eargs | None = None,
    ):
        super().__init__(Prompt.Type.editor, name, message, when)

        if default is not None:
            self["default"] = default
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate
        if eargs is not None:
            self["eargs"] = eargs
