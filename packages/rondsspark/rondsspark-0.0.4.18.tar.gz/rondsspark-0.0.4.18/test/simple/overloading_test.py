class pipely(object):
    def __init__(self, *args, **kw):
        self._args = args
        self.__dict__.update(kw)

    def __ror__(self, other):
        if isinstance(other, bad):
            return other.val()
        return (self.map(x) for x in other if self.filter(x))

    def map(self, x):
        return x

    def filter(self, x):
        return True


class sieve(pipely):
    def filter(self, x):
        n = self._args[0]
        return x == n or x % n


class strify(pipely):
    def map(self, x):
        return str(x)


class startswith(pipely):
    def filter(self, x):
        n = str(self._args[0])
        if x.startswith(n):
            return x


class bad(object):
    def val(self):
        return 1, 2, 3


def main():
    for i in range(2, 100) | sieve(2) | sieve(3) | sieve(5) | sieve(7) | strify() | startswith(5):
        print(i)


if __name__ == '__main__':
    main()
