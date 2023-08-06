"""A simple Let's Encrypt interface (via `acme-tiny`)."""

import pathlib
import subprocess

import acme_tiny


def generate_cert(domain, cert_dir="certs"):
    """Generate a TLS certificate signed by Let's Encrypt for given domain."""
    cert_dir = pathlib.Path(cert_dir) / domain
    cert_dir.mkdir(exist_ok=True)
    account_key = cert_dir / "account.key"
    if not account_key.exists():
        with account_key.open("w") as fp:
            subprocess.call(["openssl", "genrsa", "4096"], stdout=fp)
    private_key = cert_dir / "domain.key"
    if not private_key.exists():
        with private_key.open("w") as fp:
            subprocess.call(["openssl", "genrsa", "4096"], stdout=fp)
    csr = cert_dir / "domain.csr"
    if not csr.exists():
        with csr.open("w") as fp:
            subprocess.call(
                [
                    "openssl",
                    "req",
                    "-new",
                    "-sha256",
                    "-key",
                    private_key,
                    "-subj",
                    '"/"',
                    "-addext",
                    f'"subjectAltName = DNS:{domain}, DNS:www.{domain}"',
                ],
                stdout=fp,
            )
    challenge_dir = cert_dir / "challenges"
    challenge_dir.mkdir(exist_ok=True)
    with (cert_dir / "domain.crt").open("w") as fp:
        fp.write(acme_tiny.get_crt(account_key, csr, challenge_dir))
    # XXX csr.unlink()
