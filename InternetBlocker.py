import os
import subprocess
from datetime import datetime as dt

class BlockInternet:
    """Blocks INTERNET access to the provided sites."""

    def __init__(self, starting_time=10, ending_time=17):
        self.localhost = '127.0.0.1'
        self.site_file = 'sites.txt'  # File containing websites to block
        self.ending_time = ending_time
        self.starting_time = starting_time
        self.host_file = '/etc/hosts'  # Path to hosts file on Kali Linux

    def is_admin(self):
        """Check if the program is running in administrative mode."""
        return os.getuid() == 0

    def is_working_hour(self):
        """Check if it is within the working hours."""
        current_time = dt.now()
        return dt(current_time.year, current_time.month, current_time.day, self.starting_time) < current_time < dt(
            current_time.year, current_time.month, current_time.day, self.ending_time
        )

    def read_file(self, file):
        """Read the content of the specified file."""
        with open(file, 'r') as f:
            return [line.strip('\n') for line in f.readlines() if line.strip('\n')]

    def write_file(self, contents):
        """Write the provided content to the hosts file."""
        with open(self.host_file, 'w') as f:
            is_newline = False
            for content in contents:
                if content.startswith(self.localhost) and not is_newline:
                    # Add a newline before adding any site in the hosts file
                    f.write(f'\n{content}\n')
                    is_newline = True
                else:
                    f.write(f'{content}\n')

    def main(self):
        """Block internet access to the sites specified in sites.txt."""
        lines = self.read_file(self.host_file)
        sites = self.read_file(self.site_file)

        if self.is_working_hour():
            for site in sites:
                exclude = f'{self.localhost} \t{site}'
                if exclude not in lines:
                    lines.append(exclude)
        else:
            lines = [line for line in lines if not line.startswith(self.localhost)]

        self.write_file(lines)

if __name__ == '__main__':
    block_internet = BlockInternet()

    if not block_internet.is_admin():
        print("Please run this script with sudo privileges.")
        exit()

    while True:
        block_internet.main()
