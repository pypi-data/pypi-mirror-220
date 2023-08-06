"""
Module to use analysers
"""
import concurrent.futures

from time import sleep

try:
    from ccli.cortex import Cortex
except ModuleNotFoundError:
    from cortex import Cortex

def run_analyzers(parameters) -> None:
    """Runs analyzer jobs using the Cortex instance.

    Args:
        parameters (dict): Parameters for Cortex submission.

    Returns:
        None
    """
    cortex = Cortex(parameters)

    if not parameters.alias:
        print("No alias selected. Going to selector...")
        target_analyzer = cortex.select_analyzers()
    else:
        target_analyzer = parameters.alias
        cortex.authentication()

    print(f"Analysis in progress....")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_sub = {executor.submit(cortex.run_analyzer_job, param): param for param in target_analyzer}

        for future in concurrent.futures.as_completed(future_sub):
            param = future_sub[future]
            print("---")
            print(f'Result for analyzer {param}:\n')
            try:
                response = future.result()
                if parameters.extract_only:
                    if not response:
                        response = future.result()
                        print("No observables extracted.\n")
                    else:
                        for line in response:
                            print(line)
                elif parameters.full_report:
                    print(response) # Show the full analysis report in json
                else:
                    if not response:
                        response = future.result()
                        print("No summary report. Use -fr argument to display the full report.\n")
                    else:
                        for line in response:
                            print(line)
            except KeyboardInterrupt:
                for future in future_sub:
                    print("Canceling tasks ...")
                    future.cancel()
            except Exception as e:
                print(f'Something went wrong while launching a job for {param}: \n{e}')
            finally:
                executor.shutdown(wait=True)

