# site
import click

# package
from .util import collect_demos


class DemoIdType(click.ParamType):
    name = "demoid"

    def shell_complete(self, ctx, param, incomplete):
        demo_names = (demo["id"] for demo in collect_demos())
        return [
            click.shell_completion.CompletionItem(name)
            for name in demo_names
            if name.startswith(incomplete)
        ]
