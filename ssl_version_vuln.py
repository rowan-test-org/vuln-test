import ssl
from OpenSSL import SSL, crypto
import socket

# vuln when used with pyopenssl 17.4.0

def verify_certificate(hostname, port):
    """Connects to a host and attempts to verify its SSL certificate
    using potentially outdated methods."""
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))

        # Wrap the socket with SSL/TLS using potentially older context settings
        ctx = SSL.Context(SSL.SSLv23_METHOD)  # Using a general method that might include older, weaker protocols
        ssl_sock = SSL.Connection(ctx, sock)
        ssl_sock.set_tlsext_host_name(hostname.encode())  # For Server Name Indication (SNI)
        ssl_sock.do_handshake()

        # In a vulnerable older version, certificate verification might be flawed
        # or might not enforce modern security standards.

        cert = ssl_sock.get_peer_certificate()
        if cert:
            print(f"Successfully connected to {hostname}:{port} and received a certificate:")
            print(crypto.dump_certificate(crypto.FILETYPE_TEXT, cert).decode())
            print("Note: An older pyOpenSSL might not properly validate this certificate against modern security standards.")
        else:
            print(f"Successfully connected to {hostname}:{port}, but no certificate was received.")

        ssl_sock.shutdown()
        sock.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_host = input("Enter a hostname to connect to (e.g., google.com): ")
    target_port = int(input("Enter the port (e.g., 443 for HTTPS): "))
    print(f"\nAttempting to connect to {target_host}:{target_port} using potentially outdated SSL/TLS methods...")
    verify_certificate(target_host, target_port)
