#!/usr/bin/env python3
import smtpd
import asyncore
import logging


class SMTPServer(smtpd.SMTPServer):

    def process_message(*args, **kwargs):
        logging.info(f'receive message: {args} {kwargs}')


if __name__ == "__main__":
    logging.basicConfig(
        format = '%(asctime)s %(levelname)-8s %(message)s',
        level = logging.DEBUG)
    port = 9999
    smtp_server = SMTPServer(('0.0.0.0', port), None)
    logging.info(f'listening at {port}')
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()