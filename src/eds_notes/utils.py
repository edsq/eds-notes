import subprocess


def simple_diff(
    file, comparison_commit=None, context=3, show_filename=True, comment_fmt="# {}"
):
    """Print a simplified git diff that doesn't show lines removed.

    We also remove the header and the "@@" lines, placing an ellipsis surrounded by two
    blank lines between modified hunks.

    Parameters
    ----------
    file : str
        The file to diff.
    comparison_commit : str, optional
        A commit to compare against.  The default behavior is "HEAD", but you could, for
        example, compare against the parent of HEAD with "HEAD~".
    context : int, optional
        The number of lines of context to show.
    show_filename : bool, optional
        Whether to print the filename at the top of the diff as a comment.
    comment_fmt : str, optional
        The comment format to use.  A pair of (empty) curly braces will be substituted
        by the comment.  For example, showing the comment `"foobar.txt"` with
        `comment_fmt="# {}"` will produce the comment `"# foobar.txt"`.
    """
    # Get diff output
    # `--unified=0` means zero context lines will be included in each hunk
    if comparison_commit is None:
        cmd = ["git", "diff", "--unified=0"] + [file]

    else:
        cmd = ["git", "diff", "--unified=0"] + [comparison_commit, file]

    # Call subprocess.run with check=True, which raises an error if we get a nonzero
    # exit code
    completed_proc = subprocess.run(cmd, capture_output=True, check=True)
    git_out = completed_proc.stdout.decode("utf-8")
    git_out_lines = git_out.splitlines()

    if len(git_out_lines) == 0:
        raise ValueError(f"{file} is unchanged since comparison commit")

    # Parse hunks
    raw_hunks = []  # list of [start, stop) indices for each hunk
    for line in git_out_lines:
        if line[:2] == "@@":
            # Line looks like "@@ -1,3 +2,4 @@", meaning hunk from previous version
            # started at line 1 and goes for 3 lines, and hunk from new version starts
            # at line 2 and goes for 4 lines.
            newhunk = line.split()[2][1:]  # Index from 1 to get rid of leading '+'
            newhunk_split = newhunk.split(",")
            if len(newhunk_split) == 1:
                start = newhunk_split[0]
                n_lines = 1

            else:
                start, n_lines = newhunk_split

            hunk_start = int(start) - 1  # diff indexes from 1, so we need to subtract 1
            hunk_end = hunk_start + int(n_lines)
            raw_hunks.append((hunk_start - context, hunk_end + context))

    # Combine hunks if needed
    first_hunk = raw_hunks[0]
    if first_hunk[0] < 0:
        hunks = [[0, first_hunk[1]]]

    else:
        hunks = [list(first_hunk)]

    for next_hunk in raw_hunks[1:]:
        last_hunk = hunks[-1]

        if last_hunk[1] >= next_hunk[0]:
            # Combine this hunk with the last
            last_hunk[1] = next_hunk[1]

        else:
            hunks.append(list(next_hunk))

    # Get lines to print
    with open(file, "r") as f:
        file_lines = f.read().splitlines()

    out_lines = []
    if show_filename:
        out_lines.append(comment_fmt.format(file))

    if hunks[0][0] > 0:
        # Add ellipsis at beginning
        out_lines += ["...", ""]

    out_lines += file_lines[hunks[0][0] : hunks[0][1]]

    if len(hunks) > 1:
        for hunk in hunks[1:]:
            out_lines += ["", "...", ""]
            out_lines += file_lines[hunk[0] : hunk[1]]

    if hunks[-1][1] < len(file_lines):
        # Add ellipsis at end
        out_lines += ["", "..."]

    print("\n".join(out_lines))
