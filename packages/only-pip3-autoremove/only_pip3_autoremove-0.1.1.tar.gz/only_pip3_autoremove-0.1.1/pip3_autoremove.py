from __future__ import annotations
from argparse import ArgumentParser
from collections import defaultdict
import sys, subprocess, pip

from pkg_resources import (
    DistributionNotFound,
    VersionConflict,
    get_distribution,
    working_set
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterable, Callable, TypeVar
    from pkg_resources import Distribution
    Graph = defaultdict[Distribution, set[Distribution]]
    T = TypeVar("T")

__version__ = "0.1.1"

try:
    # pip >= 10.0.0 hides main in pip._internal. We'll monkey patch what we need and hopefully this becomes available
    # at some point.
    from pip._internal import logger, main # pyright: ignore

    pip.main = main
    pip.logger = logger # pyright: ignore
    ###
except (ModuleNotFoundError, ImportError):
    pass

WHITELIST = {"pip", "setuptools", "pip3-autoremove", "wheel"}

def get_leaves(graph: Graph):
    def is_leaf(node: Distribution) -> bool:
        return not graph[node]

    return filter(is_leaf, graph)

def exclude_whitelist(dists: set[Distribution]) -> set[Distribution]:
    """Return a new set with the items of WHITELIST removed."""
    return {dist for dist in dists if dist.project_name not in WHITELIST}

def fixed_point(f: Callable[[T], T], x: T) -> T:
    """Run F(X) until the returned value equals X, then return X."""
    while True:
        y = f(x)

        if y == x:
            return x

        x = y

def find_dead(graph: Graph, dead: set[Distribution]) -> set[Distribution]:
    def is_killed_by_us(node: Distribution) -> bool:
        succ = graph[node]
        # If SUCC has items not in DEAD, they have been killed by us
        return bool(succ) and not (succ - dead) # TODO: My change might produce an error

    return dead | set(filter(is_killed_by_us, graph))

def show_tree(dist: Distribution, dead: set[Distribution], indent: int=0,
              visited: set[Distribution] | None=None) -> None:
    if visited is None:
        visited = set()

    # This package is already visited
    if dist in visited:
        return

    # Exclude this from further searches
    visited.add(dist)

    # Print the package
    print(" " * 4 * indent, end="")
    show_dist(dist)

    for req in requires(dist):
        if req in dead:
            # Requirement is dead, so print a tree of it
            show_tree(req, dead, indent + 1, visited)

def find_all_dead(graph: Graph, start: set[Distribution]) -> set[Distribution]:
    """Return all of the dead packages in GRAPH."""
    return fixed_point(lambda d: find_dead(graph, d), start)

def list_dead(names: Iterable[str]):
    start: set[Distribution] = set()

    for name in names:
        try:
            start.add(get_distribution(name))
        except DistributionNotFound:
            print("%s is not an installed pip module, skipping" % name, file=sys.stderr)
        except VersionConflict:
            print(
                "%s is not the currently installed version, skipping" % name,
                file=sys.stderr,
            )

    graph = get_graph()
    dead = exclude_whitelist(find_all_dead(graph, start))

    for d in start:
        show_tree(d, dead)

    return dead

def requires(dist: Distribution) -> list[Distribution]:
    """Return the requirements for DIST."""
    required: list[Distribution] = []

    for pkg in dist.requires():
        try:
            required.append(get_distribution(pkg))
        except VersionConflict as e:
            print(e.report(), file=sys.stderr)
            print("Redoing requirement with just package name...", file=sys.stderr)
            required.append(get_distribution(pkg.project_name))
        except DistributionNotFound as e:
            print(e.report(), file=sys.stderr)
            print("Skipping %s" % pkg.project_name, file=sys.stderr)

    return required

def get_graph() -> Graph:
    """Return a graph representing every package and its requirements."""
    g = defaultdict(set)

    for dist in working_set:
        g[dist]
        for req in requires(dist):
            g[req].add(dist)

    return g

def show_freeze(dist: Distribution) -> None:
    print(dist.as_requirement())

def show_dist(dist: Distribution) -> None:
    print("%s %s (%s)" % (dist.project_name, dist.version, dist.location))

def list_leaves(freeze=False):
    graph = get_graph()

    for node in get_leaves(graph):
        if freeze:
            show_freeze(node)
        else:
            show_dist(node)

def confirm(prompt: str, /) -> bool:
    """Prompt the user for a yes/no answer."""
    return input(prompt) == "y"

def remove_dists(dists: set[Distribution]):
    if sys.executable:
        pip_cmd = [sys.executable, "-m", "pip"]
    else:
        pip_cmd = ["pip3"]

    subprocess.check_call(pip_cmd + ["uninstall", "-y"] + [d.project_name for d in dists])

def autoremove(names: Iterable[str], yes: bool=False) -> None:
    dead = list_dead(names)

    if dead and (yes or confirm("Uninstall (y/N)? ")):
        remove_dists(dead)

def create_parser():
    """Create argument parser."""
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-L", "--leaves", action="store_true",
                       help="list leaves (packages that are not used by any others)")
    group.add_argument("-f", "--freeze", action="store_true",
                       help="list leaves (packages that are not used by any others) in requirements.txt format")

    parser.add_argument("-l", "--list", action="store_true",
                        help="list unused dependencies, but don't uninstall them")

    parser.add_argument("-y", "--yes", action="store_true",
                        help="do not prompt before removal")

    parser.add_argument("packages", metavar="ARG", nargs="*",
                        help="a Python package")

    return parser

def main():
    parser = create_parser()

    args = parser.parse_args()

    if args.leaves or args.freeze:
        list_leaves(args.freeze)
    elif args.list:
        list_dead(args.packages)
    elif not args.packages:
        # No packages
        print("No packages have been provided.", file=sys.stderr)
        parser.print_help()
    else:
        autoremove(args.packages, args.yes)

if __name__ == "__main__":
    main()
