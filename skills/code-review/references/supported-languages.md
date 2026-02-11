# Supported Languages and Tools

## Python
- **Linting:** pylint, flake8, black
- **Security:** bandit, safety
- **Performance:** cProfile, memory_profiler
- **Installation:**
  ```bash
  pip install pylint flake8 black bandit safety
  ```

## JavaScript/TypeScript
- **Linting:** eslint, prettier
- **Security:** eslint-plugin-security, npm audit
- **Performance:** lighthouse, webpack-bundle-analyzer
- **Installation:**
  ```bash
  npm install -g eslint prettier eslint-plugin-security
  ```

## Go
- **Linting:** golint, gofmt, go vet
- **Security:** gosec
- **Performance:** pprof, go-torch
- **Installation:**
  ```bash
  go install golang.org/x/lint/golint@latest
  go install github.com/securecodewarrior/gosec/v2/cmd/gosec@latest
  ```

## Rust
- **Linting:** clippy, rustfmt
- **Security:** cargo-audit
- **Performance:** cargo-flamegraph
- **Installation:**
  ```bash
  rustup component add clippy rustfmt
  cargo install cargo-audit
  ```

## Java
- **Linting:** checkstyle, spotbugs
- **Security:** findsecbugs
- **Performance:** jprofiler, visualvm
- **Installation:**
  ```bash
  # Via Maven/Gradle dependencies
  ```

## C/C++
- **Linting:** cppcheck, clang-tidy
- **Security:** flawfinder
- **Performance:** valgrind, gprof
- **Installation:**
  ```bash
  sudo apt install cppcheck clang-tidy flawfinder valgrind
  ```

## Configuration Files

### Python
Create `setup.cfg` or `pyproject.toml`:
```ini
[flake8]
max-line-length = 88
ignore = E203,W503
```

### JavaScript
Create `.eslintrc.json`:
```json
{
  "extends": ["eslint:recommended", "plugin:security/recommended"],
  "plugins": ["security"]
}
```

### General
Tools will use default configurations if no config files are found. Customize as needed for your project standards.