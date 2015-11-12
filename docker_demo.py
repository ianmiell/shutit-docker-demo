"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class docker_demo(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#                                    - Returns True if any lines in output match any of
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#                                    - Get input from user and return output
		# shutit.fail(msg)                   - Fail the program and exit with status 1
		#
		shutit.send('rm -rf /tmp/docker_demo')
		shutit.send('mkdir -p /tmp/docker_demo')
		shutit.send('cd /tmp/docker_demo')
		shutit.send('vagrant init ubuntu/trusty64')
		shutit.send('vagrant up --provider virtualbox')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su')
		shutit.send('cat /etc/issue',note='We are in an ubuntu environment.')
		shutit.send('yum install httpd',note='yum does not work!',check_exit=False)
		shutit.install('docker.io',note='Install docker')
		# Start up a centos container (docker run)
		shutit.login(command='docker run -ti centos:centos7 bash',note='Start up an instance of a centos:centos7 container. This downloads the centos:centos7 docker image.')
		# yum install something
		shutit.send('yum install -y telnet',note='Now we can use yum to install telnet')
		# run top
		shutit.send('top -b -n 1',note='Note that we only see the process we started this container with (bash), and no OS-level processes - these are running on the host.')
		# show network
		shutit.send('ifstat',note='Within the docker container we "see" our own network.')
		shutit.logout(note='Log out of the container')

		# docker images (docker images)
		shutit.send('docker images',note='Back on the host machine, we can see what images are now downloaded')
		# docker ps (docker ps)
		shutit.send('docker ps -a',note='See that we have a container that is now exited (because the bash process ended when we quit), but is still available for us to manipulate.')

		# start up 20 docker containers in the background (docker run -d) and name them (docker run --name)
		shutit.send('for c in {1..20}; do docker run -d --name container_$c centos:centos7 sleep infinity; done',note='Start 20 centos:centos7 containers in the background (-d[aemon]), each with their own name (--name container_<num>, and running "sleep" only.')

		# run top on 'host'
		shutit.send('top -b -n 1 | head',note='Running top on the host, these 20 containers use minimal resources')

		# enter one, create a file (docker exec)
		shutit.login(command='docker exec -ti container_15 bash',note='Enter container 15 with a bash shell')
		shutit.send('touch /tmp/hello_container_15',note='Create a file on this container, and exit')
		shutit.logout(note='Log out of the container')

		# file not on host
		shutit.send('ls /tmp/hello_container_15',note='Back on the host, and the file is not there',check_exit=False)
		# enter another one, file not there
		shutit.login(command='docker exec -ti container_3 bash',note='Enter container 3 with a bash shell')
		shutit.send('ls /tmp/hello_container_15',note='On container 3 the file is not there',check_exit=False)
		shutit.logout(note='Log out of the container')

		shutit.login(command='docker exec -ti container_15 bash',note='Back to container 15 with a bash shell')
		shutit.send('ls /tmp/hello_container_15',note='On container 15 the file is still there')
		shutit.logout(note='Log out of the container')
		# commit the first one and give resulting image a name, (docker commit -t)
		shutit.send('ID=$(docker commit container_15)',note='Commit our changed container as an image')
		shutit.send('docker tag $ID mycontainer',note='Tag the image with a memorable name')

		shutit.send('docker images',note='docker images now shows mycontainer has been tagged')

		shutit.login(command='docker run -ti --name mycontainer_1 mycontainer bash',note='Start container up from this image and give it the name "mycontainer_1"')
		shutit.send('ls /tmp/hello_container_15',note='The file is there in my newly created container')
		shutit.logout(note='Log out of the container')

		shutit.send('docker ps -a',note='Back on the host, get the list of containers, and you can see mycontainer_15 and mycontainer_1 exist as separate containers')
		# docker rm (docker rm)
		shutit.send('docker ps -a -q | xargs docker rm -f',note='Kill all the containers')



		# dockerfiles (docker build)

		# docker rmi (docker rmi)

		# docker volumes - persistence (docker -v)

		shutit.pause_point('')
		shutit.logout('Log out of root on the VM')
		shutit.logout('Log out of the VM')
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return docker_demo(
		'shutit.docker_demo.docker_demo.docker_demo', 1418326705.00,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)

