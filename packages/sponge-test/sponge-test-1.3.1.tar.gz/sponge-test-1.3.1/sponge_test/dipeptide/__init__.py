from pathlib import Path

__all__ = ["prefix", "description"]

prefix = str(Path(__file__).parent / "dipeptide")

description = """730 TIP3P water and an terminated ALA dipeptide. Minimization and NPT simulations have been done"""
