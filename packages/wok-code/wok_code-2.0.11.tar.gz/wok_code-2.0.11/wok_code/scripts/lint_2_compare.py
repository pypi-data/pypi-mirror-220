#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from lxml import etree
import re

from python_plus import _b, _u
from z0lib import z0lib

__version__ = "2.0.11"


IGNORE_DIRS = (".idea", ".git", "egg-info", "setup")
REGEX_CM = re.compile("(^ *#|^.* #)")
REGEX_OE = re.compile(r"([\"'])https?://www.openerp.com([\"'])")
REGEX_OO = re.compile(r"([\"'])https?://(www.)?odoo.com([\"'])")


def get_names(left_path, right_path):
    left_base = right_base = ""
    while left_path and right_path and left_path != right_path:
        left_base = os.path.basename(left_path)
        right_base = os.path.basename(right_path)
        left_path = os.path.dirname(left_path)
        right_path = os.path.dirname(right_path)
    if not left_base:
        left_base = "left"
    if not right_base:
        right_base = "right"
    return left_base, right_base


def format_xml(opt_args, source, target):
    with open(source, "r") as fd:
        try:
            root = etree.XML(_b(fd.read()))
        except BaseException as e:
            print("%s: ***** Error %s *****" % (source, e))
            root = None
            xml_text = None
    if root is not None:
        try:
            xml_text = _u(etree.tostring(root, pretty_print=True))
        except SyntaxError as e:
            print("%s: ***** Error %s *****" % (source, e))
            xml_text = None
    if xml_text:
        xml_text = xml_text.replace("\n\n", "\n")
        with open(target, "w") as fd:
            fd.write(xml_text)
    else:
        z0lib.run_traced(
            "cp %s %s" % (source, target),
            verbose=opt_args.dry_run,
            dry_run=opt_args.dry_run,
        )


def cp_file(opt_args, left_diff_path, right_diff_path, left_path, right_path, base):
    if (
        base.endswith(".pyc")
        or ((base.endswith(".po") or base.endswith(".pot")) and opt_args.ignore_po)
        or (base.startswith("README") and opt_args.ignore_doc)
        or (base.startswith("LICENSE") and opt_args.ignore_doc)
    ):
        return
    elif os.path.isfile(left_path):
        if base.endswith(".xml"):
            format_xml(opt_args, left_path, os.path.join(left_diff_path, base))
        else:
            z0lib.run_traced(
                "cp %s %s" % (left_path, os.path.join(left_diff_path, base)),
                verbose=opt_args.dry_run,
                dry_run=opt_args.dry_run,
            )
    if os.path.isfile(right_path):
        if base.endswith(".xml"):
            format_xml(opt_args, right_path, os.path.join(right_diff_path, base))
        else:
            z0lib.run_traced(
                "cp %s %s" % (right_path, os.path.join(right_diff_path, base)),
                verbose=opt_args.dry_run,
                dry_run=opt_args.dry_run,
            )


def match(opt_args, left_diff_path, right_diff_path, left_path, right_path):
    if os.path.isfile(left_path):
        base = os.path.basename(left_path)
        cp_file(opt_args, left_diff_path, right_diff_path, left_path, right_path, base)
    elif os.path.isfile(right_path):
        base = os.path.basename(right_path)
        cp_file(opt_args, left_diff_path, right_diff_path, left_path, right_path, base)


