import os
from xrpl import CryptoAlgorithm
from xrpl.ledger import get_fee
from xrpl.wallet import Wallet
import inquirer
from inquirer.themes import GreenPassion
from claudia.python.features.environment import get_client, get_test_genesis_wallet
from claudia.python.lib.framework.common import *
from claudia.python.lib.framework import constants
from claudia.python.lib.framework.object_factory import ObjFactory, ObjType

class Context(object):
    connectionType = None
    url = None
    client = None
    crypto_algorithm = None
    test_genesis_wallet = None
    default_fee = None
    minDrop = None
    transferAmount = None
    exception = None
    test_status = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Context, cls).__new__(cls)
        return cls.instance


def init_context():
    try:
        context = Context()
        context.connectionType = read_env_var('CONNECTION_TYPE')
        connectionScheme = read_env_var('CONNECTION_SCHEME')
        connectionURL = read_env_var('CONNECTION_URL')
        context.url = "{}://{}".format(connectionScheme, connectionURL)
        try:
            context.client = get_client(context)
        except ConnectionRefusedError:
            raise Exception("\nERROR: Cannot connect to {}. Make sure the network is accessible.".format(context.url))
        context.crypto_algorithm = CryptoAlgorithm.SECP256K1
        context.test_genesis_wallet = get_test_genesis_wallet(context)
        context.default_fee = int(get_fee(context.client))
        context.minDrop = context.default_fee
        context.transferAmount = constants.DEFAULT_TRANSFER_AMOUNT
        context.exception = None
        context.test_status = None
        return context
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")

def launch_workflow():
    try:
        clear_screen()
        questions = [
            inquirer.List(
                "main_menu",
                message="Welcome to the XRPL Concept Learning Center! "
                        "Please use ↑ ↓ and ↵ keys to choose an option. Current Selection",
                choices=[
                    "Create a new account",
                    "Send payment",
                    "Mint NFT",
                    "Burn NFT",
                    "Create NFT buy offer",
                    "Accept NFT buy offer",
                    "Create NFT sell offer",
                    "Accept NFT sell offer",
                    "Exit"
                ],
            ),
        ]

        selection_text = inquirer.prompt(questions, theme=GreenPassion())['main_menu']

        if selection_text == "Create a new account":
            clear_screen()
            create_account()
        if selection_text == "Send payment":
            clear_screen()
            send_payment_across_accounts()
        if selection_text == "Mint NFT":
            clear_screen()
            mint_nft()
        if selection_text == "Burn NFT":
            clear_screen()
            burn_nft()
        if selection_text == "Create NFT buy offer":
            clear_screen()
            create_nft_buy_offer()
        if selection_text == "Accept NFT buy offer":
            clear_screen()
            accept_nft_buy_offer()
        if selection_text == "Create NFT sell offer":
            clear_screen()
            create_nft_sell_offer()
        if selection_text == "Accept NFT sell offer":
            clear_screen()
            accept_nft_sell_offer()
        elif selection_text == 'Exit':
            clear_screen()
            return
    except Exception as e:
        pass


def get_confirmation(confirmation_message):
    try:
        q = [inquirer.List("confirmation", message=confirmation_message, choices=["Yes", "No"], default="No")]
        answer = inquirer.prompt(q, theme=GreenPassion())['confirmation']
        if (answer == 'Yes'):
            return_value = True
        else:
            return_value = False
        return return_value
    except Exception as e:
        pass


