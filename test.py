from app.flask import AppLogic

obj = AppLogic()


def test_do_log(log_message="test_log_message", level="Debug"):
    obj.do_log(log_message, level)


if __name__ == '__main__':
    test_do_log()
