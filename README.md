
#Project Title
BanquePostale_AccountStatement

##Getting Started

Python script to download Bank account statements from french bank with a firefox instance (headless or live mode)

##Hardware:

    nRF5x series (nRF52832)
    LIS2DH serie (eg LIS2DHTR)

##Pinout:

    LIS2DHTR-SCL --> nRF52832-P0.10
    LIS2DHTR-SCA --> nRF52832-P0.09
    LIS2DHTR-ACC-INT1 --> nRF52832-P0.05
    LIS2DHTR-ACC-INT2 --> nRF52832-P0.06

##Installing

    for a quick demo, put this sketch in nRF5_SDK_15.0.0_a53641a\examples\peripheral[Your_Project]

##Main Functionality

##This firmware uses:

    INT1 PIN to wake up the MCU
    INT2 PIN to force sleep mode (after a defined duration)


##Authors

https://github.com/johnmarcc
