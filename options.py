'''
This manages all options passed to this application
'''

import sys
from optparse import OptionParser
import ConfigParser


#pylint: disable=too-few-public-methods
class CommandlineOptions(object):
    '''
        Manages the command line options and configuration file parameters
    '''
    def __init__(self):
        self.parser = CommandlineOptions.__parse_options()
        (self.args, _) = self.parser.parse_args()
        if (self.args.start or self.args.end) and not self.args.instance:
            sys.exit('Provide the Instance ID to start or stop, exiting...')
        elif self.args.create:
            CommandlineOptions.__validate_input(self.args.key_name,\
                                                'Please provide key_pair name to use')
            CommandlineOptions.__validate_input(self.args.key_file,\
                                                'Please provide key_file to use')
            config = ConfigParser.RawConfigParser()
            config.read(self.args.configFilePath)
            self.zone = config.get('setup', 'zone')
            self.webserver_config = config.get('setup', 'webserver_config')
            self.min_count = int(config.get('setup', 'min_count'))
            self.max_count = int(config.get('setup', 'max_count'))
        elif self.args.start or self.args.end or self.args.status:
            pass
        else:
            self.parser.print_help()
            sys.exit(0)

    @staticmethod
    def __parse_options():
        '''
            Command Line Option Parser
        '''
        usage = '%prog [options]\n Provision a Demo Linux Web Server on Amazon EC2'
        description = '\nYou need to set up your AWS security credentials\
before this code is able to connect to AWS. \
You can pip install awscli and run aws configure'
        parser = OptionParser(usage=usage, description=description)
        parser.add_option('--image-id', '-i',
                          help='The AMI to use for provisioning',
                          dest='image_id',
                          default="ami-6f68cf0f")
        parser.add_option('--configuration-file-path', '-f',
                          help='The path to the config file',
                          dest='configFilePath',
                          default='setup.cfg')
        parser.add_option('--key-name', '-k',
                          help='The KeyPair Name',
                          dest='key_name',
                          default=None)
        parser.add_option('--key-file', '-r',
                          help='The key file to save the private key',
                          dest='key_file',
                          default=None)
        parser.add_option('--instance-type', '-t',
                          help='The Amazon preconfigured instance type to use',
                          dest='instance_type',
                          default='t2.micro')
        parser.add_option('--create-instance', '-c',
                          help='Halt a running instance',
                          dest='create',
                          action='store_true',
                          default=None)
        parser.add_option('--start-instance', '-s',
                          help='Fire up an instance',
                          dest='start',
                          action='store_true',
                          default=None)
        parser.add_option('--stop-instance', '-e',
                          help='Halt a running instance',
                          dest='end',
                          action='store_true',
                          default=None)
        parser.add_option('--instance-status', '-z',
                          help='Halt a running instance',
                          dest='status',
                          action='store_true',
                          default=None)
        parser.add_option('--instance-id', '-d',
                          help='Provide instance id',
                          dest='instance',
                          default=None)
        return parser

    @staticmethod
    def __validate_input(option, msg):
        if not option:
            sys.exit('{0}'.format(msg))
