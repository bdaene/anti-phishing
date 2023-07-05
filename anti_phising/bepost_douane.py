# This script targets the phishing site "https://bepost-douane.com"
import asyncio
import logging
import random

import httpx

from anti_phising.utils import NAMES_DATA, gen_cc_number, load_names

_logger = logging.getLogger(__name__)
BASE_URL = "https://bepost-douane.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://bepost-douane.com/soul.php',
    'Origin': 'https://bepost-douane.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}


def gen_response_parameters(first_name, last_name):
    cc_number = gen_cc_number()
    cc_number = '+'.join(cc_number[i * 4:i * 4 + 4] for i in range(4))

    parameters = dict(
        step='card',
        titulaire=f"{first_name} {last_name}",
        ccc=cc_number,
        exp=f"{random.randint(1, 12):02}%2F{random.randint(23, 28):02}",
        cvc=f"{random.randint(000, 999):03}",
    )
    return '&'.join(f"{key}={parameter}" for key, parameter in parameters.items())


async def send_request(first_name, last_name):
    parameters = gen_response_parameters(first_name, last_name)

    async with httpx.AsyncClient() as client:
        client.headers = HEADERS
        # Get cookies
        await client.get(BASE_URL)
        await client.post(f"{BASE_URL}/set/send.php", data=parameters)


async def send_requests(first_names, last_names, n=1000):
    first_names = random.choices(**first_names, k=n)
    last_names = random.choices(**last_names, k=n)

    await asyncio.gather(*(send_request(first_name, last_name)
                           for first_name, last_name in zip(first_names, last_names)))


def main():
    logging.basicConfig(level=logging.DEBUG)

    first_names = load_names(NAMES_DATA['first_names'])
    last_names = load_names(NAMES_DATA['last_names'])

    asyncio.run(send_requests(first_names, last_names, n=1))


if __name__ == '__main__':
    main()
