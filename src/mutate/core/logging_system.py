# core/logging_system.py

import json
from utils.timing import TimeStamp

class Logger:
    """
    Multi-channel logging system with timestamps and export support.
    """

    def __init__(self):
        self.entries = []
        self.sim_time = 0

    def set_sim_time(self, t):
        self.sim_time = t

    def log(self, category, message, creature=None, data=None):
        """
        category: string (e.g., "CREATURE_LIFE", "DEV_ACTION", "FLAG")
        message: short description
        creature: optional Creature instance
        data: optional dict with extra info
        """

        entry = {
            "sim_time": self.sim_time,
            "real_time": TimeStamp.format_real(TimeStamp.real_time()),
            "category": category,
            "message": message,
            "creature_id": creature.id if creature else None,
            "creature_species": creature.species.name if creature else None,
            "data": data or {}
        }

        self.entries.append(entry)

    # ------------------------------------------------------------
    # Export
    # ------------------------------------------------------------

    def export_json(self, path):
        with open(path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def export_text(self, path):
        with open(path, "w") as f:
            for e in self.entries:
                line = (
                    f"[{e['real_time']}] "
                    f"(sim {e['sim_time']}) "
                    f"[{e['category']}] "
                    f"{e['message']}"
                )
                if e["creature_id"] is not None:
                    line += f" | Creature {e['creature_id']} ({e['creature_species']})"
                if e["data"]:
                    line += f" | Data: {e['data']}"
                f.write(line + "\n")
