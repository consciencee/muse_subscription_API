class Subscription:
    def __init__(self):
        self.subscribers = []

    def add_subscriber(self, subscriber):
        subscr_event_interface = getattr(subscriber, "on_event", None)
        if callable(subscr_event_interface):
            self.subscribers.append(subscriber)
        else:
            print("Subscriber must implement \"on_event(data)\" function")

    def rm_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify_all_subscribers(self, data):
        for subscriber in self.subscribers:
            subscriber.on_event(data)
