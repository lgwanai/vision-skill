# Offline Dependencies

Cross-platform offline Python dependencies for vision-skill.

## Directory Structure

```
offline-deps/
├── common/          # Pure Python wheels (cross-platform)
├── macos/           # macOS-specific binary wheels (cp310-cp313)
└── windows/         # Windows-specific binary wheels (win_amd64, win32)
```

## Supported Platforms

| Platform | Architectures | Python Versions |
|----------|--------------|-----------------|
| macOS | universal2 | 3.10, 3.11, 3.12, 3.13 |
| Windows | x64, x86 | 3.10, 3.11, 3.12, 3.13 |

## Dependencies

| Package | Version | Type |
|---------|---------|------|
| requests | 2.34.2 | Pure Python |
| python-dotenv | 1.2.2 | Pure Python |
| cos-python-sdk-v5 | 1.9.44 | Pure Python |
| certifi | 2026.5.20 | Pure Python |
| charset_normalizer | 3.4.7 | Platform binary + Pure Python fallback |
| idna | 3.18 | Pure Python |
| urllib3 | 2.7.0 | Pure Python |
| xmltodict | 1.0.4 | Pure Python |
| six | 1.17.0 | Pure Python |
| crcmod | 1.7 | Source (needs C++ compiler) |
| pycryptodome | 3.23.0 | Platform binary (abi3) |

## Offline Installation

### macOS
```bash
pip install --no-index \
  --find-links ./offline-deps/common \
  --find-links ./offline-deps/macos \
  -r requirements.txt
```

### Windows
```bash
pip install --no-index \
  --find-links ./offline-deps/common \
  --find-links ./offline-deps/windows \
  -r requirements.txt
```

> **Note for Windows users**: `crcmod` is provided as source tarball (.tar.gz) and requires a C++ compiler (MSVC) to build. If you encounter build errors, install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
