// std/stl
#include <iostream>
#include <cstdint>

// efuse-codec
#include "itkpix_efuse_codec.h"

int main(int argc, char* argv[]) {

    namespace efuse = itkpix_efuse_codec;

    std::string encoded_efuse_binary_str = efuse::encode("BONN", 0x146cb);
    std::cout << "efuse (binary)        : " << encoded_efuse_binary_str << " (n-bits = " << encoded_efuse_binary_str.length() << ")" << std::endl;

    uint32_t encoded_efuse_data = std::stoul(encoded_efuse_binary_str, 0, 2);
    std::cout << "efuse (hex)           : 0x" << std::hex << encoded_efuse_data << std::endl;


    std::cout << "---" << std::endl;
    std::string decoded_efuse_binary_str  = efuse::decode(encoded_efuse_data);
    std::cout << "decoded_efuse_binary_str = " << decoded_efuse_binary_str << " (n-bits = " << std::dec << decoded_efuse_binary_str.length() << ")" << std::endl;
    efuse::EfuseData decoded{decoded_efuse_binary_str};
    std::cout << "Decoded:" << std::endl;
    std::cout << "  raw: 0x" << std::hex << decoded.raw() << std::endl;
    std::cout << "  sn : 0x" << std::hex << decoded.chip_sn() << std::endl;
    std::cout << "  pl : 0x" << std::hex << decoded.probe_location_id() << " (name=" << decoded.probe_location_name() << ")" << std::endl;
    return 0;
}
