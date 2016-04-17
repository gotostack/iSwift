#!/usr/bin/env python
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import optparse
import os
import subprocess
import sys

here = os.path.dirname(__file__)


def main():
    usage = "usage: %prog [file1..fileN]"
    description = """With no file paths given this script will automatically
compress all jQuery-based files of the admin app. Requires the Google Closure
Compiler library and Java version 6 or later."""
    parser = optparse.OptionParser(usage, description=description)
    parser.add_option("-c", dest="compiler", default="~/bin/compiler.jar",
                      help="path to Closure Compiler jar file")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()

    compiler = os.path.expanduser(options.compiler)
    if not os.path.exists(compiler):
        sys.exit("Google Closure compiler jar file %s not found. "
                 "Please use the -c option to specify the path." % compiler)

    if not args:
        if options.verbose:
            sys.stdout.write("No filenames given; "
                             "defaulting to admin scripts\n")
        args = [os.path.join(here, f) for f in [
            "actions.js", "collapse.js", "inlines.js", "prepopulate.js"]]

    for arg in args:
        if not arg.endswith(".js"):
            arg = arg + ".js"
        to_compress = os.path.expanduser(arg)
        if os.path.exists(to_compress):
            to_compress_min = "%s.min.js" % "".join(arg.rsplit(".js"))
            cmd = "java -jar %s --js %s --js_output_file %s" % (
                compiler,
                to_compress,
                to_compress_min)
            if options.verbose:
                sys.stdout.write("Running: %s\n" % cmd)
            subprocess.call(cmd.split())
        else:
            sys.stdout.write(
                "File %s not found. Sure it exists?\n" % to_compress)


if __name__ == '__main__':
    main()
