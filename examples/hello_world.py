#!/usr/bin/env python3

import concur as c


def app():
    return c.button("Close")


if __name__ == "__main__":
    c.integrations.main("Hello World", app(), 500, 500)
