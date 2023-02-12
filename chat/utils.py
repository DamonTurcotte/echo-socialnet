from chat.models import PvtMessage

def message_list(chat_query, current_user):
    chat_messages = PvtMessage.objects.filter(
        chat=chat_query).order_by('timestamp').reverse()
    message_list = []
    for item in chat_messages:
        if item.message == '':
            continue

        message_obj = dict()

        if item.sender == current_user:
            sender = True
        else:
            sender = False

        message = item.message

        message_obj['sender'] = sender
        message_obj['content'] = message
        message_obj['timestamp'] = item.when_last()  # type:ignore
        message_list.append(message_obj)

    return message_list
