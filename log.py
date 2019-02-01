# My personal invention
# TODO: add license
import config


def logi(message, description):
    if config.log if hasattr(config, 'log') else True:
        print("(I)", message.from_user.username, description, ("(id: {0})".format(message.chat.id)))
