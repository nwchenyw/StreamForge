# StreamForge Code Signing Policy

Free code signing provided by [SignPath.io](https://signpath.io/), certificate by [SignPath Foundation](https://signpath.org/).

## 📌 Project Overview
- **Project Name:** StreamForge
- **Repository:** [https://github.com/nwchenyw/StreamForge](https://github.com/nwchenyw/StreamForge)
- **License:** MIT License (OSI-Approved)
- **Releases & Downloads:** [https://github.com/nwchenyw/StreamForge/releases](https://github.com/nwchenyw/StreamForge/releases)

---

## 👥 Roles and Responsibilities
- **Project Owner & Maintainer:** [@nwchenyw](https://github.com/nwchenyw)
- **Release Manager & Approver:** [@nwchenyw](https://github.com/nwchenyw)

---

## 🔒 Security and Signing Pipeline
- Official Windows binaries (`StreamForge.exe` and `StreamForge-Setup-*.exe`) are built via GitHub Actions CI/CD workflows from tagged releases on the `main` branch.
- Automated code signing is executed via the trusted SignPath.io GitHub Action integration.
- Artifacts are verified against SHA-256 checksums and published directly to GitHub Releases.
- Signing keys and certificates are securely managed by the SignPath Foundation HSM and are never exposed in the source code or build logs.
