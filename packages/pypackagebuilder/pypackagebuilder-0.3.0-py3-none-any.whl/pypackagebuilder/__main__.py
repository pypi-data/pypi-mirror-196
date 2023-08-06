import logging
import argparse
import shutil
import sys

try:
    # NOTE: tomllib is available only for python >=3.11
    import tomllib
except Exception:
    import toml

from pathlib import Path
from typing import Optional
from build import ProjectBuilder
from pyc_wheel import main as pyc_wheel_main
from twine.commands.check import check
from twine.commands.upload import upload
from twine.settings import Settings

log = logging.getLogger(__name__)


class Setup:
    def __init__(self, toml_file: Path = Path("pyproject.toml")) -> None:
        try:
            with toml_file.open("rb") as f:
                self.cfg = tomllib.load(f)
        except NameError:
            self.cfg = toml.load(str(toml_file))

        self.name = self.cfg["project"]["name"].replace("-", "_")
        self.version = self.cfg["project"]["version"]

    def _get_dest_pckg_name(self, pyver: str) -> str:
        return f"{self.name}-{self.version}-{pyver}-none-any.whl"

    def build(
        self, pyver: str, output_dir: Path = Path.cwd() / "dist", quiet: bool = True
    ) -> None:
        log.info(f"Building {self._get_dest_pckg_name(pyver)} ...")

        if (output_dir / self._get_dest_pckg_name(pyver)).exists():
            log.warning(
                f"WHL already exist (overwriting): {output_dir / self._get_dest_pckg_name(pyver)}"
            )

        config_settings = {}
        if quiet:
            config_settings["--quiet"] = ""

        # build
        ProjectBuilder(str(Path.cwd())).build(
            distribution="wheel",
            output_directory=str(output_dir),
            config_settings=config_settings,
        )

        # rename output file with correct python version
        shutil.move(
            output_dir / f"{self.name}-{self.version}-py3-none-any.whl",
            output_dir / self._get_dest_pckg_name(pyver),
        )

        log.info(f"Build SUCESS: {output_dir / self._get_dest_pckg_name(pyver)}")

    def pyc_compile(
        self, pyver: str, directory: Path = Path.cwd() / "dist", quiet: bool = True
    ) -> None:
        log.info(f"Compiling {self._get_dest_pckg_name(pyver)} ...")

        args = [str(directory / self._get_dest_pckg_name(pyver))]
        if quiet:
            args += ["--quiet"]

        # compiling to .pyc
        pyc_wheel_main(args)

        log.info(f"Compilation SUCESS: {directory / self._get_dest_pckg_name(pyver)}")

    def check(self, pyver: Optional[str] = None, directory: Path = Path.cwd() / "dist") -> None:
        if pyver:
            whl_pattern = self._get_dest_pckg_name(pyver)
        else:
            whl_pattern = f"{self.name}-{self.version}*.whl"

        log.info(f"Checking whl '{whl_pattern}' ...")

        check(dists=[f"{str(directory)}/{whl_pattern}"], strict=False)

        log.info("Check SUCESS")

    def publish(self, repo: str, directory: Path = Path.cwd() / "dist") -> None:
        log.info(f"Publishing '{self.name}-{self.version}*.whl' ...")

        upload(
            upload_settings=Settings(repository_name=repo),
            dists=[f"{str(directory)}/{self.name}-{self.version}*.whl"],
        )

        log.info("Publish SUCESS")


class ParseLoggingArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = getattr(logging, values.upper())
        setattr(namespace, self.dest, values)


class ParsePathResolvedArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = Path(values).resolve()
        setattr(namespace, self.dest, values)


class LocalArgsManager(argparse.ArgumentParser):
    def __init__(self, prog: str, description: Optional[str] = None):
        super().__init__(prog=prog, description=description)

    def _add_logging_arguments(self, parser, default_lvl=logging.WARNING):
        parser.add_argument(
            "--log",
            type=str,
            default=default_lvl,
            action=ParseLoggingArgument,
            choices=["critical", "error", "warning", "info", "debug"],
            help="Level of console logger.",
        )

    def parse_arguments(self, args) -> argparse.Namespace:
        args = [a.strip() for a in args if a.strip()]
        return self.parse_args(args)

    def set_parsers(self) -> "LocalArgsManager":
        subparser = self.add_subparsers(dest="action", help="action type")
        self._add_build_subcommand(subparser)
        self._add_compile_subcommand(subparser)
        self._add_check_subcommand(subparser)
        self._add_publish_subcommand(subparser)
        return self

    def _add_build_subcommand(self, parser) -> None:
        command_parser = parser.add_parser("build", help="Build package")
        command_parser.add_argument(
            "pyversion", type=str, help="""Python version for which the package will be built"""
        )
        command_parser.add_argument(
            "--output",
            type=str,
            action=ParsePathResolvedArgument,
            default=(Path.cwd() / "dist").resolve(),
            help="""Directory for output whl files.""",
        )
        self._add_logging_arguments(command_parser, default_lvl=logging.INFO)

    def _add_compile_subcommand(self, parser) -> None:
        command_parser = parser.add_parser(
            "compile", help="Compile package to pyc (precompiled python) files"
        )
        command_parser.add_argument(
            "pyversion", type=str, help="""Python version for which the package will be compile"""
        )
        command_parser.add_argument(
            "--dir",
            type=str,
            action=ParsePathResolvedArgument,
            default=(Path.cwd() / "dist").resolve(),
            help="""Directory where whl files will be compiled""",
        )
        self._add_logging_arguments(command_parser, default_lvl=logging.INFO)

    def _add_check_subcommand(self, parser) -> None:
        command_parser = parser.add_parser("check", help="Check whl files")
        command_parser.add_argument(
            "--pyversion",
            type=str,
            help="""Python version for which the package will be compile""",
        )
        command_parser.add_argument(
            "--dir",
            type=str,
            action=ParsePathResolvedArgument,
            default=(Path.cwd() / "dist").resolve(),
            help="""Directory where whl files will be checked""",
        )
        self._add_logging_arguments(command_parser, default_lvl=logging.INFO)

    def _add_publish_subcommand(self, parser) -> None:
        command_parser = parser.add_parser(
            "publish", help="Publish package to the external repository"
        )
        command_parser.add_argument(
            "repo", type=str, help="""Python package repoitory name (e.x. pypi, testpypi)"""
        )
        command_parser.add_argument(
            "--dir",
            type=str,
            action=ParsePathResolvedArgument,
            default=(Path.cwd() / "dist").resolve(),
            help="""Directory from which whl files will be published""",
        )
        self._add_logging_arguments(command_parser, default_lvl=logging.INFO)


def main(argv=sys.argv[1:]):
    args = LocalArgsManager("pypackagebuilder").set_parsers().parse_arguments(argv)

    # logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(int(args.log))
    console_handler.setFormatter(logging.Formatter(r"[%(levelname)-8s]:%(message)s"))
    logger.addHandler(console_handler)

    log.debug(f"Script arguments: {args}")

    if args.action == "build":
        Setup().build(pyver=args.pyversion, output_dir=args.output, quiet=True)
    elif args.action == "compile":
        Setup().pyc_compile(pyver=args.pyversion, directory=args.dir, quiet=True)
    elif args.action == "check":
        Setup().check(pyver=args.pyversion, directory=args.dir)
    elif args.action == "publish":
        Setup().publish(repo=args.repo, directory=args.dir)


if __name__.rpartition(".")[-1] == "__main__":
    sys.exit(main(sys.argv[1:]))
