# wpipe LTS Policy

**Version**: 2.0.0
**Release Date**: April 13, 2026
**LTS End Date**: April 13, 2031 (5 years)

---

## Overview

wpipe 2.0.0 is designated as a **Long-Term Support (LTS)** release. This means it will receive maintenance updates, security patches, and critical bug fixes for a period of **5 years** from the release date.

This policy ensures that users running wpipe in production environments can rely on a stable, secure, and well-maintained library without forced migration to newer versions.

---

## Support Timeline

| Date | Event |
|------|-------|
| April 13, 2026 | wpipe 2.0.0 LTS released |
| April 13, 2028 | Mid-life review - assess remaining issues |
| January 13, 2031 | End of new feature backports |
| April 13, 2031 | End of LTS support (EOL) |

---

## What Gets Backported

### ✅ Included in LTS Updates

1. **Security Fixes**
   - Vulnerability patches in wpipe code
   - Critical security updates in dependencies
   - CVE remediations

2. **Critical Bug Fixes**
   - Data corruption issues
   - Pipeline execution failures
   - Memory leaks
   - Race conditions

3. **Compatibility Updates**
   - Python version support (within 3.9-3.13 range)
   - Critical dependency updates that break compatibility
   - OS-level compatibility fixes

4. **Documentation Fixes**
   - Errata corrections
   - Security documentation updates

### ❌ NOT Included in LTS Updates

1. **New Features**
   - Phase 3 features (distributed execution, advanced scheduling, etc.)
   - New decorators, executors, or integrations
   - Dashboard improvements

2. **Performance Optimizations**
   - General speedups (unless fixing a regression)
   - Algorithm improvements
   - Memory optimizations (unless fixing a leak)

3. **API Changes**
   - Breaking changes to existing APIs
   - New convenience methods
   - Deprecation of existing APIs

4. **Dependency Upgrades** (non-security)
   - Upgrading to new major versions of dependencies
   - Adding new optional dependencies

---

## Versioning Policy

LTS updates follow **semantic versioning** with patch-level increments:

- `2.0.1`, `2.0.2`, etc. - Patch releases for LTS fixes
- Minor and major version bumps (`2.1.0`, `3.0.0`) are NOT part of LTS
- LTS users can safely upgrade within the `2.0.x` series

### Release Cadence

- **Security fixes**: Released within 30 days of disclosure
- **Critical bugs**: Released within 60 days of confirmation
- **Other fixes**: Batched and released quarterly

---

## Python Version Support

LTS guarantees compatibility with:

- **Python 3.9** (minimum)
- **Python 3.10**
- **Python 3.11**
- **Python 3.12**
- **Python 3.13** (maximum tested)

If any of these Python versions receive end-of-life from the Python Software Foundation during the LTS period, wpipe LTS will continue to work on those versions but may not receive new compatibility fixes.

---

## Dependency Policy

### Pinned for LTS

The following dependencies are pinned for the LTS period to ensure stability:

| Dependency | Minimum Version | Notes |
|------------|----------------|-------|
| requests | >=2.31.0 | Core HTTP client |
| loguru | >=0.7.0 | Logging |
| pandas | >=2.0.0 | Data processing |
| pyyaml | >=6.0.1 | YAML configuration |
| tqdm | >=4.66.0 | Progress bars |
| rich | >=13.7.0 | Terminal output |
| pydantic | >=2.0.0 | Type validation |
| fastapi | >=0.100.0 | Dashboard API |
| uvicorn | >=0.23.0 | Dashboard server |
| wsqlite | >=0.1.0 | SQLite wrapper |

### Security Exception

If a critical vulnerability is discovered in any dependency, wpipe LTS may:
1. Bump the minimum version to a patched release
2. Document the security advisory in release notes
3. Provide migration guidance if API changes occur

---

## Support Channels

### Free Support

- **GitHub Issues**: Bug reports and security vulnerabilities
- **GitHub Discussions**: Questions and community support
- **Documentation**: https://wpipe.readthedocs.io/

### Priority Support

For enterprise users requiring priority support, contact:

- **Email**: wisrovi.rodriguez@gmail.com
- **GitHub Sponsors**: https://github.com/sponsors/wisrovi

---

## Security Policy

### Reporting a Vulnerability

1. **DO NOT** open a public issue for security vulnerabilities
2. Email the maintainer directly: wisrovi.rodriguez@gmail.com
3. Include a detailed description of the vulnerability
4. Allow 7 days for a response before following up

### Response Timeline

- **Acknowledgment**: Within 7 days
- **Assessment**: Within 14 days
- **Fix Released**: Within 30 days for critical issues
- **Public Disclosure**: After fix is released and users have had time to upgrade

### CVE Process

If a CVE is assigned:
1. Coordinate with MITRE/CVE assignment
2. Release patched version
3. Publish security advisory
4. Notify users via GitHub releases and security advisories

---

## Migration from LTS

When LTS ends (April 2031), users should:

1. **Assess Changes**: Review changelog between 2.0.0 and current version
2. **Test Thoroughly**: Run full test suite against newer version
3. **Update Code**: Address any deprecation warnings
4. **Migrate Gradually**: Use feature flags if needed

### Breaking Change Policy

- LTS **will not** introduce breaking changes within the 2.0.x series
- Major version upgrades (e.g., 3.0.0) may have breaking changes
- Deprecation warnings will be provided one LTS cycle before removal

---

## End of Life (EOL)

After April 13, 2031:

- No more security patches
- No more bug fixes
- No more compatibility updates
- Repository will remain public for historical reference
- Users strongly encouraged to upgrade to a newer supported version

### EOL Notice

- **6 months before EOL** (October 2030): Public announcement
- **3 months before EOL** (January 2031): Reminder in release notes
- **At EOL** (April 2031): Final notice in README and docs

---

## Acknowledgments

This LTS policy is inspired by:
- Python's own release cycle policy
- Ubuntu LTS model
- Node.js LTS guidelines
- Django's supported versions policy

---

**Policy Version**: 1.0
**Last Updated**: April 13, 2026
**Next Review**: April 13, 2028 (mid-life review)
