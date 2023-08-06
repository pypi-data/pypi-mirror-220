import asyncio
from sys import stderr

from potoo.app import Potoo
from potoo.cli import parse_cli_arguments
from potoo.export import export


def main() -> int:
    args = parse_cli_arguments()
    app = Potoo(
        args["markdown_file"],
        args["header_split_level"],
        not any([args["export"], not args["no_fragments"]]),
        args["static_footer"],
        args["hot_reload"],
    )
    app.dark = not args["light_mode"]
    if args["export"]:
        return asyncio.run(
            export(
                app,
                args["export_terminal_size"],
                export_dir=args["export_dir"],
                format=args["export"],
            )
        )
    # Set terminal title to presentation title
    stderr.write(f"\x1b]2;{app.slides[0][0].splitlines()[0]}\x07")
    stderr.flush()
    app.run()

    return 0
