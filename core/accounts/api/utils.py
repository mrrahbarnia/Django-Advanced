from threading import Thread


class EmailThread(Thread):
    def __init__(self, email_object):
        self.email_object = email_object
        Thread.__init__(self)

    def run(self):
        self.email_object.send(fail_silently=False)
