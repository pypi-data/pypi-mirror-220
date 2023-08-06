############################################################################
#                                                                          #
# Copyright (c) 2019-2023 Carl Drougge                                     #
# Modifications copyright (c) 2020 Anders Berkeman                         #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#  http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
#                                                                          #
############################################################################


from __future__ import print_function
from __future__ import division


a_example = r"""description = r'''
This is just an example. It doesn't even try to do anything useful.

You can run it to see that your installation works.
'''

options = dict(
	message=str,
)

def analysis(sliceno):
	return sliceno

def synthesis(analysis_res):
	print("Sum of all sliceno:", sum(analysis_res))
	print("Message:", options.message)
"""


build_script = r"""def main(urd):
	urd.build('example', message='Hello world!')
"""


methods_conf_template = r"""# The {name} package uses auto-discover in accelerator.conf,
# so you don't need to write anything here.
#
# But if you want to override the interpreter for some method, you can.
# For example:
# some_method 2.7
# would run some_method on the 2.7 interpreter.
"""


config_template = r"""# The configuration is a collection of key value pairs.
#
# Values are specified as
# key: value
# or for several values
# key:
# 	value 1
# 	value 2
# 	...
# (any leading whitespace is ok)
#
# Use ${{VAR}} or ${{VAR=DEFAULT}} to use environment variables.
#
# Created by accelerator version {version}

slices: {slices}
workdirs:
	{name} ./workdirs/{name}

# Target workdir defaults to the first workdir, but you can override it.
# (this is where jobs without a workdir override are built)
target workdir: {name}

method packages:
	{name} auto-discover
	{examples} auto-discover
	accelerator.standard_methods
	accelerator.test_methods

# listen directives can be [host]:port or socket path.
# urd should be prefixed with "local" to run it together with the server
# or "remote" to not run it together with the server.
listen: {listen.server}
board listen: {listen.board}
urd: local {listen.urd}

result directory: ./results
input directory: {input}

# If you want to run methods on different python interpreters you can
# specify names for other interpreters here, and put that name after
# the method in methods.conf.
# You automatically get four names for the interpreter that started
# the server: DEFAULT, {major}, {major}.{minor} and {major}.{minor}.{micro} (adjusted to the actual
# version used). You can override these here, except DEFAULT.
# interpreters:
# 	2.7 /path/to/python2.7
# 	test /path/to/beta/python
"""


def find_free_ports(low, high, count=3, hostname='localhost'):
	import random
	import socket
	ports = list(range(low, high - count))
	random.shuffle(ports)
	res = {}
	def free(port):
		if port not in res:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				s.bind((hostname, port))
				res[port] = True
			except socket.error:
				res[port] = False
			s.close()
		return res[port]
	for port in ports:
		if all(free(port + n) for n in range(count)):
			return port
	raise Exception('Failed to find %d consecutive free TCP ports on %s in range(%d, %d)' % (count, hostname, low, high))


def git(method_dir):
	from subprocess import check_call
	from accelerator.compat import FileNotFoundError
	from sys import stderr
	from os.path import exists
	if exists('.git'):
		print('WARNING: .git already exists, skipping git init', file=stderr)
		return
	try:
		check_call(['git', 'init', '--quiet'])
	except FileNotFoundError:
		print('WARNING: git appears to not be installed, skipping git init', file=stderr)
		return
	with open('.gitignore', 'w') as fh:
		fh.write('/.socket.dir\n')
		fh.write('/urd.db\n')
		fh.write('/workdirs\n')
		fh.write('/results\n')
		fh.write('__pycache__\n')
		fh.write('*.pyc\n')
	check_call(['git', 'add', '--', 'accelerator.conf', '.gitignore', method_dir])


