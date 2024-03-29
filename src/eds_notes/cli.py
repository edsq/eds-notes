import argparse

from eds_notes.utils import simple_diff


def simple_diff_cli():
    """CLI for utils.simple_diff."""
    parser = argparse.ArgumentParser(
        description="Print a simple git diff, omitting lines removed."
    )
    parser.add_argument("commit", help="The commit to compare against.", nargs="?")
    parser.add_argument("filename", help="The file to git diff.")
    parser.add_argument(
        "--context",
        help="Lines of context to show around each hunk.",
        default=3,
        type=int,
    )
    parser.add_argument(
        "--no-show-filename",
        help="Whether to print the filename at the top of the diff as a comment.",
        action="store_false",
    )
    parser.add_argument(
        "--comment-fmt",
        help="The comment format to use.  A pair of (empty) curly braces will be "
        + "substituted by the comment.",
        default="# {}",
    )

    args = parser.parse_args()

    simple_diff(
        file=args.filename,
        comparison_commit=args.commit,
        context=args.context,
        show_filename=args.no_show_filename,
        comment_fmt=args.comment_fmt,
    )
