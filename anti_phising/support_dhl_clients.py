# This script targets the phishing site "https://support-dhl-clients.com"
import asyncio
import logging
import random

import httpx

from anti_phising.utils import gen_cc_number

_logger = logging.getLogger(__name__)
BASE_URL = "https://support-dhl-clients.com"
ESPACE_CLIENT = f"{BASE_URL}/espace-client"
PHP_SESSION_IDS = (  # Could not find a way to bypass hcaptcha.
    'i210kdhtb4iaec498ep01nv0t6',
    'gvm7vho6of99g8crmgkmbbpt90',
    'm82dv9dhu17tahjte113sb74hp'
)


# https://support-dhl-clients.com/verify/index.php
# https://support-dhl-clients.com/index.php
# https://support-dhl-clients.com/espace-client/login.php?&enc=787d20b06a7c4cdf089539f32c5ab255
# https://support-dhl-clients.com/espace-client/erreur-livraison.php?787d20b06a7c4cdf089539f32c5ab255
# https://support-dhl-clients.com/espace-client/informations-utilisateur.php?787d20b06a7c4cdf089539f32c5ab255
# https://support-dhl-clients.com/espace-client/paiement-livraison.php?787d20b06a7c4cdf089539f32c5ab255
# https://support-dhl-clients.com/espace-client/authuser/card.php?787d20b06a7c4cdf089539f32c5ab255


async def send_request(client):
    # response = await client.get(f"{BASE_URL}/index.php", follow_redirects=False, timeout=100)
    # enc = response.next_request.url.params.get('enc', None)
    # logging.info(f"{enc=}")
    # if enc is None:
    #     logging.warning(f"PHPSESSID {client.cookies['PHPSESSID']} is not valid anymore.")
    #     return

    # for _ in range(5):
    #     response = await client.get(f"{ESPACE_CLIENT}/paiement-livraison.php?{enc}")
    #     if response.text != 'UNMADE PAGE':
    #         break
    #     await asyncio.sleep(0.1)
    # else:
    #     return

    card_parameters = dict(
        ccc=gen_cc_number(),
        exp=f"{random.randint(1, 12):02}%2F{random.randint(23, 28):02}",
        cvc=f"{random.randint(000, 999):03}",
    )
    # response = await client.post(f"{ESPACE_CLIENT}/authuser/card.php?{enc}", data=card_parameters)
    response = await client.post(f"{ESPACE_CLIENT}/authuser/card.php", data=card_parameters, timeout=60)

    print(response)


async def send_requests(php_session_id):
    async with httpx.AsyncClient() as client:
        # client.cookies['PHPSESSID'] = php_session_id
        await asyncio.gather(*(send_request(client) for _ in range(10)))


async def send_requests_for_all_sessions():
    await asyncio.gather(*(send_requests(php_session_id)
                           for php_session_id in PHP_SESSION_IDS))


def main():
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(send_requests_for_all_sessions())


if __name__ == '__main__':
    main()
