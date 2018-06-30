#!/usr/bin/python3

# {"username": [{"message": "\u8bf7\u8f93\u5165\u7528\u6237\u540d", "code": "required"}],
#  "password": [{"message": "\u8bf7\u8f93\u5165\u5bc6\u7801", "code": "required"}]}


class FormMiXin(object):
    def get_errors(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            new_errors={}
            for key,message_dicts in errors.items():
                messages=[]
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key]=messages
            return new_errors
        else:
            return {}