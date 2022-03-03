import numpy as np
import random
import csv
import os
import test
from CommDspy.constants import PrbsEnum, ConstellationEnum, CodingEnum
import CommDspy as cdsp

prbs_types      = [PrbsEnum.PRBS7, PrbsEnum.PRBS9, PrbsEnum.PRBS11, PrbsEnum.PRBS13, PrbsEnum.PRBS15]
constellations  = [ConstellationEnum.OOK, ConstellationEnum.NRZ, ConstellationEnum.PAM4]
codings         = [CodingEnum.UNCODED, CodingEnum.GRAY]

def test_prbs_analisys():
    """
    :return: Testing both the prbs_ana and the prbs_ana_econ
    """
    loss_th = 10
    for prbs_type in prbs_types:
        test.prbs_analysis_test(prbs_type, loss_th, lock_th=15)

def test_lock_pattern_to_signal_1():
    """
    :return:Testing the locking of the pattern on a signal length of 2 PRBS cycles with a small amount of errors
    """
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    bits_per_symbol = 2
    p_err           = 1e-4
    for prbs_type in prbs_types:
        pattern_length = 2 ** prbs_type.value - 1
        # ----------------------------------------------------------------------------------------------------------
        # Generating pattern
        # ----------------------------------------------------------------------------------------------------------
        poly_coeff = cdsp.get_polynomial(prbs_type)
        init_seed  = np.array([1] * prbs_type.value)
        prbs_seq, _ = cdsp.prbs_gen(poly_coeff, init_seed, pattern_length,
                                    bits_per_symbol=bits_per_symbol,
                                    bit_order_inv=False,
                                    pn_inv=False)
        # ----------------------------------------------------------------------------------------------------------
        # Injecting aerror to signal
        # ----------------------------------------------------------------------------------------------------------
        signal = np.tile(prbs_seq, 2)
        prob = np.random.random(signal.shape)
        signal[prob < p_err] = 1 - signal[prob < p_err]
        # ----------------------------------------------------------------------------------------------------------
        # Shifting the pattern and checking
        # ----------------------------------------------------------------------------------------------------------
        shift_idx = random.randint(0, len(prbs_seq))
        pattern = np.concatenate((prbs_seq[shift_idx:], prbs_seq[:shift_idx]))
        test.lock_pattern_to_signal_test(pattern, signal, shift_idx)

def test_lock_pattern_to_signal_2():
    """
    :return:Testing the locking of the pattern on a signal length of 2 PRBS cycles with a small amount of errors
    """
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    bits_per_symbol = 2
    p_err           = 1e-4
    for prbs_type in prbs_types:
        pattern_length = 2 ** prbs_type.value - 1
        # ----------------------------------------------------------------------------------------------------------
        # Generating pattern
        # ----------------------------------------------------------------------------------------------------------
        poly_coeff = cdsp.get_polynomial(prbs_type)
        init_seed  = np.array([1] * prbs_type.value)
        prbs_seq, _ = cdsp.prbs_gen(poly_coeff, init_seed, pattern_length,
                                    bits_per_symbol=bits_per_symbol,
                                    bit_order_inv=False,
                                    pn_inv=False)
        # ----------------------------------------------------------------------------------------------------------
        # Injecting aerror to signal
        # ----------------------------------------------------------------------------------------------------------
        signal = prbs_seq
        prob = np.random.random(signal.shape)
        signal[prob < p_err] = 1 - signal[prob < p_err]
        # ----------------------------------------------------------------------------------------------------------
        # Shifting the pattern and checking
        # ----------------------------------------------------------------------------------------------------------
        shift_idx = random.randint(0, len(prbs_seq))
        pattern = np.concatenate((prbs_seq[shift_idx:], prbs_seq[:shift_idx]))
        test.lock_pattern_to_signal_test(pattern, signal, shift_idx)

