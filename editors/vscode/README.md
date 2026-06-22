# 🚀 WPipe VS Code Tools

[![Version](https://img.shields.io/visual-studio-marketplace/v/wpipe.wpipe-vscode?style=flat-square&color=blue)](https://marketplace.visualstudio.com/items?itemName=wpipe.wpipe-vscode)
[![Author](https://img.shields.io/badge/Author-wisrovi-orange?style=flat-square)](https://github.com/wisrovi)
[![License](https://img.shields.io/github/license/wisrovi/wpipe?style=flat-square&color=green)](https://github.com/wisrovi/wpipe/blob/main/LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-William_Rodriguez-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/wisrovi/)

<img width="1682" height="943" alt="image" src="https://github.com/user-attachments/assets/9618bcca-4253-43b1-a483-7941a1130edf" />

**The Swiss Army Knife for Pipeline Orchestration with WPipe.**

Elevate your Python data engineering with intelligent tools designed to maximize speed, clarity, and resilience. This extension provides a deep, seamless integration of the **WPipe** engine directly into your favorite editor, turning complex orchestration into a visual and intuitive experience.

---

## 💎 Why WPipe Tools?

Traditional pipeline development can be opaque and error-prone. **WPipe Tools** changes the game by giving you visual superpowers and intelligent automation.

### 📊 Real-Time DAG Visualization
Stop guessing how your data flows. Watch your architecture come to life as you write code.
- **Instant Insights:** Generate high-fidelity Directed Acyclic Graphs (DAG) from your `.py` and `.yaml` configurations.
- **Live Feedback:** The visualization panel refreshes instantly on save, helping you catch logic errors before they hit production.
- **Interactive Exploration:** Zoom, pan, and navigate through complex architectures with professional-grade controls.

### 🔍 Step Registry Explorer
Master your ecosystem of reusable components.
- **Centralized Hub:** A dedicated sidebar view maps every `@step` across your entire workspace.
- **Hierarchical Categorization:** Official library and community plugins are organized dynamically using folders based on `category` and subcategories (`subcategory1`, `subcategory2`, `subcategory3`). Steps without defined categories are neatly grouped under a virtual "General" folder to keep your root view clean.
- **Precision Navigation:** Click any step to teleport directly to its implementation.
- **One-Click Testing:** Run and validate individual steps in isolation without launching the full pipeline.

### 🌐 Cloud Catalog Integration
Join a global community of data engineers.
- **Always Updated:** The extension automatically fetches the latest official and community-contributed steps from the cloud.
- **Plug & Play:** Find the perfect component, click to import, and stay focused on your core logic.

### 🧠 Intelligent snippets (The "Pro" Way)
Don't just write code—write *excellent* code.
- **`wpstep` / `wpstepadv`**: Create everything from simple functions to robust classes with built-in retries and timeouts.
- **`wppipe` / `wppipeadv`**: Scaffold production-ready pipelines with metric tracking and persistence in seconds.
- **Flow Control**: Rapidly insert `Parallel`, `Condition`, `For`, and `Background` blocks with automatic imports.

### 🛡️ World-Class YAML Validation
Safety first. Eliminate configuration errors before they happen.
- **Smart Autocomplete:** Intelligent schema-aware suggestions for your `*.wpipe.yaml` files.
- **Zero-Error Syntax:** Real-time validation ensures your YAML is always clean and compatible.

---

## 🚀 Getting Started

1. **Install:** Search for `WPipe Tools` in the VS Code Marketplace or press `Ctrl+P` and type `ext install wpipe.wpipe-vscode`.
2. **Activate:** Open any Python (`.py`) or WPipe YAML (`.yaml`) file.
3. **Visualize:** Open the Command Palette (`Ctrl+Shift+P`) and run `WPipe: Preview Pipeline DAG`.

---

## 🛠️ Key Commands

| Command | Action |
|---------|--------|
| `WPipe: Preview Pipeline DAG` | Open the interactive graph visualizer. |
| `WPipe: Open Web Dashboard` | Launch the real-time monitoring dashboard. |
| `WPipe: Search & Import Steps` | Browse the global component library. |
| `WPipe: Show Cheat Sheet / Help` | Instant access to the pro-tips guide. |

---

## 📄 License

MIT License - Crafted with ❤️ by **William Rodriguez** (wisrovi).

---

**Built for engineers who demand excellence in data orchestration.**
[Visit the official WPipe repository](https://github.com/wisrovi/wpipe)
