import pexpect, time

USER = "pi"
PASS = "piminer1"
COMMAND_PROMPT = "[#$]"
SSH_NEWKEY = "(?i)are you sure you want to continue connecting"
TERMINAL_PROMPT = "(?i)terminal type\?"

class ExpectHandler(object):
	def __init__(self, host):
		self.host = host
		self.user = USER
		self.password = PASS

	def copy(self, file_name):
		child = pexpect.spawn("scp -o StrictHostKeyChecking=no {} {}@{}:src/cgminer/".format(file_name, self.user, self.host))
		ret = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, COMMAND_PROMPT, "(?i)password"])
		if ret == 0:
		   print "ERROR! Could not login with SCP. Here is what SCP said:"
#		   print child.before, child.after
		if ret == 1:
		   child.sendline("yes")
		   child.expect("(?i)password")
		if ret == 2:
		   pass
		if ret == 3:
		   child.sendline(self.password)
		   ret = child.expect([pexpect.EOF, COMMAND_PROMPT, TERMINAL_PROMPT])
		   if ret == 2:
			   child.sendline(TERMINAL_TYPE)

	def copyhome(self, file_name):
		child = pexpect.spawn("scp -o StrictHostKeyChecking=no {} {}@{}:".format(file_name, self.user, self.host))
		ret = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, COMMAND_PROMPT, "(?i)password"])
		if ret == 0:
		   print "ERROR! Could not login with SCP. Here is what SCP said:"
#		   print child.before, child.after
		if ret == 1:
		   child.sendline("yes")
		   child.expect("(?i)password")
		if ret == 2:
		   pass
		if ret == 3:
		   child.sendline(self.password)
		   ret = child.expect([pexpect.EOF, COMMAND_PROMPT, TERMINAL_PROMPT])
		   if ret == 2:
			   child.sendline(TERMINAL_TYPE)

	def run(self, cmdlines):
		child = pexpect.spawn("ssh -o StrictHostKeyChecking=no {}@{}".format(self.user, self.host))
		ret = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, COMMAND_PROMPT,"(?i)password", pexpect.EOF])
		if ret == 0:
		   print "ERROR! Could not login with SSH. Here is what SSH said."
#		   print chile.before, child.after
		if ret == 1:
		   child.sendline("yes")
		   child.expect("(?i)password")
		if ret == 2:
		   pass
		if ret == 3:
		   child.sendline(self.password)
		   child.expect(COMMAND_PROMPT)
		if ret == 4:
		   print "cannot connect."
		for cmd in cmdlines:
		   child.sendline(cmd)
		   child.expect(COMMAND_PROMPT)
		   print child.before, child.after
		   time.sleep(5)
