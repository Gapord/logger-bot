import aiosqlite
from datetime import datetime
import config as c

class InitDB:
    def __init__(self, servid):
        self.servid = servid
        self.db_path = f"database/sqlite/bases/{self.servid}.db"

    async def initdb(self, color, channel):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(""" 
                CREATE TABLE IF NOT EXISTS servers (
                    serverid INTEGER PRIMARY KEY,
                    color TEXT,
                    channel INTEGER,
                    date TEXT
                )
            """)
            # Попробуйте обновить запись, если она существует
            await db.execute("""
                UPDATE servers
                SET color = ?, channel = ?, date = ?
                WHERE serverid = ?
            """, (color, channel, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.servid))

            # Вставьте новую запись, если обновление ничего не изменило
            await db.execute("""
                INSERT INTO servers (serverid, color, channel, date)
                SELECT ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM servers WHERE serverid = ?)
            """, (self.servid, color, channel, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.servid))
            
            await db.commit()