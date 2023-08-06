import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

# Address - https://explorer.hydrachain.org/address/HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir/
address_transactions = explorer_requester.get_address_transactions("HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir")

logger.info(address_transactions)
