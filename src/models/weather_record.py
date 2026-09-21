from dataclasses import asdict, dataclass


@dataclass
class WeatherRecord:
    municipality: str
    time: str
    temperature: float
    humidity: float
    precipitation: float
    weather_code: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            municipality=data["municipality"],
            time=data["time"],
            temperature=float(data["temperature"]),
            humidity=float(data["humidity"]),
            precipitation=float(data["precipitation"]),
            weather_code=int(data["weather_code"]),
        )