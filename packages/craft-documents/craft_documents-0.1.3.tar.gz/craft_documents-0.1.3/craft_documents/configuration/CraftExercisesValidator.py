from pathlib import Path

from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class ExerciseConfiguration(dict):
    """
    Wrapper around a dictionary that defines a minimal interface of
    an exercise configured in the configuration.
    """

    # TODO: Untyped reference to configuration...
    def __init__(self, configuration, name: str, *args, **kwargs):
        """
        Set `count` or `path` as kwargs to overwrite the defaults.

        - `count: int`
        - `path: str | Path`
        """
        name = name.removesuffix(".tex")

        # set any additional values
        self.update(*args, **kwargs)

        # Ensure count
        if "count" not in self:
            self["count"] = 1

        # Count is int
        try:
            self["count"] = int(self["count"])
        except:
            raise Exception("Couldn't convert count to an integer.")

        # Ensure path
        if "path" not in self:
            self["path"] = configuration.main.parent / ("exercises/%s.tex" % name)
        # Convert relative path to absolute path
        else:
            match self["path"]:
                case str(path):
                    path = Path(path.removesuffix(".tex") + ".tex")
                    if path.is_absolute():
                        self["path"] = path
                    else:
                        self["path"] = configuration.main.parent / "exercises" / path
                case Path():
                    # TODO: Conditionally append `.tex`
                    path = self["path"]
                    if path.is_absolute():
                        self["path"] = path
                    else:
                        self["path"] = configuration.main.parent / "exercises" / path

        # Absolute path
        self["path"] = self["path"].resolve()


class CraftExercisesValidator(Validator):
    """
    Optional, that defaults to a dictionary:

    ```
    {
        "intervals": {
            "count": 1,
            "path": Path(...),
        }
    }
    ```
    """

    def __init__(self):
        self._key = "craft-exercises"
        self._semantic = Semantic.OPTIONAL

    def remove_tex(self, value: str) -> str:
        return value.removesuffix(".tex")

    def exercise_path_appending(self, component: str | Path) -> Path:
        match component:
            case str():
                return (
                    self.configuration.main.parent
                    / ("exercises/" + self.remove_tex(component) + ".tex")
                ).resolve()
            case Path():
                return (
                    self.configuration.main.parent / "exercises/" / component
                ).resolve()

    def lint(self, value) -> dict:
        result = {}

        def dict_types(dictionary: dict, key, value) -> bool:
            return all(
                isinstance(k, key) and isinstance(v, value)
                for k, v in dictionary.items()
            )

        match value:
            # craft-exercises: intervals
            case str(exercise_name):
                result[exercise_name] = ExerciseConfiguration(
                    self.configuration, exercise_name
                )

            # craft-exercises:
            case list(items):
                for item in items:
                    match item:
                        # - intervals
                        case str(exercise_name):
                            result[exercise_name] = ExerciseConfiguration(
                                self.configuration, exercise_name
                            )
                        # - intervals: 2
                        case dict(item) if dict_types(item, str, int):
                            for exercise_name, count in item.items():
                                result[exercise_name] = ExerciseConfiguration(
                                    self.configuration, exercise_name, count=count
                                )

                        # - intervals:
                        case dict(item) if dict_types(item, str, dict):
                            for exercise_name, kwargs in item.items():
                                result[exercise_name] = ExerciseConfiguration(
                                    self.configuration, exercise_name, **kwargs
                                )

            # craft-exercises:
            case dict(items):
                for exercise_name, v in items.items():
                    match v:
                        # 2
                        case int(count):
                            result[exercise_name] = ExerciseConfiguration(
                                self.configuration, exercise_name, count=count
                            )

                        # count: 3
                        case dict(config):
                            result[exercise_name] = ExerciseConfiguration(
                                self.configuration, exercise_name, **config
                            )

        return {self.remove_tex(key): value for key, value in result.items()}

    def validate(self, value) -> bool:
        """
        `value` will be of the type, that the linter produces.

        Needs to validate the path to the exercise.
        The count must be greater than 0.
        """
        invalid_keys = []

        for exercise_name, config in value.items():
            # path points to existing file
            if not config["path"].is_file():
                invalid_keys.append(exercise_name)

            # count is greater than 0
            if not config["count"] > 0:
                invalid_keys.append(exercise_name)

        for exercise_name in invalid_keys:
            value.pop(exercise_name)

        if self.configuration[self.key] == {}:
            self.configuration.pop(self.key)

        return True
