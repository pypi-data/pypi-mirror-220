"""Command line interface for hyfit"""
from hyfi import about, hydra_main


def main() -> None:
    """Main function for the CLI"""
    hydra_main(config_path=about.config_path)


if __name__ == "__main__":
    main()
