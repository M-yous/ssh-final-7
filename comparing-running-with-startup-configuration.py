# import required modules/packages/library
import pexpect
import difflib
# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'
# creat the ssh session
session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
# Check the error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()
# Session expecting password, enter details
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- FALLURE! entering password: ', password)
    exit()

# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists the display error and exit
if result != 0:
    print('--- Failure! entering enable mode')
    exit()

# Send enable password details
session.sendline (password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exist then display error and exit
if result != 0:
    print('--- Failure! entering enable mode after sending password')
    exit()

# Enter configuration mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering config mode')
    exit()
# change the hostname to R1
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])    

# check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! setting hostname')

# Saving the file locally
with open("example_file.txt", "w") as open_file:
    # Write the text to the file
    open_file.write("establish-a-ssh-connection.py")

# Exit config mode
session.sendline('exit')

# Get the startup configuration
session.sendline("show startup-config")
session.expect('#')
startup_config_str = session.before

# Get the running configuration
session.sendline("show running-config")
session.expect('#')
running_config_str = session.before

# Create a Differ object
differ = difflib.Differ()
# Compare sequences
diff = differ.compare(startup_config_str, running_config_str)
print('')
print("Comparing the current configuration with startup configuration")
print('--------------------------------------------------------------')
print('')
print(diff)
print('')
for line in diff:
    
   if "--- ip_address" in diff:
       print("Yes")
   else:
       print("No")   
   if "--- username" in diff:
       print("Yes")
   else:
       print("No")
   if "--- password_enable" not in diff:
       print("Yes")
   else:
       print("No")                    

print('')

# Terminate SSH session
session.close()