"""One plotnine figure with the active aesth palette."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from plotnine import aes, geom_point, geom_smooth, ggplot, labs, facet_wrap
from plotnine.data import anscombe_quartet

import aesth

aesth.use("arden")
tokens = aesth.palette()

plot = (
    ggplot(anscombe_quartet, aes("x", "y"))
    + geom_point(color=tokens.accent, size=2.2)
    + geom_smooth(method="lm", se=False, color=tokens.ink, size=0.9)
    + facet_wrap("dataset")
    + labs(title="Anscombe's quartet")
    + aesth.theme_aesth(figure_size=(10.5, 7.0))
)

out = Path(__file__).with_name("anscombe.png")
plot.save(out, dpi=220, verbose=False)
print(out)
