import cProfile
import optparse
import os
import sys

from scrapy.cmdline import (
    garbage_collect,
    _get_commands_from_entry_points,
    _get_commands_from_module,
    _pop_command_name,
    _run_print_help,
)
from scrapy.utils.project import get_project_settings, inside_project

import os_scrapy
from .patch import CrawlerProcess
from os_scrapy.settings import default_settings


def _run_command_profiled(cmd, args, opts):
    if opts.profile:
        sys.stderr.write("os-scrapy: writing cProfile stats to %r\n" % opts.profile)
    loc = locals()
    p = cProfile.Profile()
    p.runctx("cmd.run(args, opts)", globals(), loc)
    if opts.profile:
        p.dump_stats(opts.profile)


def _run_command(cmd, args, opts):
    if opts.profile:
        _run_command_profiled(cmd, args, opts)
    else:
        cmd.run(args, opts)


def _print_header(settings, inproject):
    if inproject:
        print(
            "OS-Scrapy %s - project: %s\n"
            % (os_scrapy.__version__, settings["BOT_NAME"])
        )
    else:
        print("OS-Scrapy %s - no active project\n" % os_scrapy.__version__)


def _print_commands(settings, inproject):
    _print_header(settings, inproject)
    print("Usage:")
    print("  os-scrapy <command> [options] [args]\n")
    print("Available commands:")
    cmds = _get_commands_dict(settings, inproject)
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass.short_desc()))
    if not inproject:
        print()
        print("  [ more ]      More commands available when run from project directory")
    print()
    print('Use "os-scrapy <command> -h" to see more info about a command')


def _print_unknown_command(settings, cmdname, inproject):
    _print_header(settings, inproject)
    print("Unknown command: %s\n" % cmdname)
    print('Use "os-scrapy" to see available commands')


def _get_commands_dict(settings, inproject):
    cmds = _get_commands_from_module("scrapy.commands", inproject)
    cmds.update(_get_commands_from_module("os_scrapy.commands", inproject))
    cmds.update(_get_commands_from_entry_points(inproject))
    cmds_module = settings["COMMANDS_MODULE"]
    if cmds_module:
        cmds.update(_get_commands_from_module(cmds_module, inproject))
    return cmds


def _print_commands(settings, inproject):
    _print_header(settings, inproject)
    print("Usage:")
    print("  os-scrapy <command> [options] [args]\n")
    print("Available commands:")
    cmds = _get_commands_dict(settings, inproject)
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass.short_desc()))
    if not inproject:
        print()
        print("  [ more ]      More commands available when run from project directory")
    print()
    print('Use "os-scrapy <command> -h" to see more info about a command')


def execute(argv=None, settings=None):
    return _execute(argv, settings)


def _execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv

    if settings is None:
        settings = get_project_settings()
        settings.setmodule(default_settings, "default")
        # set EDITOR from environment if available
        try:
            editor = os.environ["EDITOR"]
        except KeyError:
            pass
        else:
            settings["EDITOR"] = editor

    inproject = inside_project()
    cmds = _get_commands_dict(settings, inproject)
    cmdname = _pop_command_name(argv)
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(), conflict_handler="resolve"
    )
    if not cmdname:
        _print_commands(settings, inproject)
        sys.exit(0)
    elif cmdname not in cmds:
        _print_unknown_command(settings, cmdname, inproject)
        sys.exit(2)

    cmd = cmds[cmdname]
    parser.usage = "os-scrapy %s %s" % (cmdname, cmd.syntax())
    parser.description = cmd.long_desc()
    settings.setdict(cmd.default_settings, priority="command")
    cmd.settings = settings
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    _run_print_help(parser, cmd.process_options, args, opts)

    cmd.crawler_process = CrawlerProcess(settings)
    _run_print_help(parser, _run_command, cmd, args, opts)
    sys.exit(cmd.exitcode)


if __name__ == "__main__":
    try:
        execute()
    finally:
        # Twisted prints errors in DebugInfo.__del__, but PyPy does not run gc.collect()
        # on exit: http://doc.pypy.org/en/latest/cpython_differences.html?highlight=gc.collect#differences-related-to-garbage-collection-strategies
        garbage_collect()
