from pathlib import Path

__all__ = ["prefix", "description"]

prefix = str(Path(__file__).parent / "water")

description = """2449 TIP3P water (7347 atoms) No minimization or NPT simulations done"""
