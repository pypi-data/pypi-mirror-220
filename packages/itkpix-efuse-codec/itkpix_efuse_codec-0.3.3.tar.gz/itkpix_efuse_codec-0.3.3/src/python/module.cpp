#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;

#include "itkpix_efuse_codec.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

PYBIND11_MODULE(_itkpix_efuse_codec, m) {
    m.doc() = "Utilities for encoding and decoding data stored in the ITkPix ASIC efuses";

    m.def("encode", &itkpix_efuse_codec::encode,
        py::arg("probe_location"), py::arg("chip_sn")
    );

    m.def("decode", &itkpix_efuse_codec::decode,
        py::arg("efuse_data")
    );

    py::class_<itkpix_efuse_codec::EfuseData>(m, "EfuseData")
        .def(py::init<const uint32_t&>())
        .def(py::init<const std::string&>())
        .def("raw", &itkpix_efuse_codec::EfuseData::raw)
        .def("chip_sn", &itkpix_efuse_codec::EfuseData::chip_sn)
        .def("probe_location_id", &itkpix_efuse_codec::EfuseData::probe_location_id)
        .def("probe_location_name", &itkpix_efuse_codec::EfuseData::probe_location_name);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
} // module
