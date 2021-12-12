"""Blocklist Generator

This script will take a blocklist.txt file and turn it into multiple different blocklist formats
"""

from typing import *
import os
import sys

# Universal header for all generated files
file_header = """
                    --- YouTube Ad Blocklist ---
This project was created and is maintained by: Evan Pratten (@ewpratten)
More information at: https://github.com/Ewpratten/youtube_ad_blocklist
"""


def generateIPV4Hosts(block_list: List[str]) -> List[str]:
    return [f"# {line}" for line in file_header.split("\n")]+[f"0.0.0.0 {entry}" for entry in block_list]

def generateIPV6Hosts(block_list: List[str]) -> List[str]:
    return [f"# {line}" for line in file_header.split("\n")]+[f"::/0 {entry}" for entry in block_list]

def generateDomainsList(block_list: List[str]) -> List[str]:
    return [f"# {line}" for line in file_header.split("\n")]+[entry for entry in block_list]

def generateDNSMASQList(block_list: List[str]) -> List[str]:
    return [f"# {line}" for line in file_header.split("\n")]+[f"server=/{entry}/" for entry in block_list]

def generateUnboundList(block_list: List[str]) -> List[str]:
    return [f"# {line}" for line in file_header.split("\n")]+[f"local-zone: \"{entry}\" redirect\nlocal-data: \"{entry} A 127.0.0.1\"" for entry in block_list]

def generateAdblockList(block_list: List[str]) -> List[str]:
    return ["[Adblock Plus 2.0]"]+[f"! {line}" for line in file_header.split("\n")]+["||{}^".format(entry) for entry in block_list]


# All generators
generator_list: dict = {
    "hosts.ipv4.txt": generateIPV4Hosts,
    "hosts.ipv6.txt": generateIPV6Hosts,
    "domains.txt": generateDomainsList,
    "dnsmasq.txt": generateDNSMASQList,
    "unbound.txt": generateUnboundList,
    "adblockplus.txt": generateAdblockList
}


def main() -> int:

    # Load the block list to a newline-seperated list
    entries = []
    with open("blocklist.txt", "r") as fp:
        entries = fp.read().split("\n")
        fp.close()

    # Filter empty lines
    entries = list(filter(None, entries))

    # Create the output dir
    os.makedirs("output", exist_ok=True)

    # Run every generator
    for gen in generator_list:
        print(f"Running generator: {gen}")
        with open(f"output/{gen}", "w") as fp:
            fp.write("\n".join(generator_list[gen](entries)))
            fp.close()


if __name__ == "__main__":
    sys.exit(main())
