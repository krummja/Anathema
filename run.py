from argparse import ArgumentParser


if __name__ == '__main__':
    from anathema import prepare, main
    config = prepare.CONFIG
    main.main(load_slot = 0)
