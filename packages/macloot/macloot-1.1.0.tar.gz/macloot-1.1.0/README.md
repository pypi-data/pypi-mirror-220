# MAC Address Lookup and Transformation

This command line application allows you to lookup the **O**rganizationally **U**nique **I**dentifier (OUI) of MAC addresses, either from a file or from standard input (stdin). Additionally, it provides functionality to transform MAC addresses between different formats.

## Introduction

The **MAC** Address **Loo**kup and **T**ransformation (`macloot`) tool provides a convenient way to retrieve the **O**rganizationally **U**nique **I**dentifier (OUI) associated with a MAC address. It utilizes the IEEE OUI database to perform the lookup and offers options to process MAC addresses from a file or interactively through stdin.

### Supported formats
The `macloot` application is designed to effortlessly identify MAC addresses within any text input and parse them. Whether you have a large document, log files, or even user-provided input, the application intelligently scans the text to extract MAC addresses. This capability ensures that you can easily work with MAC addresses regardless of their context, simplifying the process of retrieving and manipulating these unique identifiers.

`macloot` accurately matches the most commonly used MAC addresses:
- `11:22:33:AA:BB:CC`
- `11-22-33-AA-BB-CC`
- `aa:bb:cc:dd:ee:ff`
- `aa-bb-cc-dd-ee-ff`
- `aaaa.bbbb.cccc`
- `AAAA.BBBB.CCCC`
- `112233AABBCC`
- `aabbccddeeff`

## Installation

Installing `macloot` is a breeze. Simply use the following command to install it via `pip`:
```bash
pip install macloot
```
No `sudo` is required for installing the application as it will be installed in your home directory.

The application does not include the OUI database by default but retrieves it from a trusted source (https://standards-oui.ieee.org/oui/oui.csv). Upon first run, it prompts you to download the latest version for up-to-date MAC address lookups. You have full control over initiating the download, ensuring data source approval.

## Basic Usage

To use the MAC Address Lookup and Transformation application, follow these steps:

1. Run the script with a MAC address file as input:

```bash
macloot path/to/mac_addresses.txt
```

2. Alternatively, provide MAC addresses through stdin:

```bash
macloot 00:11:22:33:44:55
```

3. Why not pipe (`|`) the output if `ifconfig` into the application:
```bash
ifconfig | macloot
```
4. Save the results from `arp -a` into a CSV file `arp.csv` using `;` as a delimiting character:
```bash
arp -a | macloot -o arp.csv -d ";"
```

The application will display the organization name associated with each MAC address found in the input.

## Advanced Usage

The MAC Address Lookup and Transformation application offers additional features and options:

### Format Transformation
To transform MAC addresses between formats, use the `-O` or `--octet-separator` argument followed by a hyphen `-`, a colon `:` or a dot `.` as the format specifier. This allows for convenient and quick conversion of MAC address formats.

#### Cisco style (using `-O .`)
To convert MAC addresses to Cisco's `aaaa.bbbb.cccc` format, use the following command:
```bash
macloot 24:16:1b:2c:3d:4e -O .
```
Output:
```bash
2416.1b2c.3d4e      Cisco Systems, Inc
```

#### Microsoft style (using `-O -`)
To convert MAC addresses to Microsoft's `AA-BB-CC-DD-EE-FF` format, use the following command:
```bash
macloot 1c1a.dfa1.b2c3 -O - -u
```
Output:
```bash
1C-1A-DF-A1-B2-C3   Microsoft Corporation
```

#### Linux style (using `-O :`)
To convert MAC addresses to Linux's `aa:bb:cc:dd:ee:ff` format, use the following command:
```bash
macloot 2c-c8-1b-a1-b2-c3 -O :
```
Output:
```bash
2c:c8:1b:a1:b2:c3   Routerboard.com
```

### Character Casing
To modify the character casing of MAC addresses in the output, you can utilize the `-l` or `--lowercase` and `-u` or `--uppercase` arguments. Using `-l` will convert the output MAC addresses to lowercase, while `-u` will convert them to uppercase.

If neither of these arguments is provided, the original casing of the input MAC addresses will be preserved in the output.

#### Uppercase
In this example we convert a MAC address in Cisco format to the format Microsoft uses (with hyphens, in **uppercase**) by using the `-u` argument:
```bash
macloot 1c1a.dfa1.b2c3 -O - -u
```
Output:
```bash
1C-1A-DF-A1-B2-C3   Microsoft Corporation
```

#### Lowercase
In this example we do the opposite, convert a MAC address in Microsoft format to the format Cisco uses (with dots, in **lowercase**) by using the `-l` argument:
```bash
macloot 24:16:1B:2C:3D:4E -O . -l
```
Output:
```bash
2416.1b2c.3d4e      Cisco Systems, Inc
```

### Search
To search for OUIs based on company names, you can utilize the `-s` or `--search` argument. By providing the desired company name as the argument value, such as "Cisco," "Apple," or "Microsoft," you can retrieve the corresponding OUIs associated with those companies. This feature enables easy lookup and identification of OUIs based on the names of specific organizations.

```bash
macloot -s microsoft
```
Output:
```bash
0003FF  Microsoft Corporation
000D3A  Microsoft Corporation
00125A  Microsoft Corporation
00155D  Microsoft Corporation
0017FA  Microsoft Corporation
... (output truncated) ...
```
To make the output compatible with CSV format, you can use the `-d ";"` option here as well. 
## Update OUI database
You can easily update the OUI database at any time by running the command: 
```bash
macloot --update-db
```
This command initiates the process of fetching the latest version of the OUI database, ensuring that you have the most recent information for accurate MAC address lookups. By offering a simple command to update the database, the application enables you to stay current with the evolving OUI data without any hassle.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please submit a GitHub [issue](https://github.com/bitcanon/macloot/issues) or a [pull request](https://github.com/bitcanon/macloot/pulls).

## License

This project is licensed under the [MIT License](LICENSE).