def matchdir_based(
    opt_args, left_diff_path, right_diff_path, left_path, right_path, base
):
    left_diff_path = os.path.join(left_diff_path, base)
    if not os.path.isdir(left_diff_path):
        z0lib.run_traced(
            "mkdir %s" % left_diff_path,
            verbose=opt_args.dry_run,
            dry_run=opt_args.dry_run,
        )
    right_diff_path = os.path.join(right_diff_path, base)
    if not os.path.isdir(right_diff_path):
        z0lib.run_traced(
            "mkdir %s" % right_diff_path,
            verbose=opt_args.dry_run,
            dry_run=opt_args.dry_run,
        )
    if os.path.isdir(left_path):
        for fn in os.listdir(left_path):
            base = os.path.basename(fn)
            matchdir(
                opt_args,
                left_diff_path,
                right_diff_path,
                os.path.join(left_path, fn),
                os.path.join(right_path, base),
            )
    if os.path.isdir(right_path):
        for fn in os.listdir(right_path):
            base = os.path.basename(fn)
            if not os.path.exists(os.path.join(left_path, base)):
                matchdir(
                    opt_args,
                    left_diff_path,
                    right_diff_path,
                    os.path.join(left_path, base),
                    os.path.join(right_path, fn),
                )


def matchdir(opt_args, left_diff_path, right_diff_path, left_path, right_path):
    if os.path.isdir(left_path):
        base = os.path.basename(left_path)
        if base not in IGNORE_DIRS:
            matchdir_based(
                opt_args, left_diff_path, right_diff_path, left_path, right_path, base
            )
    elif os.path.isdir(right_path):
        base = os.path.basename(right_path)
        if base not in IGNORE_DIRS:
            matchdir_based(
                opt_args, left_diff_path, right_diff_path, left_path, right_path, base
            )
    else:
        match(opt_args, left_diff_path, right_diff_path, left_path, right_path)


def remove_comment(opt_args, root, files, compare_path=None):
    def remove_identical_files(left_dir, right_dir, fn):
        left_path = os.path.join(left_dir, fn)
        right_path = os.path.join(right_dir, fn)
        sts, stdout, stderr = z0lib.run_traced(
            "diff -r %s %s" % (left_path, right_path),
            verbose=False,
            dry_run=opt_args.dry_run,
        )
        if sts == 0:
            os.unlink(left_path)
            os.unlink(right_path)

    for fn in files:
        ffn = os.path.join(root, fn)
        if not ffn.endswith(".py"):
            if opt_args.purge and compare_path:
                remove_identical_files(root, compare_path, fn)
            continue
        source = ""
        with open(ffn, "r") as fd:
            for line in fd.read().split("\n"):
                line = REGEX_OE.sub(r"\1https://www.odoo.com\2", line)
                line = REGEX_OO.sub(r"\1https://www.odoo.com\2", line)
                x = REGEX_CM.match(line)
                if x:
                    source += "%s\n" % (line[x.start() : x.end() - 1].rstrip() or "#")
                else:
                    source += "%s\n" % line.rstrip()
        with open(ffn, "w") as fd:
            fd.write(source)
        if opt_args.purge and compare_path:
            remove_identical_files(root, compare_path, fn)


def lintdir(opt_args, left_path, right_path):
    z0lib.run_traced(
        "black %s" % left_path, verbose=opt_args.dry_run, dry_run=opt_args.dry_run
    )
    z0lib.run_traced(
        "black %s" % right_path, verbose=opt_args.dry_run, dry_run=opt_args.dry_run
    )
    if opt_args.ignore_doc:
        for root, _dirs, files in os.walk(left_path):
            remove_comment(opt_args, root, files)
        for root, _dirs, files in os.walk(right_path):
            compare_path = None
            if root.startswith(right_path):
                compare_path = left_path + root[len(right_path) :]
            remove_comment(opt_args, root, files, compare_path=compare_path)


