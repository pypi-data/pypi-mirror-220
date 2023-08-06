from typing import TYPE_CHECKING

__all__ = ["schema_from_inis"]


if TYPE_CHECKING:
    from _typeshed import IdentityFunction
from typing import Any, Callable, Iterable
from click_schema_config.types import FileLike

import builtins

import click
from .read_config import read_configs

FC = Callable[..., Any]


def schema_from_inis(
    filenames: Iterable[FileLike] | FileLike = ["config.default.ini", "config.ini"],
    insecure_eval: bool = False,
    **kwargs: Any,
) -> "IdentityFunction":
    """Decorate a click command to load options from a config file.

    Parameters
    ----------
    filenames
        List of filenames to load, by default ["config.default.ini", "config.ini"]
    insecure_eval
        Whether or not to allow arbitrary code execution, by default False
    **kwargs
        Passed to click.option directly
    """

    config = read_configs(filenames)

    def decorator(func: FC, /) -> FC:
        # We use reverse-order so that the options are added in the order they appear in the file
        for section in reversed(config.values()):
            for d in reversed(section.values()):
                type_evalled = d.type
                if type_evalled is not None:
                    if insecure_eval:
                        try:
                            type_evalled = eval(type_evalled)
                        except Exception:
                            type_evalled = None
                    else:
                        type_evalled = getattr(builtins, type_evalled, None)

                func = click.option(
                    f"--{d.option_name}"
                    if type_evalled is not bool
                    else f"--{d.option_name}/--no-{d.option_name}",
                    d.programmatic_name,
                    **(
                        dict(  # type: ignore[arg-type]
                            type=type_evalled,
                            default=d.value,
                            required=d.required,
                            help=f"\n{d.description or ''}".replace("\n", "\b\n"),
                            show_default=True,
                        )
                        | kwargs
                    ),
                )(
                    func  # type: ignore[arg-type]
                )

        return func

    # Seems to be a mypy bug?
    # https://github.com/python/mypy/issues/9810
    return decorator  # type: ignore[return-value]
