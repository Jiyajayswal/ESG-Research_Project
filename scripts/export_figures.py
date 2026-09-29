"""Draw a simple left-to-right pipeline diagram and export SVG + PNG.

Edit STEPS to change the boxes. Text stays editable in the SVG output.

Usage:
    python scripts/export_figures.py --out outputs/ --dpi 400
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["svg.fonttype"] = "none"  # keep text as text in SVG

STEPS = [
    ("Source PDF", "#E8F0FE"),
    ("Text extraction", "#E6F4EA"),
    ("Manual review", "#FEF7E0"),
    ("Structured output", "#FCE8E6"),
]


def draw(steps, box_w=2.2, box_h=1.0, gap=0.8):
    width = len(steps) * box_w + (len(steps) - 1) * gap
    fig, ax = plt.subplots(figsize=(width * 0.9, box_h * 2))
    ax.set_xlim(-0.2, width + 0.2)
    ax.set_ylim(-0.2, box_h + 0.2)
    ax.axis("off")

    for i, (label, color) in enumerate(steps):
        x = i * (box_w + gap)
        ax.add_patch(FancyBboxPatch(
            (x, 0), box_w, box_h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=color, edgecolor="#5F6368", linewidth=1.2,
        ))
        ax.text(x + box_w / 2, box_h / 2, label, ha="center", va="center",
                fontsize=11, color="#202124")
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch(
                (x + box_w + 0.05, box_h / 2), (x + box_w + gap - 0.05, box_h / 2),
                arrowstyle="-|>", mutation_scale=14, color="#5F6368", linewidth=1.2,
            ))
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="outputs/", help="Output folder")
    parser.add_argument("--name", default="pipeline", help="Base file name")
    parser.add_argument("--dpi", type=int, default=400, help="PNG resolution")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    fig = draw(STEPS)
    fig.savefig(out / f"{args.name}.svg", bbox_inches="tight", transparent=True)
    fig.savefig(out / f"{args.name}.png", bbox_inches="tight", dpi=args.dpi, facecolor="white")
    print(f"Saved {out / args.name}.svg and .png")


if __name__ == "__main__":
    main()
