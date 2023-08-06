import os


def attr_test(msg: str):
    print(msg)


def label_from_callable(fn):
    if hasattr(fn, 'default_label'):
        return fn.default_label()
    elif hasattr(fn, '__name__'):
        if fn.__name__ == '<lambda>':
            return '<lambda at %s:%s>' % (
                os.path.basename(fn.__code__.co_filename), fn.__code__.co_firstlineno)
        return fn.__name__
    return str(fn)


def main():
    print(label_from_callable(attr_test))


if __name__ == "__main__":
    main()
