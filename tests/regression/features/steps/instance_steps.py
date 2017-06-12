# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
import sys
import random
import urllib2
from time import sleep
sys.path.append('../../../')
from behave import *


@given('an instance is selected from available {action} instances')
def step_impl(context, action): #stopped
    all_instances = context.ec2.get_instance_states(action)
    random_instance = random.choice(all_instances)
    context.instance_id = random_instance['Instance ID']
    #for item in all_instances:
    #    if item['Instance ID'] == 'i-0d5de7f2e3b68efb1':
    #        continue
    ##context.instance_id = all_instances[0]['Instance ID']
    #    context.instance_id = item['Instance ID']
    #    break

@when('the script is run to {action} an instance')
def step_impl(context, action):
    if action == 'create':
        context.ec2.create_keypair()
        context.instance_id = context.ec2.create_new_instance()
        sleep(30)
    elif action == 'stop':
        context.ec2.stop_instance(context.instance_id)
        sleep(60)
    elif action == 'start':
        context.ec2.start_instance(context.instance_id)
        sleep(60)

@when('a created aws ec2 webserver is running')
def step_impl(context):
    context.execute_steps(u"""given an instance is selected from available {action} instances""".format(action="stopped"))
    context.execute_steps(u"""when the script is run to {action} an instance""".format(action="start"))

@then('a keypair is created if it does not already exist')
def step_impl(context):
    assert context.ec2.verify_key_pairs(context.options.args.key_name) is True

@then('the instance is {action}') # running, created, stopped
def step_impl(context, action):
    if action == 'created and running':
        action = 'running'
    context.instance_status = context.ec2.get_instance_status(context.instance_id, action)
    assert(context.instance_status == action)

@then('the public homepage displays {msg}')
def step_impl(context, msg):
    context.ip = context.ec2.get_instance_public_ip(context.instance_id)
    sleep(15)
    context.homepage = urllib2.urlopen(urllib2.Request('http://{0}/'.format(context.ip))).read().strip()
    print(context.homepage)
    assert(context.homepage == msg)
