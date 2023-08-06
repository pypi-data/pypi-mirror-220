# from Utilities.package import Process, logger
from pyassist import Process
# Contains Network related functions
class Network(Process):

    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = (f"{__class__}".split("'")[1])
        self.get_logger(**kwargs)
        self.debug(f"Initialized: {kwargs['name']}")


    # rsync_service
    # * Performs RSync operation with different options
    # @param rsync_options  - Options given for RSync command
    # @param ssh_options    - If RSync is done via SSH provide that option also
    # @param from_dir      - Local directory to sync
    # @param to_dir     - Remote directory to sync
    # @param remote_address - Ip Address/ Hostname of remote machine
    # @param remote_user    - Remote user login(Optional if configured in ~/.ssh/config)
    # @return bool

    def rsync_service(self, rsync_options, ssh_options, from_dir,
                to_dir, remote_address, remote_user=""):
        # If remote user is given add @
        if(remote_user):
            remote_user = remote_user + "@"
        o, e = self.run_process(
                ["rsync" + " "
                + rsync_options + ' "'
                + ssh_options + '" '
                + from_dir + " "
                + remote_user
                + remote_address + ":"
                + to_dir
                ], False)
        o = self.decode(o)
        e = self.decode(e)
        if(e):
            if("Permanently added" in e):
                pass
            # If Build fails terminate there
            else:
                self.info("Error while RSync, check log for details")
                self.info("Output: " + o)
                self.info("Error: " + e)
                return False
        
        self.info("RSync is success")
        return True

    # vpn_service
    # * Start/ Stop the given VPN
    # @param vpn_name - VPN name
    # @param action - Start/ Stop
    # @return bool

    def vpn_service(self, vpn_name, action):
        con_list = self.decode(self.run_process(["nmcli con"], False)[0]).split("\n")

        # Check and update action
        if(
                (action == "enable") or
                (action == "up")    or
                (action == "start")
            ):
            action = "up"
        elif(
                (action == "disable") or
                (action == "down") or
                (action == "stop")
            ):
            action = "down"

        vpn_uuid = ""
        # Loop through each connection and find the VPN
        for connection in con_list:
            if(connection.startswith(vpn_name)):
                words = connection.replace(vpn_name, "").split()
                if ("vpn" == words[1]):
                    vpn_uuid = words[0]
                    break

        # If vpn is found peform the action
        if(vpn_uuid != ""):
            o,e = self.run_process(["nmcli con " + action + " " + vpn_uuid], False)
            self.info("VPN: " + vpn_name + ", Status: " + action.title())
            if(e):
                return False
        else:
            self.info("The VPN " + vpn_name + " is not found in Network Manager")
        
        return True

    # copy_files_to_remote
    # * Copies the given local file to remote
    # @param local_path - Local path of the file to be copied
    # @param ipaddress - Ip Address/ Hostname of the remote machine
    # @param command - Command to be run in remote machine
    # @param remote_user - User account to login to remtoe machine
    # @return bool

    def copy_files_to_remote(self, local_path, ipaddress, remote_path, remote_user=""):
        is_active = self.is_remote_active(ipaddress)

        if(not is_active):
            self.info("Remote '" + ipaddress + "' is not active, Terminating Process")
            return False
        if(remote_user):
            remote_user = remote_user + "@"
        command = "scp " + local_path + " " + remote_user + ipaddress + ":" + remote_path

        self.info("Copying: " + local_path + " to remote: " + ipaddress)
        o,e = self.run_process([command], False)
        if(e):
            self.info("Issue when Copying file to remote, Please check log")
            self.info("Output: " + self.decode(o))
            self.info("Error: " + self.decode(e))
            return False
        
        return True

    # run_command_in_remote
    # * Runs given command in a remote machine,
    # * have to pass arguments for command inside the command
    # @param ipaddress - Ip Address/ Hostname of the remote machine
    # @param command - Command to be run in remote machine
    # @param remote_user - User account to login to remtoe machine
    # @return bool

    def run_command_in_remote(self, ipaddress, command, remote_user=""):
        self.info("Running command in remote: " + ipaddress)
        is_active = self.is_remote_active(ipaddress)

        if(not is_active):
            self.info("Remote '" + ipaddress + "' is not active, Terminating Process")
            return False
        if(remote_user):
            remote_user = remote_user + "@"
        command = "ssh " + remote_user + ipaddress + " ./" + command
        o,e = self.run_process([command], False)
        if(e):
            self.info("Issue when Running command in remote, Please check log")
            self.info("Output: " + self.decode(o))
            self.info("Error: " + self.decode(e))
            return False
        self.info("Command Executed in remote successfully")
        return True

    # is_remote_active
    # * Checks if the remote machine is active (Accessible)
    # @param remote_address - Ip Address/ Hostname of the remote machine
    # @return bool

    def is_remote_active(self, remote_address):
        self.info("Checking if remote is active for: " + remote_address)
        o,e = self.run_process(["ping -c 4 " + remote_address], False)
        full_output = self.decode(o).split("\n")
        length = len(full_output)

        # Looping through ping output
        for i in range(length - 1, 0, -1):
            output_txt = full_output[i]
            if(output_txt.strip() == ""):
                continue
            if("packet loss" not in output_txt):
                continue
            
            description_found = True
            # If packet loss (last description line) found then split it
            line_split = output_txt.split(",")
            line_length = len(line_split)

            # Loop through description line split
            for i in range(0, line_length):
                word_split = line_split[i]
                if("packet loss" not in word_split):
                    continue

                # Finding packet loss percentage
                percent = word_split.split("%")
                percent = int(percent[0].strip())

                if(percent < 50):
                    return True

        # If the packet loss percentage is greater than 50,
        # then we wont connect
        return False

