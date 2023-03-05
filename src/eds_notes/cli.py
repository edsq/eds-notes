import argparse

from eds_notes.utils import simple_diff


def simple_diff_cli():
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
        "--comment-char",
        help="The character(s) indicating the following line is a comment.",
        default="#",
    )

    args = parser.parse_args()

    simple_diff(
        file=args.filename,
        comparison_commit=args.commit,
        context=args.context,
        show_filename=args.no_show_filename,
        comment_char=args.comment_char,
    )
