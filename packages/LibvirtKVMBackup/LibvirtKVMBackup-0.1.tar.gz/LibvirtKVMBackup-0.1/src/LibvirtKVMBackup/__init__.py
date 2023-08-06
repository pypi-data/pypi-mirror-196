import libvirt
import yaml
import os
import logging
from datetime import datetime
from xml.etree import ElementTree as ET

DomainBackupConfigsPath = "/var/lib/LibvirtKVMBackup/Configs"
LibvirtUri = "qemu:///system"


class backupError(Exception):
    def __init__(self, errormsg):
        self.message = errormsg
        super().__init__(self.message)
        logging.error(self.message)


class restoreError(Exception):
    def __init__(self, errormsg):
        self.message = errormsg
        super().__init__(self.message)


class configManager:
    def __init__(self, config):
        self.config = config

    @property
    def location(self):
        return f"{DomainBackupConfigsPath}/{self.config}"

    def create(self, configdata):
        with open(self.location(), "w") as f:
            yaml.dump(configdata, f)

    def delete(self):
        os.remove(self.location())

    def data(self):
        with open(self.location, "r") as f:
            return yaml.safe_load(f)

    def listBackupsFromPath(self, path):
        backupList = []
        for backup in os.listdir(path):
            backupList.append(backup)
        return backupList

    def listBackups(self):
        backupList = []
        for backup in os.listdir(self.data()['Destination']):
            backupList.append(backup)
        return backupList

    def backupData(self, backup):
        with open(os.path.join(self.data()['Destination'], backup, "Info.yml"), "r") as f:
            return yaml.safe_load(f)
    
    def backupLog(self, backup):
        with open(os.path.join(self.data()['Destination'], backup, "BackupLog.log"), "r") as f:
            return f.read()

    @staticmethod
    def datetimeformat():
        return "%d-%m-%Y_%H-%M"

    @staticmethod
    def list():
        try:
            return os.listdir(DomainBackupConfigsPath)
        except FileNotFoundError:
            return []
 
    @staticmethod
    def listConfigData():
        configData = []
        for config in configManager.list():
            with open(configManager(config=config).location, "r") as f:
                configData.append({
                    'name': config,
                    'data': yaml.safe_load(f)
                })
        return configData


class restore:
    def __init__(self, config, backup, domainName=None, destination=None):
        if domainName == None and destination == None:
            self.config = config
            self.configData = configManager(config).data()
            self.domainName = self.configData['DomainName']
            self.backupConfigData = configManager(config).backupData(backup)
            self.destination = self.configData['Destination']
            logging.basicConfig(level=logging.DEBUG)
        else:
            self.domainName = domainName
            self.destination = destination
            self.backupConfigDataPath = os.path.join(
                self.destination, backup, "Info.yml")
            with open(self.backupConfigDataPath, "r") as f:
                self.backupConfigData = yaml.safe_load(f)
        self.backupLocation = os.path.join(self.destination, backup)
        self.start()

    def start(self):
        # Connect to libvirt
        self._connectLibvirt()
        # Get domain
        self.domain = self.conn.lookupByName(self.domainName)
        # Check if domain is running
        if self._domainStatus() != "Shutoff":
            raise restoreError(
                f"Domain {self.domainName} is not shutdown and AutoShutdown is disabled, aborting restore")
        else:
            # Restore disks
            self.restoreDisks()
            # Restore nvram
            self.restoreNvram()
            # Restore xml
            self.restoreXml()

    def restoreDisks(self):
        for disk in self.backupConfigData['Disks']:
            diskdev = disk['dev']
            diskfilename = disk['filename']
            diskOrigLocation = disk['origLocation']
            diskLocation = os.path.join(self.backupLocation, diskdev)
            try:
                print(f"Restoring disk {diskdev} to {diskOrigLocation}")
                print(f"cp {diskLocation} {diskOrigLocation}")
                os.system(f"cp {diskLocation} {diskOrigLocation}")
                logging.info(f"Successfully restored disk {diskdev}")
            except Exception as e:
                logging.error(f"Failed to restore disk {diskdev}: {e}")

    def restoreNvram(self):
        if self.backupConfigData['Nvram'] != None:
            nvramLocation = os.path.join(self.backupLocation, "nvram")
            nvramOrigLocation = self.backupConfigData['Nvram']
            try:
                print(f"Restoring nvram to {nvramOrigLocation}")
                print(f"cp {nvramLocation} {nvramOrigLocation}")
                os.system(f"cp {nvramLocation} {nvramOrigLocation}")
                logging.info(f"Successfully restored nvram")
            except Exception as e:
                logging.error(f"Failed to restore nvram: {e}")

    def restoreXml(self):
        xmlLocation = os.path.join(self.backupLocation, "DomainXml.xml")
        try:
            print("Restoring xml", xmlLocation)
            with open(xmlLocation, "r") as f:
                xml = f.read()
            self.conn.defineXML(xml)
            logging.info(f"Successfully restored xml")
        except Exception as e:
            raise restoreError(f"Failed to restore xml: {e}")

    def _connectLibvirt(self):
        try:
            self.conn = libvirt.open(LibvirtUri)
        except libvirt.libvirtError as e:
            logging.error(f"Failed to connect to libvirt: {e}")

    def _domainStatus(self):
        state, reason = self.domain.state()
        if state == libvirt.VIR_DOMAIN_NOSTATE:
            dom_state = 'NOSTATE'
        elif state == libvirt.VIR_DOMAIN_RUNNING:
            dom_state = 'Running'
        elif state == libvirt.VIR_DOMAIN_BLOCKED:
            dom_state = 'Blocked'
        elif state == libvirt.VIR_DOMAIN_PAUSED:
            dom_state = 'Paused'
        elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            dom_state = 'Shutdown'
        elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            dom_state = 'Shutoff'
        elif state == libvirt.VIR_DOMAIN_CRASHED:
            dom_state = 'Crashed'
        elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            dom_state = 'Pmsuspended'
        else:
            dom_state = 'unknown'
        return dom_state


