from .atomic import resize_terminal
import time


def greeting(logo: str, product: str, version: str, rows=128, cols=32, delay_1=0.75, delay_2=0.1, delay_3=0.5) -> None:
    resize_terminal(rows, cols)
    # Print Logo
    print(logo)
    time.sleep(delay_1)
    for line in product.format(version).split('\n'):
        print(line)
        time.sleep(delay_2)
    time.sleep(delay_3)
