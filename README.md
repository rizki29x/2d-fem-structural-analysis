# 2D Structural Analysis Calculator – FEM with Python

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A desktop application developed as part of my undergraduate thesis (Mechanical Engineering, University of Riau, 2024). This tool performs **2D structural analysis** using the **Finite Element Method (FEM)** for beams, trusses, frames, and grid.

## ✨ Features

- ✅ **Multiple load types** – point load, uniformly distributed load (UDL), moment
- ✅ **Multiple loads** – combine several loads on the same structure
- ✅ **Structure types** – Beam, Truss, Frame (2D)
- ✅ **Outputs**:
  - Nodal displacements
  - Reaction forces
  - Element stresses/forces
  - **Free-body diagrams** before and after loading
- ✅ **Lightweight** – runs on low-spec laptops (no GPU required)
- ✅ **Pure Python** – easy to modify and distribute

## 🖥️ Requirements

- Python 3.8 or higher
- Libraries: `numpy`, `pillow`, `tkinter` (built-in)

Install dependencies:
```bash
pip install numpy pillow
