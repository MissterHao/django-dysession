from io import StringIO

import boto3
from django.core.management import call_command
from django.test import TestCase


class CommandTestCase:
    def call_command(self, command: str, *args, stdout=None, stderr=None, **kwargs):
        if stdout is None:
            stdout = StringIO()
        if stderr is None:
            stderr = StringIO()

        call_command(
            command,
            *args,
            stdout=stdout,
            stderr=stderr,
            **kwargs,
        )
        return stdout.getvalue(), stderr.getvalue()


# class DysessionInitTestCase(CommandTestCase, TestCase):
#     @mock_dynamodb
#     def test_init_dynamodb_table(self):

#         client = boto3.client("dynamodb")
#         print(client)
#         pass


# class DysessionClearTestCase(CommandTestCase, TestCase):
#     def test_call_help(self):
#         out = StringIO()
#         call_command("dysession_clear", "-h", stdout=out)
#         print(out.read())

#         call_command("dysession_clear", *["-u", "XD"], "-h", stdout=out)
#         print(out.read())


# class DysessionDestoryTestCase(CommandTestCase, TestCase):
#     def test_call_help(self):
#         out = StringIO()
#         call_command("dysession_destory", "-h", stdout=out)
#         print(out.read())
