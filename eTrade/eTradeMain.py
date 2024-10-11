
# from load import Loader
# import threading
# from TGenerator import TGenerator
# from param import parameters
# from tinWriter import TinManager
# import logging


# logging.basicConfig(
#         filename='etrade_logs/app.log',  # Specify log file
#         level=logging.ERROR,  # Set logging level to capture errors
#         format='%(asctime)s - %(levelname)s - %(message)s'  # Customize the log format
#     )

# def run_in_thread(tin, url):
#     page_loader = Loader(url)
#     try:
#         page_loader.load_page(tin)
#     except Exception as e:
#         logging.error('Error loading page: %s', e)
#         return e


# if __name__ == '__main__':
#     # Example of running multiple threads
#     # tins =['0011385998']
#     # tins =['0021385998','0011385998']
#     logging.info('iScrap initiated ...')
    

#     #  usage:
#     gen = TGenerator()
#     param = parameters()

#     while (True):

#         # Get the first n numbers
#         tins =  gen.get_next_numbers(param.eTradeParam['batch_size']) 


#         # tins = ['001138599']  # Replace with actual TINs
#         threads = []
#         # url= 'https://etrade.gov.et/business-license-checker'

#         for tin in tins:
#             logging.info('Extracting Tin numbers of size: ', len(tins))
#             thread = threading.Thread(target=run_in_thread, args=(tin,param.eTradeParam['base_url']+'?tin=00'+str(tin),))
#             threads.append(thread)
#             thread.start()

#         # Wait for all threads to complete
#         for thread in threads:
#             thread.join()


import threading
import logging
from load import Loader
from TGenerator import TGenerator
from param import parameters
from tinWriter import TinManager

# Configure logging
logging.basicConfig(
    filename='etrade_logs/app.log',    # Log file location
    level=logging.ERROR,               # Log only errors
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp, level, and message
)

def run_in_thread(tin, url):
    """
    Function to load a page in a thread-safe way.
    Args:
        tin (str): The TIN number to process.
        url (str): The URL to load.
    """
    page_loader = Loader(url)
    try:
        page_loader.load_page(tin)
    except Exception as e:
        logging.error('Error loading page for TIN %s: %s', tin, e)
        return e

def main():
    """
    Main function to initiate scraping using multiple threads.
    TINs are processed in batches and each batch runs in its own thread.
    """
    print('iScrap initiated...')

    logging.info('iScrap initiated...')

    # Initialize generator and parameters
    gen = TGenerator()
    param = parameters()

    while True:
        # Get the next batch of TINs
        tins = gen.get_next_numbers(param.eTradeParam['batch_size'])

        if not tins:
            logging.info('No more TINs to process. Exiting...')
            print('No more TINs to process. Exiting...',end='\r')
            break

        logging.info('Processing %d TIN numbers...', len(tins))
        print('Processing %d TIN numbers...', len(tins),end='\r')
        
        threads = []

        for tin in tins:
            url = f"{param.eTradeParam['base_url']}?tin=00{str(tin)}"
            thread = threading.Thread(target=run_in_thread, args=(tin, url))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    main()
