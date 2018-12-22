
import re
import sys
import json
import yaml
import getopt

from pprint import pprint
from urllib.request import Request, urlopen


def main(query, num=100, debug=False):
	url = f"https://www.google.com/search?q={query}&oq={query}&gl=us&hl=en&num={num}"
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	res = urlopen(req).read().decode().replace('><', '>\n<')

	res = re.sub(r'<head>.*</head>', '', res, flags=re.S)
	res = res.split('\n')[3:]
	res = [ x + '\n' for x in res ]

	if debug:
		with open('results.html', 'w') as f:
			f.writelines(res)

	start_flag = None
	re_groups = []
	for i in range(len(res)):
		if res[i][:3] == '<h3':
			start_flag = i
		elif res[i][-8:] == '</cite>\n' and start_flag is not None:
			re_groups.append(res[start_flag: i + 1])
			start_flag = None

	re_groups = [ ''.join(y.strip() for y in x) + '\n' for x in re_groups ]

	if debug:
		with open('scratch.txt', 'w') as f:
			f.writelines(re_groups)

	p = r'.*<a[^>]*>(.*)</a>.*<cite>(.*)</cite>.*'
	re_finds = []

	for x in map(lambda x: list(map(list, re.findall(p, x))), re_groups):
		re_finds.extend(x)

	re_finds = [ [ x[0].strip().replace('\n', ''), x[1].strip().replace('\n', '') ] 
				for x in re_finds 
				if '...' not in x[1] ]

	print(json.dumps(re_finds))

	if debug:
		with open('dump.yaml', 'w') as f:
			yaml.dump(re_finds, f, default_flow_style=False)


if __name__ == '__main__':
	# Defining parameter options
	short_flags = "dn:q:"
	long_flags = [ "debug", "num=", "query=" ]
	raw_args = sys.argv[1:]

	# Not catching getopt.err on purpose, since I can't think of a better error message yet
	opts, f_args = getopt.getopt(raw_args, short_flags, long_flags)

	# Initialising the two parameters to main
	num, query, debug = None, None, False

	for arg, val in opts:
		if arg in ('--num', '-n'):
			num = val
		elif arg in ('--query', '-q'):
			query = val
		elif arg in ('--debug', '-d'):
			debug=True
		
	# Check that query has been passed since it has no default
	if query is None:
		raise ValueError('Missing non-optional argument --query or -q')

	if num is None:
		main(query)
	else:
		main(query, num)
