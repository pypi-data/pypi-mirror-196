from pathlib import Path

__all__ = ["prefix", "description"]

prefix = str(Path(__file__).parent / "ala12")

description = """a peptide with 12 Alanines. ff19SB forcefield. No water"""
