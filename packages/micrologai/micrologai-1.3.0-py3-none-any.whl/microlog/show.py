#
# Microlog. Copyright (c) 2023 laffra, dcharbon. All rights reserved.
#

import sys

import microlog.api as api


if __name__ == "__main__":
    name = sys.argv[1]
    try:
        # check if the user passed an absolute path
        path, name = sys.argv[1].split("/logs/")
    except:
        pass
    api.runner.showLog(name)