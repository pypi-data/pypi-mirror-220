# ITkPix E-fuse Codec

Utilities for encoding and decoding the data stored in the ITkPix ASIC e-fuses

# Installation

## Cpp

The `itkpix-efuse-codec` C++ library is header-only.
Simply add the [single_include/itkpix_efuse_codec/](single_include/itkpix_efuse_codec/)
directory to your project's include path and you should be able to
`#include "itkpix_efuse_codec.h`.

## Python

`itkpix-efuse-codec` is available on [PyPi](https://pypi.org/project/itkpix-efuse-codec/).
Simply run the following command to install:

```shell
pip install itkpix-efuse-codec
```

# Usage

## Python

### Command-line Utility

`pip` installing `itkpix-efuse-codec` givers you the `efuse` command-line utility, which has the `encode` and `decode` sub-commands.

#### encode

```verbatim
efuse -v encode BONN 0x146cb
Input:
   probe_location name  : BONN
   chip serial number   : 83659 (bin: 0b10100011011001011, hex: 0x146cb)
Encoded:
   encoded e-fuse (bin) : 00010001010001101100101100011111 (32 bits)
                  (hex) : 0x1146cb1f
```

#### decode

```
efuse -v decode 0x1146cb1f
Input:
    e-fuse data   (bin): 0b100010100011011001011
                  (hex): 0x1146cb
Decoded:
    chip serial number : 0x146cb
    probe location     : BONN (id: 0x1)
```

### As a module

You can import the `itkpix_efuse_codec` module in your existing Python scripts. For example,
to generate the 32-bit encoded E-fuse data you would do:

```python
import itkpix_efuse_codec

probe_location_name : str = "BONN" # must be a valid name
chip_sn : int = 0x12345;
efuse_binary_string = itkpix_efuse_codec.encode(probe_location_name, chip_sn) # returns binary string

efuse_data = int(efuse_binary_string, 2) # parse the binary string into an integer
```

To decode 32-bit E-fuse data retreived from the ITkPix ASIC, you would do:

```python
import itkpix_efuse_codec
from itkpix_efuse_codec import EfuseData

retrieved_efuse_data : int = ...
decoded_efuse_data = int(itkpix_efuse_codec.decode(retrieved_efuse_data), 2) # parse the binary string into an integer
efuse_data = EfuseData(decoded_efuse_data) # EfuseData class has useful getters

chip_sn = efuse_data.chip_sn()
probe_location_name = efuse_data.probe_location_name()
probe_location_id = efuse_data.probe_location_id()
```
