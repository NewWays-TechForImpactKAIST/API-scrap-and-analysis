from dataclasses import dataclass


@dataclass
class Councilor:
    sdName: str
    sggName: str
    wiwName: str
    name: str
    gender: str
    birthday: str
    age: int
    jobId: int
    job: str
    eduId: int
    edu: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            sdName=data.get("sdName"),
            sggName=data.get("sggName"),
            wiwName=data.get("wiwName"),
            name=data.get("name"),
            gender=data.get("gender"),
            birthday=data.get("birthday"),
            age=data.get("age"),
            jobId=data.get("jobId"),
            job=data.get("job"),
            eduId=data.get("eduId"),
            edu=data.get("edu"),
        )
    
    def to_dict(self):
        return {
            "sdName": self.sdName,
            "sggName": self.sggName,
            "wiwName": self.wiwName,
            "name": self.name,
            "gender": self.gender,
            "birthday": self.birthday,
            "age": self.age,
            "jobId": self.jobId,
            "job": self.job,
            "eduId": self.eduId,
            "edu": self.edu,
        }