import typing as tp
import re

InputLike = tp.Union[tp.Any, tp.Tuple[tp.Any, ...], tp.Dict[str, tp.Any], "Inputs"]

def _unique_name(
    names: tp.Set[str],
    name: str,
):

    if name in names:

        match = re.match(r"(.*?)(\d*)$", name)
        assert match is not None

        name = match[1]
        num_part = match[2]

        i = int(num_part) if num_part else 2
        str_template = f"{{name}}{{i:0{len(num_part)}}}"

        while str_template.format(name=name, i=i) in names:
            i += 1

        name = str_template.format(name=name, i=i)

    names.add(name)
    return name


def _unique_names(
    names: tp.Iterable[str],
    *,
    existing_names: tp.Optional[tp.Set[str]] = None,
) -> tp.Iterable[str]:
    if existing_names is None:
        existing_names = set()

    for name in names:
        yield _unique_name(existing_names, name)


def _lower_snake_case(s: str) -> str:
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
    parts = s.split("_")
    output_parts = []

    for i in range(len(parts)):
        if i == 0 or len(parts[i - 1]) > 1:
            output_parts.append(parts[i])
        else:
            output_parts[-1] += parts[i]

    return "_".join(output_parts)


def _get_name(obj) -> str:
    if hasattr(obj, "name") and obj.name:
        return obj.name
    elif hasattr(obj, "__name__") and obj.__name__:
        return _lower_snake_case(obj.__name__)
    elif hasattr(obj, "__class__") and obj.__class__.__name__:
        return _lower_snake_case(obj.__class__.__name__)
    else:
        raise ValueError(f"Could not get name for: {obj}")

class Inputs:
    args: tp.Tuple[tp.Any, ...]
    kwargs: tp.Dict[str, tp.Any]

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def from_value(cls, value: InputLike) -> "Inputs":
        if isinstance(value, cls):
            return value
        elif isinstance(value, tuple):
            return cls(*value)
        elif isinstance(value, dict):
            return cls(**value)
        else:
            return cls(value)
