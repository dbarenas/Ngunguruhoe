import aiosqlite
from Ngunguruhoe.domain.models.alert import Alert
from Ngunguruhoe.domain.ports.alert_port import AlertPort
from datetime import datetime

class SQLiteAlertRepository(AlertPort):
    def __init__(self, db_path="alerts.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    timestamp TEXT,
                    symbol TEXT,
                    action TEXT,
                    confidence REAL
                )
            """)
            await db.commit()

    async def save_alert(self, alert: Alert):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT INTO alerts VALUES (?, ?, ?, ?)", (
                alert.timestamp.isoformat(),
                alert.symbol,
                alert.action,
                alert.confidence
            ))
            await db.commit()

    async def get_latest_alert(self) -> Alert | None:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 1") as cursor:
                row = await cursor.fetchone()
                if row:
                    return Alert(datetime.fromisoformat(row[0]), row[1], row[2], row[3])
                return None
