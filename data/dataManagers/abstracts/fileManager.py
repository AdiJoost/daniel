from pathlib import Path
from config.rootPath import getRootPath
from config.configManager import getConfig
from config.applicationConfig.applicationConfigFields import ApplicationConfigFields
from data.dataManagers.enums.overwriteMechanism import OverwriteMechanism

class FileManager():

    CONFIG_FIELD = ApplicationConfigFields.OVERWRITE_MECHANISM.value

    def __init__(self, filename: str, folderpath: str, filetype: str="", baseDataFolder: str = "data") -> None:
        self.filename = filename
        self.folderpath = folderpath
        self.filetype = filetype
        self.baseDataFolder = baseDataFolder
        self.absolutPath = self.getAbsolutPath()
        self._initFile()

    def getAbsolutPath(self) -> Path:
        rootPath = getRootPath()
        return rootPath.joinpath(self.baseDataFolder, self.folderpath, f"{self.filename}.{self.filetype}")
    
    def fileExists(self) -> bool:
        return self.absolutPath.exists()
    
    def _initFile(self) -> None:
        configValue = getConfig(name=self.CONFIG_FIELD)
        overwriteMechanism: OverwriteMechanism = None
        if not configValue:
            overwriteMechanism = OverwriteMechanism.OVERWRITE
        else:
            overwriteMechanism = OverwriteMechanism[configValue]
        if overwriteMechanism == OverwriteMechanism.OVERWRITE:
            self._createFile()
        if overwriteMechanism == OverwriteMechanism.APPEND:
            self._createFileIfNotExists()
        if overwriteMechanism == OverwriteMechanism.ERROR_ON_EXISTS:
            self._validateFileNotExists()

    def _createFile(self) -> None:
        self.absolutPath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.absolutPath, "w", encoding="UTF-8") as file:
            pass

    def _createFileIfNotExists(self) -> None:
        if not self.fileExists():
            self.absolutPath.parent.mkdir(parents=True, exist_ok=True)
            self.absolutPath.touch()
    
    def _validateFileNotExists(self) -> None:
        if self.fileExists():
            raise (f"FileAlreadyExists: {self.absolutPath} already exists. Change application config to OVERWRITE or APPEND if this is intended")
        
