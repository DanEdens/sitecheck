"""
    Geo-Instruments
    Sitecheck Scanner
"""
# __name__ = '__main__'
# __author__ = "Dan Edens"
# __version__= "0.8.3.6"
# __url__= "https://geodev.geo-instruments.com/DanEdens/Sitecheck_Scanner"

import asyncio
import os

from sitecheck import Scanner


async def main():
    """Main Entry point for Scanner"""
    if os.environ['Reset'] == 'True':
        Scanner.enable_all_projects()
    if os.environ['Edit'] == 'True':
        Scanner.edit()
    await Scanner.Scan()


if __name__ == "__main__":
    """Prevents main from running automatically when imported"""
    if os.environ['Repl'] == 'True':
        Scanner.repl()
    else:
        asyncio.run(
            main()
            )
