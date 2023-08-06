from dataclasses import dataclass
import yaml

@dataclass
class DefectReportConfig:
    def __init__(self):
        self.DefectDataInfo = self.read_config(r"C:\gitvob_reliability\repo\mr-uwf-reliability\system\apps\ExcelUtility\DefectDataExtractorConfig.yaml")

    def read_config(self, filePath):
        with open(filePath, 'r') as file:
            self.DefectDataInfo = yaml.safe_load(file)
        return self.DefectDataInfo

    def fetch_group_name(self, teamName):
        groupName = ""
        if teamName:
            groupName = [groupKey for groupKey, groupValues in self.DefectDataInfo['groupnames'].items() for team in
                     groupValues if team == teamName]
            return groupName[0]
        else:
            return groupName

