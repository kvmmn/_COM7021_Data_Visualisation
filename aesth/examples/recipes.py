"""One figure that uses the wrapper the way a report would.

Toy cities only.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from plotnine import aes, ggplot, labs

import aesth

HOURS = list(range(8, 16))
LEEDS = [42, 48, 55, 61, 58, 63, 70, 66]
YORK = [30, 33, 36, 40, 39, 44, 47, 45]

frame = pd.DataFrame(
    {
        "hour": HOURS + HOURS,
        "demand": LEEDS + YORK,
        "city": ["Leeds"] * len(HOURS) + ["York"] * len(HOURS),
    }
)

aesth.use("carbon")
plot = (
    ggplot(frame, aes("hour", "demand", color="city"))
    + aesth.line()
    + labs(title="Mean demand by city", x="Hour", y="Passengers")
    + aesth.dress(colour=True, claim="Leeds", levels=["Leeds", "York"])
)

out = ROOT / "studies" / "recipe_demand.png"
aesth.save(plot, out)
print(out)
