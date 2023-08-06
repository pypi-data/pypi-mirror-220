# NTLMAIL
### Emailing with SMTP and NTLM made easy

- Easy to Use
- Fast and Reliable
- Based on the <a href="https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-smtpntlm/">original Documentation</a> by Microsoft

```python
from ntlm_auth.ntlm import NtlmContext
from ntlmail import SMTP

# Create NTLM Context for auth
auth = NtlmContext("username", "password", "domain")

# Create SMTP Connection to the Server
conn = SMTP("server.test.com", 587, "test@gmail.com")

# Check if the Server supports NTLM
print(conn.test_NTLM())

# Authenticate via the NTLM Context from above
print(conn.authenticate(auth))

# Ready to send Emails now
print(conn.send_mail("receiver@gmail.com", "Hey there!", "<h1>This email was sent via NTLMAIL</h1>"))
```

## Contributing

- If you have any contribution Ideas or Improvements, don't hesitate adding them!