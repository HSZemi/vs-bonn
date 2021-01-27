#! /usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
	newline_after = False
	for line in f:
		do_print = True
		extra_newline = False
		if line.startswith('§'):
			print(f"\n\n### {line.strip()}")
			do_print = False
			extra_newline = True
		for characters in ('A','B','C','D','E','F','G'):
			if line.startswith(f'{characters}. '):
				print(f"\n# {line.strip()}")
				do_print = False
				extra_newline = True
		for characters in ('I','II','III','IV','V','VI','VII','VIII','IX','X'):
			if line.startswith(f'{characters}. '):
				print(f"\n## {line.strip()}")
				do_print = False
				extra_newline = True
		if line.startswith('('):
			print(f"\n{line.strip()}")
			do_print = False
			extra_newline = False
		if line.startswith('1. '):
			print(f"\n{line.strip()}")
			do_print = False
			extra_newline = False
		if line.startswith('a. '):
			print(f"\n{line.strip()}")
			do_print = False
			extra_newline = False
		if do_print:
			if extra_newline:
				print('')
				extra_newline = False
			print(line.strip())
