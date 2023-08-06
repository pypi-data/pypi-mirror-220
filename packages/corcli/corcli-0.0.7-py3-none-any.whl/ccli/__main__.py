"""
Main class
"""
import argparse
import tomllib

from getpass import getpass
from os import environ
from os import path

try:
    from ccli.analyzer import run_analyzers
except ModuleNotFoundError:
    from analyzer import run_analyzers

def init_argparse() -> argparse.ArgumentParser:
    """Initialise the argument parsers

    This function creates an instance of `argparse.ArgumentParser` and configures it
    with the following command line arguments:

    Args:
        -a, --alias: Specify the analyzer using the alias.
        -s, --selector: Selector mode to select one or multiple analyzers available
            from the Cortex instance.
        -d, --debug: Enable debug mode.

    Returns:
        An instance of `argparse.ArgumentParser` configured with the specified
        command line arguments.
    """
    parser = argparse.ArgumentParser(
                        prog='corcli',
                        description='Submit Cortex analysers/responders job using the CLI',
                        epilog='If you spot issues, reach me out at https://github.com/0xFustang/corcli/issues'
                                     )
    parser.add_argument("-c", "--cortex-url", help="Specify the Cortex URL")
    parser.add_argument("-k", "--api-key", help="Specify the API key")
    parser.add_argument("-vf", "--verify-cert", help="Specify the certificate verification mode", action=argparse.BooleanOptionalAction)
    parser.add_argument("-a", "--alias", help="Specify the analyzer using the alias", action="append")
    parser.add_argument("-d", "--domain", help="Specify the observable type as domain")
    parser.add_argument("-u", "--url", help="Specify the observable type as url")
    parser.add_argument("-ha", "--hash", help="Specify the observable type as hash")
    parser.add_argument("-f", "--file", help="Specify the observable type as file")
    parser.add_argument("-m", "--mail", help="Specify the observable type as mail")
    parser.add_argument("-i", "--ip", help="Specify the observable type as ip")
    parser.add_argument("-ci", "--cortex-instance", help="Specify the Cortex instance number")
    parser.add_argument("-e", "--extract-only", help="Display only the extracted artifacts", action="store_true")
    parser.add_argument("-fr", "--full-report", help="Display the full report", action="store_true")
    parser.add_argument("-nc", "--no_cache", help="Force no caching", action="store_true")
    parser.add_argument("-cf", "--config-file", help="Set the configuration file path")
    return parser

def main() -> None:
    """Main function

    This function simply read the config file and build the parameters for run_analyzer
    """
    parser = init_argparse()
    args = parser.parse_args()

    if not (args.domain or
            args.ip or
            args.hash or
            args.url or
            args.file or
            args.mail):
        parser.error('No observable type selected, check the available options using -h')
    elif args.domain:
        args.observable_type = 'domain'
        args.observable_data = args.domain
    elif args.ip:
        args.observable_type = 'ip'
        args.observable_data = args.ip
    elif args.hash:
        args.observable_type = 'hash'
        args.observable_data = args.hash
    elif args.url:
        args.observable_type = 'url'
        args.observable_data = args.url
    elif args.file:
        args.observable_type = 'file'
        args.observable_data = args.file
        if not path.isfile(args.file):
            print(f'File {args.file} not found')
            exit(1)
    elif args.mail:
        args.observable_type = 'mail'

    if args.config_file:
        try: # Try to open the configuration file ccli_config.toml
            with open(args.config_file) as file_obj:
                content = file_obj.read()
                config_data = tomllib.loads(content)
        except FileNotFoundError:
            """Pass except if the config file is not found
            If the configuration file is not found, pass take the arguments passed in the command
            """
            pass
        except Exception:
            raise Exception("Something unexepected happened...")

        if not args.cortex_instance:
            cortex_instance = "default"
        else:
            cortex_instance = args.cortex_instance

        try:
            config_cortex_info = config_data["cortex-instance"][cortex_instance]
        except KeyError:
            raise KeyError(f"cortex-instance '{cortex_instance}' not found in the config")
        except Exception:
            raise Exception("Something unexepected happened...")

    else:
        if not args.cortex_url:
            print("Error: please provide the Cortex instance URL using -c/--cortex-url or a configuration file using -cf/--config-file option.")
            exit(1)

    if not args.cortex_url:
        try:
            args.cortex_url = config_cortex_info["url"] # Override args.cortex_url
        except KeyError:
            print("Error: missing key url in the configuration file.")
    if not args.verify_cert:
        try:
            args.verify_cert = config_cortex_info["verify_cert"]
        except KeyError or FileNotFoundError:
            print("Warning: verify_cert key not found in the configuration, verify certificate is set to true by default")
            args.verify_cert = True
        except Exception:
            args.verify_cert = True

    if args.no_cache:
        args.no_cache = 1 # Option to set no caching in Cortex (force=1)
    else:
        args.no_cache = 0

    if args.alias:
        alias_values = []
        for alias in args.alias:
            try:
                if alias in config_cortex_info:
                    alias_value = config_cortex_info[alias]
                    alias_values.append(alias_value)
                else:
                    print(f"alias '{alias}' not found in the config")
                    exit(1)
            except Exception:
                raise Exception("Something unexepected happened...")

        args.alias = alias_values

    if args.api_key:
        pass
    elif environ.get('CORTEX_CLI_API'):
        args.api_key = environ.get('CORTEX_CLI_API')
    else:
        args.api_key = getpass("Please provide your Cortex API key:")
        print("------\n")

    parameters = args

    run_analyzers(parameters)

if __name__ == "__main__":
    main()
