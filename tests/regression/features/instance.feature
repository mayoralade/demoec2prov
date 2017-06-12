Feature: Test Instance Creation, Start and Stop

Scenario: Create an instance
   When the script is run to create an instance
   Then a keypair is created if it does not already exist
   And the instance is created and running

Scenario: Start an instance
   Given an instance is selected from available stopped instances
   When the script is run to start an instance
   Then the instance is running

Scenario: Stop an instance
   Given an instance is selected from available running instances
   When the script is run to stop an instance
   Then the instance is stopped

Scenario: Verify WebServer running
   When a created aws ec2 webserver is running
   Then the public homepage displays Automation for the People
