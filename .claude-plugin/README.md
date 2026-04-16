# software-dev-agents

Multi-agent pipeline for professional code development. Validate, test, refactor, and improve code quality with adaptive workflows and confidence scoring.

## 📥 Installation

### Quick Install (Recommended)
```
/plugin install https://github.com/eliezeravihail/software-dev-agents
```

### Or from Marketplace
```
/plugin marketplace add eliezeravihail/software-dev-agents
/plugin install software-dev-agents@eliezeravihail-software-dev-agents
```

---

## 🎯 Usage

After installation, use the `/experts` skill:

```
/experts:security-review               ← Check vulnerabilities
/experts:code-simplify                 ← Improve code quality
/experts:dev-cycle                     ← Full pipeline
/experts:validate-requirements-static  ← Validate code
/experts:test-assumptions              ← Generate tests
/experts:refactor-code-structure       ← Refactor safely
/experts:test-generate-suite           ← Create test suite
```

### Example
```
/experts:security-review
/experts:code-simplify
/experts:dev-cycle
```

---

## 🤖 Agents

| Agent | Role | Model |
|-------|------|-------|
| **refactorer** | Code refactoring + guardrails | Sonnet 4.6 |
| **validator** | Validation + confidence scoring | Sonnet 4.6 |
| **tester** | Testing + coverage | Sonnet 4.6 |

---

## 🔄 Pipeline

```
validate-static → test-assumptions → validate-final → refactor → test-suite
```

Adaptive retry + confidence scoring at each step.

---

## 📚 Knowledge Integration

Integrates with [knowledge-library-agents](https://github.com/eliezeravihail/knowledge-library-agents) for domain-specific guidance during refactoring and validation.

---

## 🔗 Repository

[github.com/eliezeravihail/software-dev-agents](https://github.com/eliezeravihail/software-dev-agents)

---

## 📄 License

MIT
