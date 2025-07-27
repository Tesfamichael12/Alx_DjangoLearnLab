# Security Policy

## Supported Versions

We recommend always using the latest stable version of our project to ensure that you receive the latest security updates. However, the following versions are currently supported:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| 0.9.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please report it as soon as possible. We take all security vulnerabilities seriously and will address them promptly.

### How to Report

- **Email:** Please send a detailed description of the vulnerability, including steps to reproduce it, to [security@example.com](mailto:security@example.com).
- **PGP Key:** If you prefer to encrypt your communication, please use our PGP key, which is available at `https://example.com/pgp-key`.

## Security Best Practices Implemented

### 1. Secure Django Settings
- `DEBUG` is set to `False` in production.
- `ALLOWED_HOSTS` is configured to restrict access to specific domains/IPs.
- Cookies (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`) are set to be sent over HTTPS only.

### 2. Cross-Site Request Forgery (CSRF) Protection
- All forms are protected with CSRF tokens by including `{% csrf_token %}` in templates.

### 3. Cross-Site Scripting (XSS) Protection
- The `SECURE_BROWSER_XSS_FILTER` is enabled to protect against XSS attacks.
- `Content Security Policy (CSP)` headers are set up to control which resources the application can load.

### 4. SQL Injection Protection
- The Django ORM is used to interact with the database, avoiding direct SQL queries and preventing SQL injection.

## Security Testing

We regularly test our application for vulnerabilities, including:
- Manual testing of form inputs to check for XSS and CSRF vulnerabilities.
- Automated tools to scan for SQL injection points and other security issues.

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top Ten Security Risks](https://owasp.org/www-project-top-ten/)

## The above has been compiled with the help of Chatgpt IA

# Security Configuration for LibraryProject

## HTTPS and Secure Settings

- **SECURE_SSL_REDIRECT**: Redirects all HTTP requests to HTTPS.
- **SECURE_HSTS_SECONDS**: Configured to 1 year to enforce HTTPS.
- **SECURE_HSTS_INCLUDE_SUBDOMAINS**: Ensures that all subdomains are included in the HSTS policy.
- **SECURE_HSTS_PRELOAD**: Allows for HSTS preloading by browsers.
- **SESSION_COOKIE_SECURE**: Ensures session cookies are only transmitted over HTTPS.
- **CSRF_COOKIE_SECURE**: Ensures CSRF cookies are only transmitted over HTTPS.
- **X_FRAME_OPTIONS**: Set to DENY to prevent clickjacking.
- **SECURE_CONTENT_TYPE_NOSNIFF**: Prevents MIME-type sniffing.
- **SECURE_BROWSER_XSS_FILTER**: Enables XSS filtering in browsers.

## Deployment Configuration

- SSL/TLS certificates obtained from Let's Encrypt.
- Nginx configured to serve the site over HTTPS with strict security headers.