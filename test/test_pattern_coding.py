import numpy as np
import CommDspy as cdsp


def coding_gray_test(constellation):
    """
    :param constellation: Enumeration stating the constellation. Should be taken from:
                          CommDspy.constants.ConstellationEnum
    :return:
    """
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    levels = cdsp.get_levels(constellation)
    assert levels.any() is not None, 'Constellation ' + constellation.name + ' type not supported'
    bits = int(np.log2(len(levels)))
    pattern = np.random.randint(0, 2 ** bits, 100)
    assert_str = '|{0:^6s}| bits = {1:1d} Falied!!!!'.format( constellation.name, bits)
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut = cdsp.tx.coding_gray(pattern, constellation)
    # ==================================================================================================================
    # Computing the coding in a different way
    # ==================================================================================================================
    coded_ref = pattern
    if bits == 2:
        coded_temp = pattern.copy()
        coded_temp[pattern == 3] = 2
        coded_temp[pattern == 2] = 3
        coded_ref = coded_temp
    assert np.all(coded_ref == coded_dut), assert_str

def decoding_gray_test(constellation):
    """
    :param constellation: Enumeration stating the constellation. Should be taken from:
                          CommDspy.constants.ConstellationEnum
    :return:
    """
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    levels = cdsp.get_levels(constellation)
    assert levels.any() is not None, 'Constellation ' + constellation.name + ' type not supported'
    bits    = int(np.log2(len(levels)))
    pattern = np.random.randint(0, 2 ** bits, 100)
    assert_str = '|{0:^6s}| bits = {1:1d} Falied!!!!'.format(constellation.name, bits)
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut   = cdsp.tx.coding_gray(pattern, constellation)
    decoded_dut = cdsp.rx.decoding_gray(coded_dut, constellation)
    assert np.all(pattern == decoded_dut), assert_str

def coding_differential_test(constellation):
    """
    :param constellation: Enumeration stating the constellation. Should be taken from:
                          CommDspy.constants.ConstellationEnum
    :return:
    """
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    levels = cdsp.get_levels(constellation)
    assert levels.any() is not None, 'Constellation ' + constellation.name + ' type not supported'
    bits = int(np.log2(len(levels)))
    pattern = np.random.randint(0, 2 ** bits, 100)
    assert_str = '|{0:^6s}| bits = {1:1d} Falied!!!!'.format(constellation.name, bits)
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut = cdsp.tx.coding_differential(pattern, constellation)
    # ==================================================================================================================
    # Computing the coding in a different way
    # ==================================================================================================================
    coded_ref = np.zeros_like(pattern)
    init_symbol = 0
    for ii, symbol in enumerate(pattern):
        coded_ref[ii] = int((init_symbol + symbol) % len(levels))
        init_symbol = coded_ref[ii]
    assert np.all(coded_ref == coded_dut), assert_str

def decoding_differential_test(constellation):
    """
    :param constellation: Enumeration stating the constellation. Should be taken from:
                          CommDspy.constants.ConstellationEnum
    :return:
    """
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    levels = cdsp.get_levels(constellation)
    assert levels.any() is not None, 'Constellation ' + constellation.name + ' type not supported'
    bits = int(np.log2(len(levels)))
    pattern = np.random.randint(0, 2 ** bits, 100)
    assert_str = '|{0:^6s}| bits = {1:1d} Falied!!!!'.format(constellation.name, bits)
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut = cdsp.tx.coding_differential(pattern, constellation)
    decoded_dut = cdsp.rx.decoding_differential(coded_dut, constellation)
    assert np.all(pattern == decoded_dut), assert_str

def coding_manchester_test():
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    pattern = np.random.randint(0, 2 , [100, 3])
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut = cdsp.tx.coding_manchester(pattern)
    # ==================================================================================================================
    # Computing the coding in a different way
    # ==================================================================================================================
    coded_ref = np.zeros(600)
    for ii, symbol in enumerate(np.reshape(pattern, -1)):
        coded_ref[2*ii]     = symbol
        coded_ref[2*ii + 1] = 1 - symbol
    coded_ref = np.reshape(coded_ref, [100, 6])
    assert np.all(coded_ref == coded_dut), 'Manchester encoding failed!'

def decoding_manchester_test():
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    pattern = np.random.randint(0, 2, 100)
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut = cdsp.tx.coding_manchester(pattern)
    decoded_dut = cdsp.rx.decoding_manchester(coded_dut)
    assert np.all(pattern == decoded_dut), 'Manchester decoding failed!'

def coding_bipolar_test():
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    pattern = np.random.randint(0, 2, [100, 3])
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut = cdsp.tx.coding_bipolar(pattern)
    # ==================================================================================================================
    # Computing the coding in a different way
    # ==================================================================================================================
    coded_ref = np.reshape(pattern, -1)
    running_sign = -1
    for ii, symbol in enumerate(coded_ref):
        if symbol == 1:
            coded_ref[ii] *= running_sign
            running_sign *= -1
    coded_ref = np.reshape(coded_ref, [100, 3])

    assert np.all(coded_ref == coded_dut), 'Bi-polar encoding failed!'

def decoding_bipolar_test():
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    pattern = np.random.randint(0, 2, 100)
    # ==================================================================================================================
    # Getting DUT coded pattern
    # ==================================================================================================================
    coded_dut = cdsp.tx.coding_bipolar(pattern)
    decoded_dut = cdsp.rx.decoding_bipolar(coded_dut, error_deterction=True)
    assert np.allclose(pattern, decoded_dut), 'Manchester decoding failed!'
