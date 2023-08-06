from dataclasses import dataclass, field

@dataclass
class Result():
    links: list[str] = field(default_factory=list)
    status: str = ""
    time_in_s: float = 0