import telnetlib
from ntlm_auth.ntlm import NtlmContext
from colorama import Fore
from base64 import b64encode, b64decode

class SMTP:
    def __init__(self, server_addr: str, port: int, sender_email: str, debug: bool = False) -> None:
        """SMTP Class

        Args:
            server_addr (str): Outlook Server Address
            port (int): Server Port
            sender_email (str): Mail for sending Emails
            debug (bool, optional): Print Debug Messages. Defaults to False.
        """
        self.__telnet_conn = telnetlib.Telnet(server_addr, port)
        self.__debug = debug
        self.ehlo()
        self.authenticated = False
        self.sender_email = sender_email

    def __read_until_done(self, tmout: int = 1, singular: bool = False):
        rsp_list = []
        if singular:
            rsp = self.__telnet_conn.read_until(b'\r\n', timeout=tmout).decode('utf-8').strip()
            if self.__debug: print(Fore.GREEN + rsp + Fore.RESET)
            return [rsp]
        while True:
            rsp = self.__telnet_conn.read_until(b'\r\n', timeout=tmout).decode('utf-8').strip()
            if rsp == "":
                return rsp_list
            if self.__debug: print(Fore.GREEN + rsp + Fore.RESET)
            rsp_list.append(rsp)

    def __send_command_and_get_response(self, command: str, tmout: int = 1, singular: bool = True) -> list[str]:
        if self.__debug: print(Fore.BLUE + command + Fore.RESET)
        self.__telnet_conn.write(command.encode('utf-8') + b'\r\n')
        return self.__read_until_done(tmout, singular)

    def ehlo(self) -> list[str]:
        """Perform EHLO Command
        Get's called automatically on instantiating

        Returns:
            list[str]: EHLO Features
        """
        return self.__send_command_and_get_response("EHLO", singular=False)
    
    def test_NTLM(self) -> bool:
        """Test if the Server supports NTLM before actually authenticating

        Returns:
            bool: Has NTLM
        """
        return False if ("334" in self.__send_command_and_get_response("AUTH NTLM")) else True

    def authenticate(self, ntlm_context: NtlmContext) -> bool:
        """Authenticate User via NTLM

        Args:
            ntlm_context (NtlmContext): NTLM Context

        Returns:
            bool: Successfull authentication
        """
        if not self.authenticated:
            ntlm_negotiate_message = ntlm_context.step()
            rsp = self.__send_command_and_get_response(b64encode(ntlm_negotiate_message).decode("utf-8"))
            challenge = rsp[0].split(" ")[1]
            ntlm_auth_response = ntlm_context.step(b64decode(challenge))
            self.authenticated = "235" in self.__send_command_and_get_response(b64encode(ntlm_auth_response).decode("utf-8"))[0]
            return self.authenticated
        
    def send_mail(self, receiver_email: str, subject: str, html_body: str) -> bool:
        """Sends email to Recepient

        Args:
            receiver_email (str): Receiver Email
            subject (str): Email Subject
            html_body (str): HTML Body (Normal text also supported)

        Returns:
            bool: Successfull sending of email
        """
        self.__send_command_and_get_response(f"mail from: {self.sender_email}")
        self.__send_command_and_get_response(f"rcpt to: {receiver_email}")
        self.__send_command_and_get_response("data")
        msg = f"""From: <{self.sender_email}>
To: <{receiver_email}>
Subject: {subject}
Content-Type: text/html; charset=UTF-8

{html_body}
"""
        self.__telnet_conn.write(msg.encode("utf-8"))
        self.__telnet_conn.write(b"\r\n.\r\n")
        return "Queued mail for delivery" in self.__read_until_done(singular=True)[0]