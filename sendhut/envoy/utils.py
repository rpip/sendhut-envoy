class ItemSet(object):
    """
    Represents a set of objects: deliveries, couriers etc.
    """
    def __iter__(self):
        raise NotImplementedError()

    def count(self):
        """Return the total"""
        pass


class ItemList(list, ItemSet):

    def __repr__(self):
        return 'ItemList(%s)' % (super(ItemList, self).__repr__(),)


class Partitioner(ItemSet):
    """
    Represents an ItemSet partitioned for purposes such as delivery
    Override the __iter__() method to provide custom partitioning.
    """
    def __init__(self, subject):
        self.subject = subject

    def __iter__(self):
        'Override this method to provide custom partitioning'
        yield ItemList(self.subject)

    def __nonzero__(self):
        return bool(self.subject)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.subject)

    def classify(self, item):
        raise NotImplementedError()

    def get_partition(self, classifier, items):
        return ItemList(items)


class GroupingPartitioner(Partitioner):

    def __init__(self, subject, keyfunc, partition_class):
        self.keyfunc = keyfunc
        self.partition_class = partition_class
        super(GroupingPartitioner, self).__init__(subject)

    def __iter__(self):
        subject = sorted(self.subject, key=self.classify)
        for classifier, items in groupby(subject, key=self.classify):
            yield (classifier, self.get_partition(classifier, items))

    def classify(self, item):
        return self.keyfunc(item)

    def get_partition(self, classifier, items):
        return self.partition_class(items)


def partition(subject, keyfunc, partition_class=list):
    return GroupingPartitioner(subject, keyfunc, partition_class)
