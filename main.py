#!/usr/bin/env python
'''
Demo Script to provison a webserver on Amazon EC2
'''
import sys
import os
from time import sleep
import boto3
import botocore.exceptions
from options import CommandlineOptions


class EC2DemoProvisioner(object):
    '''
        Demo EC2 Provisioner for Linux WebServer
    '''
    def __init__(self, options):
        self.options = options
        self.client = boto3.client('ec2')
        self.instance = {}

    def get_instance_states(self):
        '''
            Get all current running instances
        '''
        all_instances = []
        states = self.client.describe_instance_status()
        for state in states.values()[:-1]:
            for instance in state:
                all_instances.append({'Instance ID': instance['InstanceId'],
                                      'State': instance['InstanceState']['Name']})

        return all_instances

    def get_instance_status(self, instance_id):
        '''
            Get the status of a single instance
        '''
        all_instances = self.get_instance_states()
        for instance in all_instances:
            if instance_id in instance.values():
                return instance['State']

    def create_new_instance(self):
        '''
            Create a new EC2 instance, defaults to t2.micro type, see config file for more info
        '''
        self.instance = self.client.run_instances(ImageId=self.options.args.image_id,
                                                  MinCount=self.options.min_count,
                                                  MaxCount=self.options.max_count,
                                                  KeyName=self.options.args.key_name,
                                                  InstanceType=self.options.args.instance_type,
                                                  Placement={'AvailabilityZone': self.options.zone},
                                                  Monitoring={'Enabled': False},
                                                  UserData=self.options.webserver_config)

        return self.instance['Instances'][0]['InstanceId']

    def key_pair_exists(self):
        '''
            Check if the private key file exists
        '''
        return os.path.isfile(self.options.args.key_file)\
                 and os.path.getsize(self.options.args.key_file) > 0

    def create_keypair(self):
        '''
            Create new keypair to use with the EC2 instance
        '''
        if not self.key_pair_exists():
            try:
                key_pair = self.client.create_key_pair(KeyName=self.options.args.key_name)
                with open(self.options.args.key_file, 'w') as kpfile:
                    kpfile.write(key_pair['KeyMaterial'])
                    os.chmod(self.options.args.key_file, 0400)
            except botocore.exceptions.ClientError:
                confirm_progress('KeyPair already exist')
        else:
            confirm_progress('KeyPair file already exists')

    def get_instance_public_ip(self, iid):
        '''
            Get the public ip address for the given instance
        '''
        instance_data = self.client.describe_instances(InstanceIds=[iid])
        return instance_data['Reservations'][0]['Instances'][0]['PublicIpAddress']

    def start_instance(self, instance_id):
        '''
            Start the given instance
        '''
        self.client.start_instances(InstanceIds=[instance_id])

    def stop_instance(self, instance_id):
        '''
            Stop the given instance
        '''
        self.client.stop_instances(InstanceIds=[instance_id])

    def poll_for_state(self, iid, state, timeout):
        '''
            Wait for machine to get to desired state, timeout if it takes too long
        '''
        sleep_time = 30
        while self.get_instance_status(iid) != state:
            if sleep_time >= timeout:
                sys.exit('Instance is taking too long to provison, exiting...')
            print 'Please wait, instance is being created...'
            sleep(sleep_time)
            sleep_time += sleep_time

def confirm_progress(msg):
    '''
        Provide use input to proceed with operation
    '''
    print msg
    should_proceed = raw_input('Will you like to proceed? [Y/N]')
    if should_proceed in ['N', 'n', 'No', 'no']:
        sys.exit('Aborting Operation')

def main():
    '''
        Main Function

        This either starts, stops, gets status or creates an instance
    '''
    options = CommandlineOptions()
    provisioner = EC2DemoProvisioner(options)
    if options.args.start:
        provisioner.start_instance(options.args.instance)
    elif options.args.end:
        provisioner.stop_instance(options.args.instance)
    elif options.args.create:
        instances = provisioner.get_instance_states()
        if instances:
            confirm_progress('You already have {0} instance running'.format(len(instances)))
        provisioner.create_keypair()
        iid = provisioner.create_new_instance()
        provisioner.poll_for_state(iid, 'running', '300')
        ip_addr = provisioner.get_instance_public_ip(iid)
        print '\nYou can access the webserver homepage at: http://{0}/\n'.format(ip_addr)

    return provisioner.get_instance_states()


if __name__ == '__main__':
    print main()
