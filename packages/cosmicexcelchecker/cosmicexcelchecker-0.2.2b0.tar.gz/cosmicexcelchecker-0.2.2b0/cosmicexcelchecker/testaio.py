import aiohttp
import asyncio

async def main(url):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://github.com'
    }

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return []

            l = resp.json()
            return l

# l = asyncio.run(main(url='https://raw.githubusercontent.com/Discord-AntiScam/scam-links/main/urls.json'))
# print(l)
# print(len(l))
# print(type(l))

import requests

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://github.com'
    }

resp = requests.get(url='https://raw.githubusercontent.com/Discord-AntiScam/scam-links/main/urls.json', headers=headers)
if resp.status_code == 200:
    lj = resp.json()
    print(len(lj), type(lj))
    print(lj)