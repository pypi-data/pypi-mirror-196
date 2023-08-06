from .filer import Filer

def main():
    import sys
    filer = Filer(sys.argv[1], directory=sys.argv[2])
    filer.start()


if __name__ == "__main__":
    main()