from rc import VON_BASE_PATH
from view import APPLY_COLOR
import view

import os
import cmd
import traceback
import shlex
import controller
import glob

import readline
readline.set_completer_delims(' \t\n')

WELCOME_STRING = APPLY_COLOR("BOLD_YELLOW", "Welcome to VON!")
GOODBYE_STRING = APPLY_COLOR("BOLD_YELLOW", "OK, goodbye! :D")

def _complete_path(path):
	if os.path.isdir(path):
		return glob.glob(os.path.join(path, '*'))
	else:
		return glob.glob(path+'*')

class VonTerminal(cmd.Cmd, controller.VonController):
	def getcwd(self):
		return os.getcwd().replace(VON_BASE_PATH.rstrip("/"), '')

	@property
	def prompt(self):
		return APPLY_COLOR("BOLD_CYAN", "VON") + \
				APPLY_COLOR("CYAN", self.getcwd()) + \
				"\n" + APPLY_COLOR("BOLD_GREEN", ":)") + " "

	def emptyline(self):
		pass

	def completedefault(self, text, line, start_idx, end_idx):
		return _complete_path(text)

	def run(self):
		print WELCOME_STRING
		if not os.getcwd().startswith(VON_BASE_PATH):
			os.chdir(VON_BASE_PATH) # set cwd
		while 1:
			try:
				self.cmdloop()
				break
			except KeyboardInterrupt:
				print "^C"
			except SystemExit:
				pass
			except:
				traceback.print_exc()
		print "\n" + GOODBYE_STRING 

	def onecmd(self, line):
		"""Interpret the argument as though it had been typed in response
		to the prompt."""
		if line.strip() == "":
			return self.emptyline()
		_ = shlex.split(line)
		cmd = _[0]
		argv = _[1:]
		self.lastcmd = line
		if line == 'EOF' :
			self.lastcmd = ''
			return 1
		else:
			try:
				func = getattr(self, 'do_' + cmd)
			except AttributeError:
				return self.default(line)
			return func(argv)

	def direct(self, cargs):
		# cargs = sys.argv ostensibly
		if len(cargs) == 0:
			view.error("No command given")
		cmd = cargs[0]
		if hasattr(self, 'do_' + cmd):
			func = getattr(self, 'do_' + cmd)
			func(cargs[1:])
		else:
			view.error("Command {} not recognized".format(cmd))

	def do_help(self, argv):
		arg = ''.join(argv)
		if arg:
			try:
				func = getattr(self, 'do_' + arg)
			except AttributeError:
				views.error('Command {} not found'.format(arg))
			else:
				print APPLY_COLOR("MAGENTA", "Getting `{} --help`...".format(arg))
				func(['--help'])
		else:
			print "Here is a list of available commands:"
			for name in sorted(self.get_names()):
				if name[:3] == 'do_' and name != 'do_help' and name != 'do_EOF':
					print name[3:]
	
# vim: fdm=marker
