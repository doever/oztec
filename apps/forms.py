#!/usr/bin/python3
import json


class FormMiXin(object):
    def get_errors(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key,message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}

    # 取第一个错误
    def get_first_error(self):
        if hasattr(self, 'errors'):
            errors = self.errors.as_json()
            errors = json.loads(errors)
            # first_error = sorted(first_error_list[0].items())[1][1]

            key = list(errors.keys())[0]
            first_error = sorted(errors[key][0].items())[1][1]
            return first_error

