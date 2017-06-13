# miniproject-ALADEOJEBI-MAYOWA

A simple Python application that provisions a simple web server from AWS EC2

## Requirements

This mini project depends on `boto3`, the AWS SDK for Python, and requires
Python 2.6.5+, 2.7, 3.3, 3.4, or 3.5. You can install `boto3` using pip:

    pip install boto3

## Basic Configuration

You need to set up your AWS security credentials before the sample code is able
to connect to AWS. You can do this by installing awscli via pip and running:

    aws configure

You will need aws_access_key_id and aws_secret_access_key

See the [Security Credentials](http://aws.amazon.com/security-credentials) page
for more information on getting your keys.

## Running the script

This sample application connects to Amazon's [Elastic Compute Cloud (EC2)](http://aws.amazon.com/ec2),
 creates a linux ec2 t2.micro instance (RHEL 7) by default, configures httpd to
 display. The script will generate a bucket name and file for you. All you need 
 to do is run the code:

    python main.py
    Usage: main.py [options]
    Provision a Demo Linux Web Server on Amazon EC2
   
    You need to set up your AWS security credentialsbefore this code is able to
    connect to AWS. You can pip install awscli and run aws configure
   
    Options:
      -h, --help            show this help message and exit
      -i IMAGE_ID, --image-id=IMAGE_ID
                            The AMI to use for provisioning
      -f CONFIGFILEPATH, --configuration-file-path=CONFIGFILEPATH
                            The path to the config file
      -k KEY_NAME, --key-name=KEY_NAME
                            The KeyPair Name
      -r KEY_FILE, --key-file=KEY_FILE
                            The key file to save the private key
      -t INSTANCE_TYPE, --instance-type=INSTANCE_TYPE
                            The Amazon preconfigured instance type to use
      -c, --create-instance
                            Halt a running instance
      -s, --start-instance  Fire up an instance
      -e, --stop-instance   Halt a running instance
      -z, --instance-status
                            Halt a running instance
      -d INSTANCE, --instance-id=INSTANCE
                        Provide instance id

You need to make sure the credentials you're using have the correct permissions to access the Amazon EC2 service.
The configuration file enables you modify the ec2 zone, webserver config e.t.c.

## Testing

Testing was done via regression tests using Behave framework

    pip install behave

To run the tests

    behave tests/regression/features/instance.feature

## License

None

