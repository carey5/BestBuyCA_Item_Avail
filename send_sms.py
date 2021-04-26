# Download the helper library from https://www.twilio.com/docs/python/install
def send_sms(body, sender, to):
    from twilio.rest import Client


    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC4eb3c1795c6e2286bd50f3408f18bde8'
    auth_token = 'c2367ad32663b29ca5fd406ea44f42f3'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=body,
                         from_=sender,
                         to=to
                     )


if __name__ == "__main__":
    send_sms(body, sender, to)