def create_account():
    try:
        print("Launching 'Create a new account' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"
        print(" - Propose a new wallet")
        wallet = Wallet.create(crypto_algorithm=context.crypto_algorithm)
        print(" - Fund the new wallet from test genesis account")
        fund_amount = constants.DEFAULT_ACCOUNT_FUND_AMOUNT
        response = send_payment(context,
                                source_wallet=context.test_genesis_wallet,
                                destination_wallet=wallet,
                                amount=fund_amount)
        print(" - Verify if funding succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )
        print(" - Workflow Summary:")
        print(f"     - Wallet Address: {wallet.classic_address}")
        print(f"     - Wallet Seed: {wallet.seed}")
        print(f"     - Wallet Funds: {get_account_balance(context, wallet.classic_address)}")
        print(f"     - Source Wallet Address: {context.test_genesis_wallet.classic_address}")
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def send_payment_across_accounts():
    try:
        print("Launching 'Send payment' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"

        print(" - Get source wallet information")
        source_wallet, source_address, source_seed = get_wallet_info(context, "source")
        print(" - Get destination wallet information")
        destination_wallet, destination_address, destination_seed = get_wallet_info(context, "destination")

        initial_source_balance = get_account_balance(context, source_address)
        initial_destination_balance = get_account_balance(context, destination_address)
        print(" - Get transfer amount information")
        question = [
            inquirer.Text('amount',
                          message=f"Please enter the amount of XRP to transfer. "
                                  f"OR just press ↵ (return) key to accept default ({constants.DEFAULT_TRANSFER_AMOUNT}).")
        ]
        amount = str(inquirer.prompt(question, theme=GreenPassion())['amount'])
        if amount.replace("'", "").replace('"', '').lower() == '':
            amount = constants.DEFAULT_TRANSFER_AMOUNT
        print(f" - Sending payment transaction")
        response = send_payment(context,
                                source_wallet=source_wallet,
                                destination_wallet=destination_wallet,
                                amount=amount)
        print(" - Verify if transaction succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )
        print(" - Workflow Summary:")
        print(f"     - Source Wallet Address: {source_address}")
        print(f"     - Source Wallet Seed: {source_seed}")
        print(f"     - Source Wallet Current Balance: {get_account_balance(context, source_address)}")
        print(f"     - Source Wallet Initial Balance: {initial_source_balance}")
        print(f"     - Destination Wallet Address: {destination_address}")
        print(f"     - Destination Wallet Seed: {destination_seed}")
        print(f"     - Destination Wallet Current Balance: {get_account_balance(context, destination_address)}")
        print(f"     - Destination Wallet Initial Balance: {initial_destination_balance}")
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def mint_nft():
    try:
        print("Launching 'Mint NFT' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"

        print(" - Get owner account information")
        owner_wallet, owner_address, owner_seed = get_wallet_info(context, "owner")

        print(" - Minting NFT")
        payload = ObjFactory.getObj(
            ObjType.nft_token_mint,
            account=owner_address,
            nftoken_taxon=0,
            flags=8
        )
        response = sign_autofill_and_submit(context.client, payload, owner_wallet)
        print(f" - Verify if minting succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )

        nftoken = get_nft_tokens(context.client, owner_address)[-1]
        print(" - Workflow Summary:")
        print(f"     - Owner Wallet Address: {owner_address}")
        print(f"     - Owner Wallet Seed: {owner_seed}")
        print(f"     - Minted NFT ID: {nftoken}")
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def burn_nft():
    try:
        print("Launching 'Burn NFT' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"

        print(" - Get owner account information")
        owner_wallet = get_existing_wallet_info(context, 'owner')
        owner_address = owner_wallet.classic_address
        owner_seed = owner_wallet.seed

        initial_owner_nft_count = len(get_nft_tokens(context.client, owner_address))
        question = [
            inquirer.Text('nft_id',
                          message=f"Please enter the NFT ID for the owner account")
        ]
        nft_id = str(inquirer.prompt(question, theme=GreenPassion())['nft_id'])
        owner_nft_count_post_minting = len(get_nft_tokens(context.client, owner_address))

        print(" - Burning the NFT")
        payload = ObjFactory.getObj(
            ObjType.nft_token_burn,
            account=owner_address,
            nftoken_id=nft_id,
        )
        response = sign_autofill_and_submit(context.client, payload, owner_wallet)

        print(f" - Verify if burning succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )

        owner_nft_count_post_burning = len(get_nft_tokens(context.client, owner_address))

        print(" - Workflow Summary:")
        print(f"     - Owner Wallet Address: {owner_address}")
        print(f"     - Owner Wallet Seed: {owner_seed}")
        print(f"     - Burnt NFT ID: {nft_id}")
        print(f"     - Owner Wallet Initial NFT Count: {initial_owner_nft_count}")
        print(f"     - Owner Wallet NFT Count after minting: {owner_nft_count_post_minting}")
        print(f"     - Owner Wallet NFT Count after burning: {owner_nft_count_post_burning}")
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def create_nft_buy_offer():
    try:
        print("Launching 'Create NFT buy offer' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"

        print(" - Get owner account information")
        owner_wallet, owner_address, owner_seed = get_wallet_info(context, "owner")

        print(" - Get buyer account information")
        buyer_wallet, buyer_address, buyer_seed = get_wallet_info(context, "buyer")

        if get_confirmation(f"Do you have an NFT already minted? If not, we can mint one for you"):
            print(" - Enter NFT information")
            question = [
                inquirer.Text('nft_id', message=f"Please enter the NFT ID")
            ]
            nftoken_id = str(inquirer.prompt(question, theme=GreenPassion())['nft_id'])

        else:
            print(f"     - Okay! Minting a new NFT")
            payload = ObjFactory.getObj(
                ObjType.nft_token_mint,
                account=owner_address,
                nftoken_taxon=0,
                flags=8
            )
            response = sign_autofill_and_submit(context.client, payload, owner_wallet)
            print(f" - Verify if minting succeeded")
            if ResponseCode.success not in str(response):
                raise Exception(
                    "Expected response code was not received."
                    "\nExpected Code = '{}'."
                    "\nResponse received: '{}'".format(ResponseCode.success, response)
                )

            nfttokens = get_nft_tokens(context.client, owner_address)
            nftoken_id = nfttokens[-1]

        print(f" - Create a buy offer")
        payload = ObjFactory.getObj(
            ObjType.nf_token_create_offer,
            account=buyer_address,
            owner=owner_address,
            nftoken_id=nftoken_id,
            amount=context.transferAmount
        )
        response = sign_autofill_and_submit(context.client, payload, buyer_wallet)

        print(f" - Verify if offer creation succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )

        print(" - Workflow Summary:")
        print(f"     - Owner Wallet Address: {owner_address}")
        print(f"     - Owner Wallet Seed: {owner_seed}")
        print(f"     - Buyer Wallet Address: {buyer_address}")
        print(f"     - Buyer Wallet Seed: {buyer_seed}")
        print(f"     - Minted NFT ID: {nftoken_id}")
        print(f"     - Created Offer ID: {get_token_offers_response(context.client, buyer_address, token_id=nftoken_id)[0]}")
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def accept_nft_buy_offer():
    try:
        print("Launching 'Accept NFT buy offer' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"

        print(" - Get owner account information")
        owner_wallet = get_existing_wallet_info(context, 'owner')
        owner_address = owner_wallet.classic_address
        owner_seed = owner_wallet.seed

        print(" - Get buy offer information")
        question = [
            inquirer.Text('offer_id', message=f"Please enter the Buy Offer ID")
        ]
        offer_id = str(inquirer.prompt(question, theme=GreenPassion())['offer_id'])

        print(f" - Accept the buy offer")
        payload = ObjFactory.getObj(
            ObjType.nf_token_accept_offer,
            account=owner_address,
            nftoken_buy_offer=offer_id
        )
        response = sign_autofill_and_submit(context.client, payload, owner_wallet)

        print(f" - Verify if offer acceptance succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )

        print(" - Workflow Summary:")
        print(f"     - Owner Wallet Address: {owner_address}")
        print(f"     - Owner Wallet Seed: {owner_seed}")
        print(f"     - Accepted Buy Offer ID: {offer_id}")
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def create_nft_sell_offer():
    try:
        print("Launching 'Create NFT sell offer' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"

        print(" - Get owner account information")
        owner_wallet, owner_address, owner_seed = get_wallet_info(context, "owner")

        if get_confirmation(f"Do you have an NFT already minted? If not, we can mint one for you"):
            print(" - Enter NFT information")
            question = [
                inquirer.Text('nft_id', message=f"Please enter the NFT ID")
            ]
            nftoken_id = str(inquirer.prompt(question, theme=GreenPassion())['nft_id'])

        else:
            print(f"     - Okay! Minting a new NFT")
            payload = ObjFactory.getObj(
                ObjType.nft_token_mint,
                account=owner_address,
                nftoken_taxon=0
            )
            response = sign_autofill_and_submit(context.client, payload, owner_wallet)
            print(f" - Verify if minting succeeded")
            if ResponseCode.success not in str(response):
                raise Exception(
                    "Expected response code was not received."
                    "\nExpected Code = '{}'."
                    "\nResponse received: '{}'".format(ResponseCode.success, response)
                )

            nfttokens = get_nft_tokens(context.client, owner_address)
            nftoken_id = nfttokens[-1]

        print(f" - Create a sell offer")
        payload = ObjFactory.getObj(
            ObjType.nf_token_create_offer,
            account=owner_address,
            nftoken_id=nftoken_id,
            amount=context.transferAmount,
            flags=1
        )
        response = sign_autofill_and_submit(context.client, payload, owner_wallet)

        print(f" - Verify if offer creation succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )

        print(" - Workflow Summary:")
        print(f"     - Owner Wallet Address: {owner_address}")
        print(f"     - Owner Wallet Seed: {owner_seed}")
        print(f"     - Owner Wallet Current Balance: {get_account_balance(context, owner_address)}")
        print(f"     - Minted NFT ID: {nftoken_id}")
        print(f"     - Created Offer ID: {get_token_offers_response(context.client, owner_address, token_id=nftoken_id)[0]}")

    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def accept_nft_sell_offer():
    try:
        print("Launching 'Create and accept NFT sell offer' workflow...")
        print(" - Verify if the network is accessible")
        context = init_context()
        assert context.client.is_open(), "Not able to gain access to the network using the WebSocket Python client"

        print(" - Get seller account information")
        buyer_wallet, buyer_address, buyer_seed = get_wallet_info(context, "buyer")

        print(" - Get sell offer information")
        question = [
            inquirer.Text('offer_id', message=f"Please enter the Sell Offer ID")
        ]
        offer_id = str(inquirer.prompt(question, theme=GreenPassion())['offer_id'])

        print(f" - Accept the sell offer")
        payload = ObjFactory.getObj(
            ObjType.nf_token_accept_offer,
            account=buyer_address,
            nftoken_sell_offer=offer_id
        )
        response = sign_autofill_and_submit(context.client, payload, buyer_wallet)

        print(f" - Verify if offer acceptance succeeded")
        if ResponseCode.success not in str(response):
            raise Exception(
                "Expected response code was not received."
                "\nExpected Code = '{}'."
                "\nResponse received: '{}'".format(ResponseCode.success, response)
            )

        print(" - Workflow Summary:")
        print(f"     - Buyer Wallet Address: {buyer_address}")
        print(f"     - Buyer Wallet Seed: {buyer_seed}")
        print(f"     - Accepted Sell Offer ID: {offer_id}")
    except Exception as e:
        print(f"An unexpected error has occurred. Details: \n{e}")


def get_wallet_info(context, account_type):
    if get_confirmation(f"Do you have the address and seed of the {account_type} account? "
                        f"If not, we can create for you with {constants.DEFAULT_ACCOUNT_FUND_AMOUNT} XRP drops"):
        wallet = get_existing_wallet_info(context, account_type)
    else:
        print(f"     - Okay! Generating a new {account_type} wallet")
        wallet = Wallet.create(crypto_algorithm=context.crypto_algorithm)
        send_payment(context,
                     source_wallet=context.test_genesis_wallet,
                     destination_wallet=wallet,
                     amount=constants.DEFAULT_ACCOUNT_FUND_AMOUNT)

    address = wallet.classic_address
    seed = wallet.seed

    return wallet, address, seed


def get_existing_wallet_info(context, account_type):
    question = [
        inquirer.Text('seed', message=f"Please enter {account_type} account seed")
    ]
    seed = str(inquirer.prompt(question, theme=GreenPassion())['seed'])

    print(f"     - Got it! Generating {account_type} wallet using the provided information")
    wallet = Wallet(seed=seed, sequence=0, algorithm=context.crypto_algorithm)
    return wallet


def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
