#!/usr/bin/env python3

import os
import sys

argv = sys.argv[1:]

for root, directory, _file in os.walk('.'):

	for _ in _file:

		_archivo = os.path.join(root, _)

		if (os.path.isfile(_archivo)):

			cmd = os.system('cat "%s" | grep -i "%s"' % (_archivo, argv[0]))
			if (cmd == 0):
				print(_archivo)