class backup:
    def __init__(self, config):

        DomainBackupConfigPath = configManager(config).location
        try:
            with open(DomainBackupConfigPath, "r") as f:
                DomainBackupConfigData = yaml.safe_load(f)
        except FileNotFoundError:
            raise backupError(f"Cannot find config file with name {config}")

        self.dateTime = datetime.now().strftime(configManager.datetimeformat())

        try:
            self.Debug = DomainBackupConfigData['Debug']
            self.DomainName = DomainBackupConfigData['DomainName']
            self.Disks = DomainBackupConfigData['Disks']
            self.BackupDestination = DomainBackupConfigData['Destination']
            self.AutoShutdown = DomainBackupConfigData['AutoShutdown']
        except KeyError as e:
            raise backupError(f"{e} does not exist in config.")
        self.start()

    def start(self):
        """
        - check if destination exists
        - create directory with the date
        - connect to libvirt
        - shut down vm
        - backup xml
        - read vdisk locations
        - backup vdisks
        - backup nvram
        - start domain again if it was started
        """
        # Check backup destination
        if os.path.exists(self.BackupDestination):
            if not os.path.isdir(self.BackupDestination):
                raise backupError(
                    f"Backup destination {self.BackupDestination} isn't a directory")
            else:
                # create backup directory
                self.BackupPath = os.path.join(
                    self.BackupDestination, self.dateTime)
                try:
                    os.mkdir(self.BackupPath)
                except PermissionError:
                    raise backupError(
                        f"Failed to create folder for backup: {self.BackupPath} because of permission issues")

        else:
            raise backupError(
                f"Backup destination {self.BackupDestination} doesn't exist")

        # Start thread to create the backup
        self._createLog()
        self._createBackup()
    def _createLog(self):
        # configure logging
        logging.basicConfig(filename=os.path.join(
            self.BackupPath, "BackupLog.log"), filemode='w', level=logging.DEBUG)

    def _createBackup(self):
        self._connectLibvirt()
        self.domain = self.conn.lookupByName(self.DomainName)
        self.domainXml = self.domain.XMLDesc()
        self.domainXmlTree = ET.fromstring(self.domainXml)
        self.domainOrigState = self._domainStatus()
        # Check if domain is shutoff, otherwise shut it down
        if self.domainOrigState != "Shutoff":
            logging.debug("Domain is not shutoff")
            if self.AutoShutdown:
                logging.info("AutoShutdown is enabled, shutting down domain")
                self._shutdownDomain()
            else:
                raise backupError(
                    "Domain is not shutoff and AutoShutdown is disabled, aborting backup")

        else:
            logging.info("Domain is shutoff, can start backup!")

        # backup domain xml
        self._backupXml()

        # backup disks
        self.domainDisks = self._getDomainDisks()
        for disk in self.domainDisks:
            diskname = disk['dev']
            disklocation = disk['origLocation']
            diskdestination = os.path.join(self.BackupPath, diskname)
            logging.debug(f"Backing up disk {diskname} to {diskdestination}")
            try:
                os.system(f"cp {disklocation} {diskdestination}")
                logging.info(f"Successfully backed up disk {diskname}")
            except Exception as e:
                logging.error(f"Failed to backup disk {diskname}: {e}")

        # backup nvram
        nvramLocation = self._getDomainNvram()
        if nvramLocation != None:
            nvramDestination = os.path.join(self.BackupPath, "nvram")
            logging.debug(f"Backing up nvram to {nvramDestination}")
            try:
                os.system(f"cp {nvramLocation} {nvramDestination}")
                logging.info("Successfully backed up nvram")
            except Exception as e:
                logging.error(f"Failed to backup nvram: {e}")

        # write disk list to file
        with open(os.path.join(self.BackupPath, "Info.yml"), "w") as f:
            data = {'Disks': self.domainDisks, 'Nvram': nvramLocation}
            yaml.dump(data, f)

        # start domain if it was started
        if self.domainOrigState == "Running":
            logging.debug("Domain was running, starting it again")
            try:
                self.domain.create()
                logging.debug("Domain successfully started")
            except libvirt.libvirtError as e:
                logging.error(
                    f"Failed to start domain {self.DomainName}: {e}")

    def _shutdownDomain(self):
        try:
            self.domain.shutdown()
            logging.debug("Domain successfully shutdown")
        except libvirt.libvirtError as e:
            logging.error(f"Failed to shutdown domain {self.DomainName}: {e}")
            raise backupError(
                f"Failed to shutdown domain {self.DomainName}: {e}")

    def _getDomainDisks(self):
        disks = self.domainXmlTree.findall('./devices/disk')
        disklist = []
        for disk in disks:
            disktype = disk.get('type')
            if disktype == "file":
                sourcefile = disk.find('./source').get('file')
                targetdev = disk.find('./target').get('dev')
                if targetdev in self.Disks:
                    disklist.append({
                        'dev': targetdev,
                        'origLocation': sourcefile,
                        'filename': os.path.basename(sourcefile)
                    })
                else:
                    logging.debug(
                        f"Skipping disk {targetdev}, it is not in the list of disks to backup")
        return disklist

    def _getDomainNvram(self):
        nvram_elem = self.domainXmlTree.find('os/nvram')
        if nvram_elem != None:
            return nvram_elem.text
        else:
            return None

    def _connectLibvirt(self):
        try:
            self.conn = libvirt.open(LibvirtUri)
        except libvirt.libvirtError as e:
            logging.error(f"Failed to connect to libvirt: {e}")

    def _backupXml(self):
        domainXmlDestination = os.path.join(
            self.BackupPath, "DomainXml.xml")
        logging.debug(f"domain xml backup destination: {domainXmlDestination}")
        with open(domainXmlDestination, "w") as f:
            f.write(self.domainXml)
            logging.info("Succesfully backed up domain xml configuration")

    def _domainStatus(self):
        state, reason = self.domain.state()
        if state == libvirt.VIR_DOMAIN_NOSTATE:
            dom_state = 'NOSTATE'
        elif state == libvirt.VIR_DOMAIN_RUNNING:
            dom_state = 'Running'
        elif state == libvirt.VIR_DOMAIN_BLOCKED:
            dom_state = 'Blocked'
        elif state == libvirt.VIR_DOMAIN_PAUSED:
            dom_state = 'Paused'
        elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            dom_state = 'Shutdown'
        elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            dom_state = 'Shutoff'
        elif state == libvirt.VIR_DOMAIN_CRASHED:
            dom_state = 'Crashed'
        elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            dom_state = 'Pmsuspended'
        else:
            dom_state = 'unknown'
        return dom_state
