from dataclasses import asdict, dataclass


@dataclass
class HistoricalWeather:
    municipality: str
    date: str
    temperature_mean: float
    precipitation: float
    weather_code: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            municipality=data["municipality"],
            date=data["date"],
            temperature_mean=float(data["temperature_mean"]),
            precipitation=float(data["precipitation"]),
            weather_code=int(data["weather_code"]),
        )