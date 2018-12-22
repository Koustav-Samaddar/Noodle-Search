
import re
import yaml

from pprint import pprint
from urllib.request import urlretrieve, install_opener, build_opener, Request, urlopen


def main():
	search = 'wormhole'
	query = f"https://www.google.com/search?q={search}&oq={search}&gl=us&hl=en&num=100"
	req = Request(query, headers={'User-Agent': 'Mozilla/5.0'})
	res = urlopen(req).read().decode().replace('><', '>\n<')

	res = re.sub(r'<head>.*</head>', '', res, flags=re.S)
	res = res.split('\n')[3:]
	res = [ x + '\n' for x in res ]

	with open('results.html', 'w') as f:
		f.writelines(res)

	print("Finished downloading the html file")

	start_flag = None
	re_groups = []
	for i in range(len(res)):
		if res[i][:3] == '<h3':
			start_flag = i
			print("Start triggered")
		elif res[i][-8:] == '</cite>\n' and start_flag is not None:
			re_groups.append(res[start_flag: i + 1])
			start_flag = None
			print("End triggered")

	re_groups = [ ''.join(y.strip() for y in x) + '\n' for x in re_groups ]

	with open('scratch.txt', 'w') as f:
		f.writelines(re_groups)

	p = r'.*<a[^>]*>(.*)</a>.*<cite>(.*)</cite>.*'
	re_finds = []

	for x in map(lambda x: list(map(list, re.findall(p, x))), re_groups):
		re_finds.extend(x)

	re_finds = [ [ x[0].strip().replace('\n', ''), x[1].strip().replace('\n', '') ] for x in re_finds if '...' not in x[1] ]

	pprint(re_finds)

	with open('dump.yaml', 'w') as f:
		yaml.dump(re_finds, f, default_flow_style=False)

	print("Finished parsing the html file")


if __name__ == '__main__':
	main()
