from dataclasses import asdict, dataclass


@dataclass
class ServiceRequest:
    id: int
    date: str
    municipality: str
    service: str
    area: str
    status: str

    def to_dict(self):
        return asdict(self)

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