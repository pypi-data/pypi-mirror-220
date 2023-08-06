import os, datetime
from . import ProcessUtilities

# Contains device related functions
class DeviceUtilities(ProcessUtilities):

    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = (f"{__class__}".split("'")[1])
        self.get_logger(**kwargs)
        self.debug(f"Initialized: {kwargs['name']}")

    def change_dir_owner(self, dir, user, group):
        command = "chown "  + user + ":" + group + " " + dir
        o,e = self.run_process([command])
        self.check_and_log_errors(e, "Error Change Group for device: ")

    def sticky_file_permission(self, filename, mod_type="g" ,permission="rwx"):
        command = "sudo chmod -R " + mod_type + "+s " + filename
        o,e = self.run_process([command], True)
        self.check_and_log_errors(e, "Error Change Sticky Mode for device: ")
        command = "sudo setfacl -R -d -m " + mod_type + "::" + permission + " " + filename
        o,e = self.run_process([command], True)
        self.check_and_log_errors(e, "Error SetFacl for device: ")

    def change_file_permission_recursive(self, filename, permission="777"):
        command = "chmod -R " + permission + " " + filename
        o,e = self.run_process([command], True)
        self.check_and_log_errors(e, "Error Change Mode for device: ")
    
    def change_file_permission(self, filename, permission="777"):
        command = "chmod " + permission + " " + filename
        o,e = self.run_process([command], True)
        self.check_and_log_errors(e, "Error Change Mode for device: ")

    def check_device_path_in_use(self, device_path):
        o = self.run_process(["lsof -w | grep " + device_path], True)
        return ("".join(str(x) for x in o) != "")
    
    def check_and_unmount_device_path(self, device_path, force_unmount=False):
        self.log("Check and unmount: " + device_path)
        if(force_unmount):
            self.run_process(["umount -rl " + device_path])
            self.log("Device unmounted")
            return True
        in_use = self.check_device_path_in_use(device_path)
        # Check if the Device is not in use
        if(not in_use):
            self.run_process(["umount " + device_path])
            self.log("Device unmounted")
            return True
        self.log("Device in Use, not unmounted")
        return False
        
    def check_and_mount_device_to_path(self, mount_path, device_path, fstype):
        fstype = fstype.lower()
        if(fstype == "ntfs"):
            mount_type = " -t ntfs-3g "
        elif(fstype == "ext4"):
            mount_type = " -t ext4 "
        else:
            mount_type = " "
        command = 'mount "' + device_path + '"' + mount_type + '"' + mount_path + '"'
        o,e = self.run_process([command])
        if(len(e) > 0):
            self.check_and_log_errors(header="Error Mounting Device: ", e=e)
        
        if(fstype == "ext4") or ("lvm" in fstype):
            return True
        return False

    def change_mount_drive_permissions(self, mount_path):
        self.change_dir_owner(mount_path, "sambare", "adm")
        self.print_info_log("Chmod -> " + mount_path)
        self.sticky_file_permission(mount_path, mod_type="g", permission="rwx")
        self.change_file_permission(mount_path, permission="770")

    def get_lvm_physical_volumes(self, skip_vgs=None, skip_lvs=None):
        command = "sudo lvs -o lv_name,lv_path,vg_name,dm_path,devices"
        options = "lv,path,vg,dmpath,devices"
        
        # Run lsblk command and get drive details
        output,error = self.run_process([command])
        output_as_list = self.decode(output).split("\n")

        # Get options and its position from output first line
        option_list = []
        start_index = 0
        end_index = 0
        option_line = output_as_list[0].lower()
        options = options.split(",")
        options_length = len(options)

        # Loop through options to get their start and end points in output
        for key in range(0, options_length - 1):
            end_index = int(option_line.find(options[key + 1])) + 1
            option_list.append({
                "name": options[key],
                "start_index": start_index,
                "end_index": end_index
            })
            start_index = end_index
        
        option_list.append({
            "name": options[options_length - 1],
            "start_index": start_index,
            "end_index": len(option_line)
        })

        output_as_list = output_as_list[1:]
        drive_details_list = {}
        for drive in output_as_list:
            lvm_detail = {}
            for option in option_list:
                lvm_detail[option["name"].strip()] = drive[option["start_index"]: option["end_index"]].strip()

            lvm_detail["skip"] = False
            
            if skip_vgs:
                if(lvm_detail["vg"] in skip_vgs):
                    lvm_detail["skip"] = True
            if skip_lvs:
                if(lvm_detail["lv"] in skip_lvs):
                    lvm_detail["skip"] = True
            		
            device_detail_device = lvm_detail["devices"]
            drive_path = lvm_detail["dmpath"]
            device_detail_device = device_detail_device[:device_detail_device.find("(")]
            
            if(drive_path not in drive_details_list):
                drive_details_list[drive_path] = {
                    "path": lvm_detail["path"],
                    "dmpath": lvm_detail["dmpath"],
                    "lv_name": lvm_detail["lv"],
                    "vg_name": lvm_detail["vg"],
                    "skip"	 : lvm_detail["skip"],
                    "devices": []
                }

            drive_details_list[drive_path]["devices"].append(device_detail_device)

        return drive_details_list

    def get_connected_drives_by_types(self, drive_types=[]):
        drives = {}
        for drive_type in drive_types:
            connected_drives = self.get_connected_drives_by_type(drive_type)
            for key in connected_drives:
                drives[key] = connected_drives[key]
        return drives

    def get_connected_drives_by_type(self, drive_type=None):
        
        # Options for lsblk to drive and parition details
        options = "size,path,kname,label,uuid,type,mountpoint,fstype"
        command = "lsblk -o " + options
        #  + " | grep " + drive_type

        # Run lsblk command and get drive details
        output,error = self.run_process([command])
        output_as_list = self.decode(output).split("\n")

        # Get options and its position from output first line
        option_list = []
        start_index = 0
        end_index = 0
        option_line = output_as_list[0].lower()
        options = options.split(",")
        options_length = len(options)
        # print(output_as_list)

        # Loop through options to get their start and end points in output
        for key in range(0, options_length - 1):
            end_index = int(option_line.find(options[key + 1])) + 1
            option_list.append({
                "name": options[key],
                "start_index": start_index,
                "end_index": end_index
            })
            start_index = end_index
        
        option_list.append({
            "name": options[options_length - 1],
            "start_index": start_index,
            "end_index": len(option_line)
        })
        # print(option_list)
        output_as_list = output_as_list[1:]
        drive_details_list = []
        for drive in output_as_list:
            device_detail = {}
            for option in option_list:
                device_detail[option["name"].strip()] = drive[option["start_index"]: option["end_index"]].strip()
