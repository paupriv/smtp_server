# smtp_server

This is an server which uses the smtp protocol. It operates on the default port 25.
The program receives emails and save the contents.

Its important that the email's body were checked by dkim signature.
The key can be found on (sample) s1._domainkey.domain.com txt record in dns
The subdomain can be found in the header of the email.