def main(argv, cfg):
	from os import makedirs, listdir, chdir
	from os.path import exists, join, realpath, dirname
	from sys import version_info
	from argparse import RawTextHelpFormatter
	from accelerator.shell.parser import ArgumentParser
	from accelerator.compat import shell_quote
	from accelerator.error import UserError
	from accelerator.extras import DotDict
	import accelerator

	parser = ArgumentParser(
		prog=argv.pop(0),
		description=r'''
			creates an accelerator project directory.
			defaults to the current directory.
			creates accelerator.conf, a method dir, a workdir and result dir.
			both the method directory and workdir will be named <NAME>,
			"dev" by default.
		'''.replace('\t', ''),
		formatter_class=RawTextHelpFormatter,
	)
	parser.add_argument('--slices', default=None, type=int, help='override slice count detection')
	parser.add_argument('--name', default='dev', help='name of method dir and workdir, default "dev"')
	parser.add_argument('--input', default='# /some/path where you want import methods to look.', help='input directory')
	parser.add_argument('--force', action='store_true', negation='dont', help='go ahead even though directory is not empty, or workdir\nexists with incompatible slice count')
	parser.add_argument('--tcp', default=False, metavar='HOST/PORT', nargs='?', help='listen on TCP instead of unix sockets.\nspecify HOST (can be IP) to listen on that host\nspecify PORT to use range(PORT, PORT + 3)\nspecify both as HOST:PORT')
	parser.add_argument('--no-git', action='store_true', negation='yes', help='don\'t create git repository')
	parser.add_argument('--examples', action='store_true', negation='no', help='copy examples to project directory')
	parser.add_argument('directory', default='.', help='project directory to create. default "."', metavar='DIR', nargs='?')
	options = parser.parse_intermixed_args(argv)

	assert options.name
	assert '/' not in options.name

	if options.tcp is False:
		listen = DotDict(
			board='.socket.dir/board',
			server='.socket.dir/server',
			urd='.socket.dir/urd',
		)
	else:
		hostport = options.tcp or ''
		if hostport.endswith(']'): # ipv6
			host, port = hostport, None
		elif ':' in hostport:
			host, port = hostport.rsplit(':', 1)
		elif hostport.isdigit():
			host, port = '', hostport
		else:
			host, port = hostport, None
		if port:
			port = int(port)
		else:
			port = find_free_ports(0x3000, 0x8000)
		listen = DotDict(
			server='%s:%d' % (host, port,),
			board='%s:%d' % (host, port + 1,),
			urd='%s:%d' % (host, port + 2,),
		)

	if not options.input.startswith('#'):
		options.input = shell_quote(realpath(options.input))
	prefix = realpath(options.directory)
	workdir = join(prefix, 'workdirs', options.name)
	slices_conf = join(workdir, '.slices')
	try:
		with open(slices_conf, 'r') as fh:
			workdir_slices = int(fh.read())
	except IOError:
		workdir_slices = None
	if workdir_slices and options.slices is None:
		options.slices = workdir_slices
	if options.slices is None:
		from multiprocessing import cpu_count
		options.slices = cpu_count()
	if workdir_slices and workdir_slices != options.slices and not options.force:
		raise UserError('Workdir %r has %d slices, refusing to continue with %d slices' % (workdir, workdir_slices, options.slices,))

	if not options.force and exists(options.directory) and listdir(options.directory):
		raise UserError('Directory %r is not empty.' % (options.directory,))
	if not exists(options.directory):
		makedirs(options.directory)
	chdir(options.directory)
	for dir_to_make in ('.socket.dir', 'urd.db',):
		if not exists(dir_to_make):
			makedirs(dir_to_make, 0o750)
	for dir_to_make in (workdir, 'results',):
		if not exists(dir_to_make):
			makedirs(dir_to_make)
	with open(slices_conf, 'w') as fh:
		fh.write('%d\n' % (options.slices,))
	method_dir = options.name
	if not exists(method_dir):
		makedirs(method_dir)
	with open(join(method_dir, '__init__.py'), 'w') as fh:
		pass
	with open(join(method_dir, 'methods.conf'), 'w') as fh:
		fh.write(methods_conf_template.format(name=options.name))
	with open(join(method_dir, 'a_example.py'), 'w') as fh:
		fh.write(a_example)
	with open(join(method_dir, 'build.py'), 'w') as fh:
		fh.write(build_script)
	if options.examples:
		from shutil import copytree
		from accelerator import examples
		copytree(dirname(examples.__file__), 'examples')
		examples = 'examples'
	else:
		examples = '# accelerator.examples'
	with open('accelerator.conf', 'w') as fh:
		fh.write(config_template.format(
			name=shell_quote(options.name),
			slices=options.slices,
			version=accelerator.__version__,
			examples=examples,
			input=options.input,
			major=version_info.major,
			minor=version_info.minor,
			micro=version_info.micro,
			listen=DotDict({k: shell_quote(v) for k, v in listen.items()}),
		))
	if not options.no_git:
		git(method_dir)
