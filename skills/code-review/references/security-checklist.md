# Security Audit Checklist

## General Security Principles
- [ ] Input validation and sanitization
- [ ] Authentication and authorization checks
- [ ] Secure communication (HTTPS/TLS)
- [ ] Proper error handling (no sensitive data leaks)
- [ ] Secure defaults and fail-safe behavior

## Common Vulnerabilities

### Injection Attacks
- [ ] SQL injection prevention (parameterized queries)
- [ ] Command injection prevention (avoid shell execution with user input)
- [ ] XSS (Cross-Site Scripting) prevention
- [ ] CSRF (Cross-Site Request Forgery) protection

### Authentication & Authorization
- [ ] Strong password policies
- [ ] Proper session management
- [ ] Secure token handling (JWT, API keys)
- [ ] Role-based access control (RBAC)

### Data Protection
- [ ] Encryption at rest and in transit
- [ ] Secure storage of sensitive data
- [ ] Proper handling of PII (Personal Identifiable Information)
- [ ] Data minimization principles

### Dependencies & Supply Chain
- [ ] Regular dependency updates
- [ ] Vulnerability scanning (npm audit, pip-audit)
- [ ] Only trusted dependencies
- [ ] License compliance

### Code Quality Security
- [ ] Avoid hardcoded secrets
- [ ] Secure random number generation
- [ ] Proper cryptographic practices
- [ ] Secure file operations

## Language-Specific Checks

### Python
- [ ] Use of `eval()` or `exec()` with untrusted input
- [ ] Pickle usage with untrusted data
- [ ] Unsafe YAML/JSON parsing
- [ ] Path traversal vulnerabilities

### JavaScript/Node.js
- [ ] Prototype pollution
- [ ] Insecure deserialization
- [ ] RegExp DoS (ReDoS)
- [ ] Unsafe eval usage

### Go
- [ ] SQL injection in database queries
- [ ] Path traversal in file operations
- [ ] Unsafe pointer usage
- [ ] Race conditions in concurrent code

## Automated Tool Integration
- **Bandit** (Python): `bandit -r .`
- **ESLint Security** (JS/TS): `npx eslint --ext .js,.ts .`
- **Gosec** (Go): `gosec ./...`
- **Cargo Audit** (Rust): `cargo audit`

## Severity Levels
- **Critical:** Immediate fix required (remote code execution, data breaches)
- **High:** Fix within 1 week (privilege escalation, data leaks)
- **Medium:** Fix within 1 month (information disclosure)
- **Low:** Address when convenient (minor issues, best practices)

## Remediation Guidelines
1. **Immediate Actions:** Block deployment, notify security team
2. **Short-term:** Implement fixes, add monitoring
3. **Long-term:** Code reviews, security training, automated scanning

## Reporting
- Document all findings with severity and impact
- Provide actionable remediation steps
- Track fixes and verify resolution
- Maintain security metrics and trends