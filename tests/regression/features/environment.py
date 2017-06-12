# -*- coding: UTF-8 -*-

import sys
import random
sys.path.append('../../../')
from options import CommandlineOptions
from main import EC2DemoProvisioner

# -- SETUP: create an options object

def before_all(context):
    context.options = TestOptions()
    context.options.args.key_name = 'RegressionTestKey_{0}'.format(random.randint(1, 100))
    context.options.args.key_file = '{0}.pem'.format(context.options.args.key_name)
    context.ec2 = EC2DemoProvisioner(context.options)


class TestOptions(CommandlineOptions):
    def __init__(self, action=None):
        super(TestOptions, self).__init__(test=True)
        self.action = action
        self.zone = 'us-west-2b'
        self.webserver_config = '''#!/bin/bash
 yum update -y
 yum install -y httpd
 systemctl enable httpd
 systemctl start httpd
 firewall-cmd --add-service=http --permanent
 systemctl restart firewalld
 groupadd www
 usermod -a -G www ec2-user
 chown -R root:www /var/www
 chmod 2775 /var/www
 find /var/www -type d -exec chmod 2775 {} +
 find /var/www -type f -exec chmod 0664 {} +
 echo "Automation for the People" > /var/www/html/index.html'''
        self.min_count = 1
        self.max_count = 1