#            device_detail["path"] = "/dev/" + device_detail["kname"]
            if not drive_type:
                drive_details_list.append(device_detail)
            elif(device_detail["type"] == drive_type):
                drive_details_list.append(device_detail)

#        return list({d["path"]:d for d in drive_details_list}.values())
        return {d["path"]:d for d in drive_details_list}


    # https://www.oreilly.com/openbook/samba/book/
    def generate_samba_veto_and_seperate_share_list(self, shared_folder_path):
        
        self.log("generate_samba_veto_and_seperate_share_list: Started")
        # Veto files are files the user donot wish to share with the network
        config_folder_path = os.path.join(shared_folder_path, ".config-share")
        veto_file_path = os.path.join(config_folder_path, ".ignore")
        seperate_share_file_path = os.path.join(config_folder_path, ".share-seperate")
        
        veto_files = "/lost+found/*.config-share*/"
        seperate_share_path_list = []
        if(os.path.exists(veto_file_path)):
            veto_file_list = []
            with open(veto_file_path, "r") as f:
                veto_file_list = f.readlines()
            veto_files += "/".join(veto_file_list).replace("\n", "")
        
        if(os.path.exists(seperate_share_file_path)):
            with open(seperate_share_file_path, "r") as f:
                seperate_share_path_list = f.readlines()

        
        return veto_files, seperate_share_path_list
        

    def generate_samba_config_for_path(self, shared_folder_path):
        label = os.path.basename(shared_folder_path)
        mountpoint = shared_folder_path
        
        veto_files, seperate_share = self. generate_samba_veto_and_seperate_share_list(shared_folder_path=shared_folder_path)
        lines = []
        for share_path in seperate_share:
            share_path = share_path.replace("\n", "")
            share_path = os.path.join(shared_folder_path, share_path)
            share_config = self.generate_samba_config_for_path(share_path)
            lines.extend(share_config)
        
        
        # Samba Configuration for each device
        lines.append("\n")
        lines.append("[" + label + "]")
        lines.append("path=" + mountpoint)
        lines.append("comment = Programmatical")
        lines.append("writable=Yes")
        lines.append("create mask=0777")
        lines.append("directory mask=0777")
        lines.append("force create mode = 0666")
        lines.append("force directory mode = 0777")
        lines.append("follow symlinks = yes")
        lines.append("wide links = yes")
        lines.append("veto files = " + veto_files)
        lines.append("public=no")
        
        return lines
    
    def generate_samba_config_for_device(self, device):
        # Check if Device is mounted, then only share
        mountpoint = device["mountpoint"]

        if(mountpoint == "/") or ("/boot" in mountpoint) or ("swap" in mountpoint.lower()) or (len(mountpoint) < 1):
            return
        
        lines = self.generate_samba_config_for_path(mountpoint)
        return lines
    
    def generate_samba_config_from_connected_devices(self):
        drives = {}
        drives = self.get_connected_drives_by_types(["part", "lvm"])

        generated_mountpoints = []
        lines = ["# This is created programatically on " + datetime.now().strftime("%Y-%m-%d | %H:%M:%s")]

        for key in drives:
            device = drives[key]
            if(device not in generated_mountpoints):
                config = self.generate_samba_config_for_device(device=device)
                generated_mountpoints.append(device["mountpoint"])
            if config:
                lines.extend(config)
        return lines