def test_lock_pattern_to_signal_3():
    """
    :return:Testing the locking of the pattern on a signal length of 2 PRBS cycles with a small amount of errors
    """
    # ==================================================================================================================
    # Local variables
    # ==================================================================================================================
    bits_per_symbol = 2
    p_err           = 1e-4
    for prbs_type in prbs_types:
        pattern_length = 2 ** prbs_type.value - 1
        # ----------------------------------------------------------------------------------------------------------
        # Generating pattern
        # ----------------------------------------------------------------------------------------------------------
        poly_coeff = cdsp.get_polynomial(prbs_type)
        init_seed  = np.array([1] * prbs_type.value)
        prbs_seq, _ = cdsp.prbs_gen(poly_coeff, init_seed, pattern_length,
                                    bits_per_symbol=bits_per_symbol,
                                    bit_order_inv=False,
                                    pn_inv=False)
        # ----------------------------------------------------------------------------------------------------------
        # Injecting error to signal
        # ----------------------------------------------------------------------------------------------------------
        cutoff_idx = random.randint(int(len(prbs_seq) / 4), int(len(prbs_seq) * 3 / 4))
        signal = prbs_seq[:cutoff_idx]
        prob = np.random.random(signal.shape)
        signal[prob < p_err] = 1 - signal[prob < p_err]
        # ----------------------------------------------------------------------------------------------------------
        # Shifting the pattern and checking
        # ----------------------------------------------------------------------------------------------------------
        shift_idx = random.randint(0, len(prbs_seq))
        pattern = np.concatenate((prbs_seq[shift_idx:], prbs_seq[:shift_idx]))
        test.lock_pattern_to_signal_test(pattern, signal, shift_idx)

