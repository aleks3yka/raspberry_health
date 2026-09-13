from pathlib import Path
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from raspberry_health.database import Measurement

thermal_zone_list = ["x86_pkg_temp", "cpu-thermal", "cpu_thermal"]

def detect_thermalzone() -> Path:
    for zone in Path("/sys/class/thermal").glob("thermal_zone*"):
        type = (zone / "type").read_text().strip()
        if type in thermal_zone_list:
            return zone/"temp"
    raise RuntimeError("your system doesn't supported")

def read_temp(path: Path) -> float:
    data = path.read_text().strip()
    data = float(data)
    return data / 1000

class Temp_reader:
    device: Path

    def __init__(self):
        self.device = detect_thermalzone()

    def get_temp(self):
        return read_temp(self.device)

async def add_measurement(session_maker: async_sessionmaker[AsyncSession], reader: Temp_reader) -> None:
    temp = reader.get_temp()
    new_row = Measurement(temperature=temp, source="cpu", date=datetime.today())
    async with session_maker() as session:
        session.add(new_row)
        await session.commit()