def main(cli_args=None):
    cli_args = cli_args or sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Compare 2 paths after formatted them in the same way",
        epilog="© 2021-2023 by SHS-AV s.r.l.",
    )
    parser.add_argument("-b", "--odoo-version")
    parser.add_argument("-c", "--cache", action="store_true", help="Use cached values")
    parser.add_argument(
        "-d",
        "--ignore-doc",
        action="store_true",
        help="Ignore README, docs and comment in files",
    )
    parser.add_argument("-i", "--ignore-po", action="store_true")
    parser.add_argument("-m", "--meld", action="store_true", help="Use meld")
    parser.add_argument(
        "-P",
        "--purge",
        action="store_true",
        help="Purge identical files on temporary dirs",
    )
    parser.add_argument("-n", "--dry-run", dest="dry_run", action="store_true")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument("left_path")
    parser.add_argument("right_path", nargs="?")
    opt_args = parser.parse_args(cli_args)
    if not opt_args.right_path:
        # When just 1 path is issued, current directory become the left path
        # that is the reference path
        opt_args.right_path = os.path.abspath(opt_args.left_path)
        opt_args.left_path = os.path.abspath(os.getcwd())
    else:
        opt_args.right_path = os.path.abspath(opt_args.right_path)
    opt_args.left_path = os.path.abspath(opt_args.left_path)
    if (
        os.path.isfile(opt_args.left_path)
        and os.path.isdir(opt_args.right_path)
        or os.path.isdir(opt_args.left_path)
        and os.path.isfile(opt_args.right_path)
    ):
        print("Cannot compare file against dir!")
    diff_path = os.path.expanduser("~/tmp/diff")
    if not os.path.isdir(os.path.dirname(diff_path)):
        os.mkdir(os.path.dirname(diff_path))
    if not os.path.isdir(diff_path):
        os.mkdir(diff_path)
    left_base, right_base = get_names(opt_args.left_path, opt_args.right_path)
    left_diff_path = os.path.join(diff_path, left_base)
    right_diff_path = os.path.join(diff_path, right_base)
    if (
        not opt_args.cache
        or not os.path.isdir(left_diff_path)
        or not os.path.isdir(right_diff_path)
    ):
        if os.path.isdir(left_diff_path):
            z0lib.run_traced(
                "chmod -R +w %s" % left_diff_path,
                verbose=opt_args.dry_run,
                dry_run=opt_args.dry_run,
            )
            z0lib.run_traced(
                "rm -fR %s" % left_diff_path,
                verbose=opt_args.dry_run,
                dry_run=opt_args.dry_run,
            )
        if os.path.isdir(right_diff_path):
            z0lib.run_traced(
                "chmod -R +w %s" % right_diff_path,
                verbose=opt_args.dry_run,
                dry_run=opt_args.dry_run,
            )
            z0lib.run_traced(
                "rm -fR %s" % right_diff_path,
                verbose=opt_args.dry_run,
                dry_run=opt_args.dry_run,
            )
        z0lib.run_traced(
            "mkdir %s" % left_diff_path,
            verbose=opt_args.dry_run,
            dry_run=opt_args.dry_run,
        )
        z0lib.run_traced(
            "mkdir %s" % right_diff_path,
            verbose=opt_args.dry_run,
            dry_run=opt_args.dry_run,
        )
        matchdir(
            opt_args,
            left_diff_path,
            right_diff_path,
            opt_args.left_path,
            opt_args.right_path,
        )
        lintdir(opt_args, left_diff_path, right_diff_path)
        z0lib.run_traced(
            "chmod -R -w %s" % left_diff_path,
            verbose=opt_args.dry_run,
            dry_run=opt_args.dry_run,
        )
        z0lib.run_traced(
            "chmod -R -w %s" % right_diff_path,
            verbose=opt_args.dry_run,
            dry_run=opt_args.dry_run,
        )
    if opt_args.meld:
        sts, stdout, stderr = z0lib.run_traced(
            "meld %s %s" % (left_diff_path, right_diff_path),
            verbose=True,
            dry_run=opt_args.dry_run,
        )
    else:
        sts, stdout, stderr = z0lib.run_traced(
            "diff -r %s %s" % (left_diff_path, right_diff_path),
            verbose=True,
            dry_run=opt_args.dry_run,
        )
    print(stdout, stderr)
    return sts


if __name__ == "__main__":
    exit(main())
