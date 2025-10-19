import os
from typing import Dict, Any
from dataclasses import dataclass

try:
    from psnawp_api import PSNAWP
except Exception:
    PSNAWP = None


@dataclass
class TrophySummary:
    bronze: int
    silver: int
    gold: int
    platinum: int
    progress: int | None = None
    level: int | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bronze": self.bronze,
            "silver": self.silver,
            "gold": self.gold,
            "platinum": self.platinum,
            "progress": self.progress,
            "level": self.level,
            "total": self.bronze + self.silver + self.gold + self.platinum,
        }


class PSNClient:
    def __init__(self, npsso: str | None = None):
        self.npsso = npsso or os.environ.get("NPSSO")
        self._psn = None
        self._error_msg = None
        
        if PSNAWP and self.npsso:
            try:
                self._psn = PSNAWP(npsso_cookie=self.npsso)
            except Exception as e:
                self._error_msg = str(e)
                self._psn = None

    @property
    def available(self) -> bool:
        return self._psn is not None

    def get_user_trophies_summary(self, online_id: str) -> TrophySummary:
        if not self.available:
            return self._demo_summary(online_id)

        try:
            user = None
            try:
                user = self._psn.user(online_id=online_id)
            except Exception:
                if hasattr(self._psn, "user"):
                    user = self._psn.user(online_id=online_id)

            if user is None:
                raise RuntimeError("Unable to get PSN user")

            summary = None
            try:
                summary = user.trophy_summary()
            except Exception:
                summary = getattr(user, "trophy_summary", None)

            if summary is None:
                raise RuntimeError("Unable to get trophy summary")

            def _get(obj, key):
                if isinstance(obj, dict):
                    return obj.get(key)
                return getattr(obj, key, None)

            earned_trophies = _get(summary, "earned_trophies")
            if earned_trophies:
                bronze = int(_get(earned_trophies, "bronze") or 0)
                silver = int(_get(earned_trophies, "silver") or 0)
                gold = int(_get(earned_trophies, "gold") or 0)
                platinum = int(_get(earned_trophies, "platinum") or 0)
            else:
                bronze = int(_get(summary, "bronze") or 0)
                silver = int(_get(summary, "silver") or 0)
                gold = int(_get(summary, "gold") or 0)
                platinum = int(_get(summary, "platinum") or 0)
            
            progress = _get(summary, "progress")
            level = _get(summary, "trophy_level") or _get(summary, "level")

            return TrophySummary(
                bronze=bronze, silver=silver, gold=gold, platinum=platinum, progress=progress, level=level
            )
        except Exception:
            return self._demo_summary(online_id)

    @staticmethod
    def _demo_summary(online_id: str) -> TrophySummary:
        return TrophySummary(bronze=120, silver=45, gold=12, platinum=3, progress=78, level=350)
