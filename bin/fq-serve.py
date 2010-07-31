#!/usr/bin/env python
import os, sys, subprocess
from clx import OptionParser, Program
import boto.ec2

EC2_REGION = 'us-west-1'

class FreequeryServeOptionParser(OptionParser):
    pass


class FreequeryServe(Program):
    __ec2_connection = None
#    def __init__(self, **kwargs):
#        self.__ec2_connection = None
#        Program.__init__(self, **kwargs)
    
    @property
    def option_dict(self):
        return dict((k, v) for k, v in self.options.__dict__.iteritems()
                           if v is not None)

    @property
    def ec2_connection(self):
        if self.__ec2_connection is not None:
            return self.__ec2_connection
        if not os.getenv('AWS_ACCESS_KEY_ID') or \
           not os.getenv('AWS_SECRET_ACCESS_KEY'):
            raise Exception("must set AWS_ACCESS_KEY_ID and " \
                            "AWS_SECRET_ACCESS_KEY env vars")
        self.__ec2_connection = boto.ec2.connect_to_region(EC2_REGION)
        return self.__ec2_connection

    def ssh(self, url, cmd, **args):
        args["stdout"] = args.get("stdout", subprocess.PIPE)
        args["stderr"] = args.get("stderr", subprocess.STDOUT)
        p = subprocess.Popen(["ssh", "-q",
                              "-o", "UserKnownHostsFile=/dev/null",
                              "-o", "StrictHostKeyChecking=no",
                              'root@' + url, cmd], **args)
        return p

    def process_instances(self, hosts, op, m):
        proc = [(host, op(host)) for host in hosts]
        print >> sys.stderr, "%s:" % m,
        for i, p in enumerate(proc):
            if p[1].wait():
                die("Operation failed on host %s." % host)
            print >> sys.stderr, i + 1,
        print >> sys.stderr, "ok."

    def distribute_file(self, instances, path, content, change_owner = False):
        def copy_file(host):
            own = ""
            dir = os.path.dirname(path) 
            if change_owner:
		own = "touch %s; chmod 400 %s;"\
                    "chown -R disco:disco %s;" % (path, path, dir)
            p = self.ssh(host, "mkdir %s 2>/dev/null;%s cat > %s"\
                             % (dir, own, path), stdin = subprocess.PIPE)
            p.stdin.write(content)
            p.stdin.close()
            return p
        self.process_instances(instances, copy_file, "Copy %s" % path)


@FreequeryServe.command
def start(program, what, *hosts):
    def start_daemon(host):
        if what == 'disco_master':
            p = program.ssh(host, "cd /srv/disco && sudo -u disco disco start")
            return p
    program.process_instances(hosts, start_daemon, "Start %s" % what)

@FreequeryServe.command
def stop(program, what, *hosts):
    def stop_daemon(host):
        if what == 'disco_master':
            p = program.ssh(host, "cd /srv/disco && sudo -u disco disco stop")
            return p
    program.process_instances(hosts, stop_daemon, "Stop %s" % what)

    
@FreequeryServe.command
def setup(program, *hosts):
    def make_sshkey(master):
       print >> sys.stderr, "Generating an ssh key on the master..",
       
       if program.ssh(master, "echo 'StrictHostKeyChecking no' >> "\
        "/etc/ssh/ssh_config").wait():
           die("Couldn't modify ssh_config")
           
       p = program.ssh(master,
               "mkdir -p /srv/disco && "\
               "(useradd -d /srv/disco -s /bin/bash disco > /dev/null " \
                           "2>&1 || echo -n) && " \
               "chown -R disco:disco /srv/disco && " \
               "rm -Rf /srv/disco/.ssh/; mkdir /srv/disco/.ssh && " \
               "ssh-keygen -N '' -f /srv/disco/.ssh/id_dsa >/dev/null && " \
               "chown -R disco:disco /srv/disco/.ssh/ && " \
               "cat /srv/disco/.ssh/id_dsa.pub", stdout = subprocess.PIPE)
       key = p.stdout.read()
       if p.wait():
           die("Key generation failed.")
       print >> sys.stderr, "ok."
       return key

    def get_cookie(master):
        p = program.ssh(master, "cat /srv/disco/.erlang.cookie",
                        stdout = subprocess.PIPE)
        cookie = p.stdout.read()
        if p.wait():
            die("Couldn't read ~/.erlang.cookie")
        return cookie

    sshkey = make_sshkey(hosts[0])
    cookie = get_cookie(hosts[0])
    program.distribute_file(hosts, "/srv/disco/.ssh/authorized_keys", sshkey,
                            change_owner=True)
    program.distribute_file(hosts, "/srv/disco/.erlang.cookie", cookie,
                            change_owner=True)

    program.distribute_file(hosts, "freequery-remote-install.sh",
                            open('bin/remote-install.sh', 'rb').read())
    def run_install(host):
        p = program.ssh(host, "sh freequery-remote-install.sh")
        return p
    program.process_instances(hosts, run_install, "Run install script")
    program.distribute_file(hosts, "/etc/disco/settings.py",
                            open('conf/disco_settings.py', 'rb').read(),
                            change_owner=True)                  

@FreequeryServe.command
def instances(program):
    resvs = program.ec2_connection.get_all_instances()
    for resv in resvs:
        for inst in resv.instances:
            if inst.state == 'running':
                print "%s\t%s\t%s" % (inst.id, inst.ip_address, inst.state)

    
if __name__ == '__main__':
    FreequeryServe(option_parser=FreequeryServeOptionParser()).main()
