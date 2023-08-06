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