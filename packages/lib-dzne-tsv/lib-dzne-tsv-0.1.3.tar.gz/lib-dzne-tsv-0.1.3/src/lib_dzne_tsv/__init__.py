import csv as _csv
import collections as _collections 
#import Counter


class Dialect(_csv.Dialect):
    delimiter = '\t'
    doublequote = False
    escapechar = None
    lineterminator = '\n'
    quotechar = '"'
    quoting = _csv.QUOTE_NONE
    skipinitialspace = False
    strict = True

def reader(target):
    return _csv.reader(target, dialect=Dialect)

def writer(target):
    return _csv.writer(target, dialect=Dialect)

class DictReader:
    def __iter__(self):
        return self
    def __init__(self, reader, *, fixed_width=True):
        self._reader = iter(reader)
        self._fieldnames = next(self._reader)
        errors = list()
        for item, count in _collections.Counter(self._fieldnames).items():
            if count > 1:
                errors.append(
                    KeyError(
                        f"The column-name {item} occures more than once! "
                    )
                )
        if len(errors):
            raise ExceptionGroup("Improperly formatted! ", errors)
        self._linenumber = 0

        if fixed_width is False:
            self._width = None
        elif fixed_width is True:
            self._width = len(self._fieldnames)
        elif type(fixed_width) is int:
            if fixed_width < 0:
                raise ValueError(
                    f"The parameter fixed_width must be at least zero! "
                )
            if fixed_width != len(self._fieldnames):
                raise ValueError(
                    f"Header has wrong number of elements! "
                )
            self._width = fixed_width
        else:
            raise TypeError(f"The parameter fixed_width must either be int or bool! ")
    def __next__(self):
        if self._width is not None:
            if self._width != len(line):
                raise ValueError(
                    f"Row {self._linenumber} has the wrong number of elements! "
                )
        self._linenumber += 1
        return dict(zip(self._fieldnames, line))



class DictWriter:
    def __init__(self, target, *, fieldnames=None):
        self._writer = writer(target)
        if fieldnames is None:
            self._fieldnames = None
        else:
            self._fieldnames = tuple(fieldnames)
            self._writer.writerow(fieldnames)
    def writerow(self, row):
        if self._fieldnames is None:
            self._fieldnames = tuple(row.keys())
            self._writer.writerow(fieldnames)
        else:
            errors = list()
            for x in row.keys():
                if x not in self._fieldnames:
                    errors.append(
                        KeyError(
                            f"The key {x} is missing! "
                        )
                    )
            for x in self._fieldnames:
                if x not in row.keys():
                    errors.append(
                        KeyError(
                            f"The key {x} is unexpected! "
                        )
                    )
            if len(errors):
                raise ExceptionGroup("Improper row! ", errors)
        self._writer.writerow([row[x] for x in self._fieldnames])










