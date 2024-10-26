# import pty
# import os

import subprocess
# import sys
# import os


# shell = os.environ.get('SHELL', 'sh')
# fil = "./ptyshka"

# with open(fil, 'wb') as rig:
#     def read(fd):
#         data = os.read(fd, 1024)
#         rig.write(data)
#         return data
    

#     pty.spawn(shell, read)

# class Shell:
#     pass





# class SimpleTerminal:
#     def __init__(self):
#         # Start the shell process
#         self.process = subprocess.Popen(
#             ['/usr/bin/bash'],  # Use 'bash' for the terminal
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             bufsize=1,
#             universal_newlines=True
#         )

#     def send_command(self, command):
#         # Send a command to the shell
#         self.process.stdin.write(command + '\n')
#         self.process.stdin.flush()

#     def read_output(self):
#         # Read the output from the shell
#         output = ''
#         # line = ' sa'
#         # while line:
#         #     line = self.process.stdout.readline()
#         #     if line:
#         #         output += line
#         #         print(line)
#         #         if line.strip() == '':  # Detect end of command output
#         #             break
#         #     else:
#         #         break
#         output = os.read(self.process.stdout, 1024)
#         return output

#     def close(self):
#         # Close the shell process
#         self.process.terminate()
#         self.process.wait()

# if True:
#     terminal = SimpleTerminal()

#     try:
#         while True:
#             command = input("Enter a command (or 'exit' to quit): ")
#             if command.lower() == 'exit':
#                 break
#             terminal.send_command(command)
#             output = terminal.read_output()
#             print(output)
#     finally:
#         terminal.close()

subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)