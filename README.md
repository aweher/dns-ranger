# DNS-RANGER

This project is a set of python scripts used to help DNS operators to understand some usage of their servers, It is based on Scapy, a tool written in Python. 

## Technologies Used

- Python 3
- Scapy
- yaml
- json
- threading
- time
- tqdm

## Installation

```bash
# clone the repository
git clone https://github.com/aweher/dns-ranger.git
cd dns-ranger
cp config.yaml.example config.yaml

# now edit the config.yaml file
vim config.yaml

# it is recommended to create a python virtual environment to run this
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

To run the tool, use the following command:

```bash
python3 %script%.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[TBD]

## Contact

If you want to contact me you can reach me at <ariel[at]weher.net>.

## Project status

The project is in development. Future updates are planned to improve the functionality and performance of the tool.

## Acknowledgements

This project uses the following open-source packages:

- [Scapy](https://scapy.net/)
- [PyYAML](https://pyyaml.org/)
- [tqdm](https://tqdm.github.io/)