def test_lock_pattern_to_signal_binary_1():
    """
    :return:Testing the locking of the pattern on a signal length of 2 PRBS cycles with a small amount of errors
    """
    p_err = 1e-4
    for prbs_type in prbs_types:
        # ----------------------------------------------------------------------------------------------------------
        # Loading pattern
        # ----------------------------------------------------------------------------------------------------------
        ref_filename = os.path.join(os.getcwd(), 'test_data', prbs_type.name + '_seed_ones.csv')
        with open(ref_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            ref_prbs_bin = np.array(next(reader)).astype(int)
        # ----------------------------------------------------------------------------------------------------------
        # Injecting aerror to signal
        # ----------------------------------------------------------------------------------------------------------
        signal    = np.tile(ref_prbs_bin, 2)
        prob      = np.random.random(signal.shape)
        signal[prob < p_err] = 1 - signal[prob < p_err]
        # ----------------------------------------------------------------------------------------------------------
        # Shifting the pattern and checking
        # ----------------------------------------------------------------------------------------------------------
        shift_idx = random.randint(0, len(ref_prbs_bin))
        pattern   = np.concatenate((ref_prbs_bin[shift_idx:], ref_prbs_bin[:shift_idx]))
        test.lock_pattern_to_signal_binary_test(pattern, signal, shift_idx)

def test_lock_pattern_to_signal_binary_2():
    """
    :return:Testing the locking of the pattern on a signal length of 1 PRBS cycles with a small amount of errors
    """
    p_err = 1e-4
    for prbs_type in prbs_types:
        # ----------------------------------------------------------------------------------------------------------
        # Loading pattern
        # ----------------------------------------------------------------------------------------------------------
        ref_filename = os.path.join(os.getcwd(), 'test_data', prbs_type.name + '_seed_ones.csv')
        with open(ref_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            ref_prbs_bin = np.array(next(reader)).astype(int)
        # ----------------------------------------------------------------------------------------------------------
        # Injecting aerror to signal
        # ----------------------------------------------------------------------------------------------------------
        signal = ref_prbs_bin
        prob = np.random.random(signal.shape)
        signal[prob < p_err] = 1 - signal[prob < p_err]
        # ----------------------------------------------------------------------------------------------------------
        # Shifting the pattern and checking
        # ----------------------------------------------------------------------------------------------------------
        shift_idx = random.randint(0, len(ref_prbs_bin))
        pattern = np.concatenate((ref_prbs_bin[shift_idx:], ref_prbs_bin[:shift_idx]))
        test.lock_pattern_to_signal_binary_test(pattern, signal, shift_idx)

def test_lock_pattern_to_signal_binary_3():
    """
    :return:Testing the locking of the pattern on a signal length of less than 1 PRBS cycles with a small amount of errors
    """
    p_err = 1e-4
    for prbs_type in prbs_types:
        # ----------------------------------------------------------------------------------------------------------
        # Loading pattern
        # ----------------------------------------------------------------------------------------------------------
        ref_filename = os.path.join(os.getcwd(), 'test_data', prbs_type.name + '_seed_ones.csv')
        with open(ref_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            ref_prbs_bin = np.array(next(reader)).astype(int)
        # ----------------------------------------------------------------------------------------------------------
        # Injecting error to signal
        # ----------------------------------------------------------------------------------------------------------
        cutoff_idx = random.randint(int(len(ref_prbs_bin)/4), int(len(ref_prbs_bin)*3/4))
        signal = ref_prbs_bin[:cutoff_idx]
        prob = np.random.random(signal.shape)
        signal[prob < p_err] = 1 - signal[prob < p_err]
        # ----------------------------------------------------------------------------------------------------------
        # Shifting the pattern and checking
        # ----------------------------------------------------------------------------------------------------------
        shift_idx = random.randint(0, len(ref_prbs_bin))
        pattern = np.concatenate((ref_prbs_bin[shift_idx:], ref_prbs_bin[:shift_idx]))
        test.lock_pattern_to_signal_binary_test(pattern, signal, shift_idx)

def test_prbs_gen_1():
    """
    :return: Testing the generation of all PRBS values except PRBS 31 in all constellations for 1 complete pattern
    generation
    """
    # ==============================================================================================================
    # Partial length PRBS generator tests
    # ==============================================================================================================
    for prbs_type in prbs_types:
        pattern_length = 2 ** prbs_type.value - 1
        for bits_per_symbol in [1, 2]:
            test.prbs_gen_test(prbs_type, pattern_length, bits_per_symbol, False, False)

def test_prbs_gen_2():
    """
    :return: Testing the generation of all PRBS values except PRBS 31 in all constellations for 1 partial pattern length
    """
    # ==============================================================================================================
    # Partial length PRBS generator tests
    # ==============================================================================================================
    for prbs_type in prbs_types:
        pattern_length = 2 ** prbs_type.value - 1
        required_length = random.randint(0, pattern_length)
        for bits_per_symbol in [1, 2]:
            test.prbs_gen_test(prbs_type, required_length, bits_per_symbol, False, False)

def test_prbs_gen_3():
    """
    :return: Testing the generation of all PRBS values except PRBS 31 in all constellations for 1 full pattern and
             another partial length
    """
    # ==============================================================================================================
    # Partial length PRBS generator tests
    # ==============================================================================================================
    for prbs_type in prbs_types:
        pattern_length = 2 ** prbs_type.value - 1
        required_length = random.randint(pattern_length+1, 2*pattern_length)
        for bits_per_symbol in [1, 2]:
            test.prbs_gen_test(prbs_type, required_length, bits_per_symbol, False, False)

def test_coding_1():
    """
    :return: Testing the coding function
    """
    pattern_2bit = np.array([0, 1, 2, 3, 0, 0, 1, 1, 2, 2, 3, 3, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])
    pattern_1bit = np.array([0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1])
    # ==================================================================================================================
    # 2 bit PAM4 test
    # ==================================================================================================================
    coded_2bit_pam4          = np.array([-3,-1,1,3,-3,-3,-1,-1,1,1,3,3,-3,-3,-3,-1,-1,-1,1,1,1,3,3,3])
    coded_2bit_pam4_gray     = np.array([-3,-1,3,1,-3,-3,-1,-1,3,3,1,1,-3,-3,-3,-1,-1,-1,3,3,3,1,1,1])
    coded_2bit_pam4_inv      = -1 * coded_2bit_pam4
    coded_2bit_pam4_gray_inv = -1 * coded_2bit_pam4_gray
    assert np.all(coded_2bit_pam4 == cdsp.code_pattern(pattern_2bit, ConstellationEnum.PAM4, CodingEnum.UNCODED, False)), 'PAM4 UNCODED '
    assert np.all(coded_2bit_pam4_gray == cdsp.code_pattern(pattern_2bit, ConstellationEnum.PAM4, CodingEnum.GRAY, False)), 'PAM4 GRAY '
    assert np.all(coded_2bit_pam4_inv == cdsp.code_pattern(pattern_2bit, ConstellationEnum.PAM4, CodingEnum.UNCODED, True)), 'PAM4 UNCODED inverted '
    assert np.all(coded_2bit_pam4_gray_inv == cdsp.code_pattern(pattern_2bit, ConstellationEnum.PAM4, CodingEnum.GRAY, True)), 'PAM4 GRAY inverted '
    # ==================================================================================================================
    # 1 bit PAM4 test
    # ==================================================================================================================
    coded_1bit_pam4          = np.array([-3,-1,-3,-1,-3,-3,-1,-1,-3,-1,-3,-3,-3,-1,-1,-1])
    coded_1bit_pam4_gray     = coded_1bit_pam4
    coded_1bit_pam4_inv      = -1 * coded_1bit_pam4
    coded_1bit_pam4_gray_inv = -1 * coded_1bit_pam4_gray
    assert np.all(coded_1bit_pam4 == cdsp.code_pattern(pattern_1bit, ConstellationEnum.PAM4, CodingEnum.UNCODED, False)), 'PAM4 UNCODED - 1 bit'
    assert np.all(coded_1bit_pam4_gray == cdsp.code_pattern(pattern_1bit, ConstellationEnum.PAM4, CodingEnum.GRAY, False)), 'PAM4 GRAY - 1 bit'
    assert np.all(coded_1bit_pam4_inv == cdsp.code_pattern(pattern_1bit, ConstellationEnum.PAM4, CodingEnum.UNCODED, True)), 'PAM4 UNCODED inverted - 1 bit'
    assert np.all(coded_1bit_pam4_gray_inv == cdsp.code_pattern(pattern_1bit, ConstellationEnum.PAM4, CodingEnum.GRAY, True)), 'PAM4 GRAY inverted - 1 bit'
    # ==================================================================================================================
    # 1 bit NRZ test
    # ==================================================================================================================
    coded_1bit_nrz      = coded_1bit_pam4 + 2
    coded_1bit_nrz_gray = coded_1bit_nrz
    coded_1bit_nrz_inv  = -1 * coded_1bit_nrz
    coded_1bit_nrz_gray_inv = -1 * coded_1bit_nrz_gray
    assert np.all(coded_1bit_nrz == cdsp.code_pattern(pattern_1bit, ConstellationEnum.NRZ, CodingEnum.UNCODED, False)), 'NRZ UNCODED'
    assert np.all(coded_1bit_nrz_gray == cdsp.code_pattern(pattern_1bit, ConstellationEnum.NRZ, CodingEnum.GRAY, False)), 'NRZ GRAY'
    assert np.all(coded_1bit_nrz_inv == cdsp.code_pattern(pattern_1bit, ConstellationEnum.NRZ, CodingEnum.UNCODED, True)), 'NRZ UNCODED inverted'
    assert np.all(coded_1bit_nrz_gray_inv == cdsp.code_pattern(pattern_1bit, ConstellationEnum.NRZ, CodingEnum.GRAY, True)), 'NRZ GRAY inverted'
    # ==================================================================================================================
    # 1 bit OOK test
    # ==================================================================================================================
    coded_1bit_ook          = (coded_1bit_nrz + 1) / 2
    coded_1bit_ook_gray     = coded_1bit_ook
    coded_1bit_ook_inv      = -1 * coded_1bit_ook
    coded_1bit_ook_gray_inv = -1 * coded_1bit_ook
    assert np.all(coded_1bit_ook == cdsp.code_pattern(pattern_1bit, ConstellationEnum.OOK, CodingEnum.UNCODED, False)), 'OOK UNCODED'
    assert np.all(coded_1bit_ook_gray == cdsp.code_pattern(pattern_1bit, ConstellationEnum.OOK, CodingEnum.GRAY, False)), 'OOK GRAY'
    assert np.all(coded_1bit_ook_inv == cdsp.code_pattern(pattern_1bit, ConstellationEnum.OOK, CodingEnum.UNCODED, True)), 'OOK UNCODED inverted'
    assert np.all(coded_1bit_ook_gray_inv == cdsp.code_pattern(pattern_1bit, ConstellationEnum.OOK, CodingEnum.GRAY, True)), 'OOK GRAY inverted'

def test_coding_2():
    """
    :return: Test the coding function with random arrays across all constellations and codings
    """
    for coding in codings:
        for constellation in constellations:
            for pn_inv in [True, False]:
                test.coding_pattern_test(constellation, coding, pn_inv)

if __name__ == '__main__':
    test_prbs_analisys()