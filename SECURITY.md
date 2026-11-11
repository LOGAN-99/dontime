# Security policy

## Reporting a vulnerability

Please do not publish exploitable details in a public issue. Contact the repository owner privately through the GitHub profile or repository owner contact channel, and include the affected URL or file, relevant version/commit, reproducible steps, and impact. Remove personal data and secrets from any proof-of-concept.

Do not access, modify, or disclose other users' data while investigating. Allow reasonable time for triage and remediation before public disclosure.

## Current controls and known limitations

- The deployment workflow checks the SSH host key fingerprint, stages candidate files, creates backups, and validates deployed files.
- Security headers are configured in `security-headers.fragment`.
- Content Security Policy is currently delivered as **Report-Only**, not enforcement. Do not describe the site as CSP-protected until enforcement is deliberately enabled and tested.
- Static checks are not a substitute for a penetration test, runtime verification, secret-history review, or server-side configuration review.
- Deployment credentials should be least-privileged and rotated if exposure is suspected. Never commit credentials, private keys, tokens, or production data.
