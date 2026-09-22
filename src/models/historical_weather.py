from dataclasses import asdict, dataclass
from datetime import date


@dataclass
class HistoricalWeather:
    municipality: str
    date: date
    temperature_mean: float
    precipitation: float
    weather_code: int

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
            municipality=data["municipality"],
            date=data["date"],
            temperature_mean=float(data["temperature_mean"]),
            precipitation=float(data["precipitation"]),
            weather_code=int(data["weather_code"]),
        )