from os.path import abspath, exists, join

import os_scrapy_cookiecutter
from cookiecutter.main import cookiecutter
from scrapy.commands.startproject import Command as ScrapyCommand
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):
    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option(
            "-p",
            "--package",
            dest="package",
            action="store_true",
            help="create project as package",
        )

    def run(self, args, opts):
        if not opts.package:
            return super(Command, self).run(args, opts)

        if len(args) not in (1, 2):
            raise UsageError()

        project_name = args[0]
        project_dir = args[0]

        if len(args) == 2:
            project_dir = args[1]

        if exists(join(project_dir, "scrapy.cfg")):
            self.exitcode = 1
            print("Error: scrapy.cfg already exists in %s" % abspath(project_dir))
            return

        if not self._is_valid_name(project_name):
            self.exitcode = 1
            return

        try:
            cookiecutter(
                os_scrapy_cookiecutter.TEMPLATE_DIR,
                no_input=True,
                extra_context={
                    "project_name": project_name,
                    "project_dir": project_dir,
                },
            )
        except Exception as e:
            self.exitcode = 1
            print(f"Error: create project with cookiecutter {e}")
            return
