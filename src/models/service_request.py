from dataclasses import asdict, dataclass
from datetime import date


@dataclass
class ServiceRequest:
    id: int
    date: date
    municipality: str
    service: str
    area: str
    status: str

    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = date.fromisoformat(self.date)

    def to_dict(self):
        data = asdict(self)
        data["date"] = self.date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data["id"]),
            date=data["date"],
            municipality=data["municipality"],
            service=data["service"],
            area=data["area"],
            status=data["status"],
        )