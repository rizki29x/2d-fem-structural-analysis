# 2D Structural Analysis Calculator – FEM with Python

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A desktop application developed as part of my undergraduate thesis (Mechanical Engineering, University of Riau, 2024). This tool performs **2D structural analysis** using the **Finite Element Method (FEM)** for beams, trusses, frames, and grid. Unlike previous versions that only supported single loads, this application can handle **multiple loads simultaneously** (point loads, distributed loads, moments).

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

## 🎯 Motivation

Commercial structural analysis software (e.g., ANSYS, Abaqus, SAP2000) is expensive and often requires high-end hardware. Many students cannot afford them or resort to illegal versions. Even free/open-source alternatives (e.g., CalculiX) still have a steep learning curve.

This application aims to provide a **simple, accessible, and educational** tool for students to learn FEM and analyze 2D structures without powerful computers.

## 🖥️ Requirements

- Python 3.8 or higher
- Libraries: `numpy`, `pillow`, `tkinter` (built-in)

Install dependencies:
```bash
pip install numpy pillow
