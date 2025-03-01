# Tests the degassing function works as expected

import VolFe as vf
import pandas as pd
import pytest


# tests to complete
# 2d closed regas
# 2d open regas

options = vf.default_models.copy()
options.loc["output csv", "option"] = False


def test_degas_df_default():
    "simple test of calc_gassing function using example 2a"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 4.17,  # wt%
        "CO2ppm": 1487.0,  # ppm
        "STppm": 1343.5,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    result = vf.calc_gassing(my_analysis, models=options)

    assert result.loc[0, "P_bar"] == pytest.approx(3774.7617761471683)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.4713653160583551)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(1472.3520719880657)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.00048209457695052205)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(-0.3715315657204652)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.0062436501019958925
    )
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(
        4.721772756477822e-05
    )


def test_degas_df_sat_sulf():
    "simple test of calc_gassing function with sulfur saturation using example 2a"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 4.17,  # wt%
        "CO2ppm": 1487.0,  # ppm
        "STppm": 1343.5,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # Choose the options I want to change for the calculation
    # - everything else will use the default options
    my_models = [["sulfur_saturation", "True"]]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(3762.539480458943)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.4711014824863762)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(1472.345721827803)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.00021903844348751043)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(
        -0.09301623162644468
    )
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.006395280169798468
    )
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(
        6.458729911225949e-06
    )


def test_degas_df_closed_CO2i():
    """simple test of calc_gassing function with closed-system degassing and initial CO2
    using example 2b"""

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 4.17,  # wt%
        "CO2ppm": 1487.0,  # ppm
        "STppm": 1343.5,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
        "initial_CO2wtpc": 4.0,
    }  # initial CO2 content of the system in wt%

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # choose the options I want - everything else will use the default options
    my_models = [["bulk_composition", "melt+vapor_initialCO2"], ["output csv", False]]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(3774.7617761471683)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.4713653160583551)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(1472.3520719880657)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.00048209457695052205)
    assert result.loc[len(result) - 1, "P_bar"] == 3.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(
        -0.31424700679099793
    )
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.33383038860830905
    )
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(
        0.0001096376822722297
    )


def test_degas_df_closed_wtg():
    """simple test of calc_gassing function with closed-system degassing and wtg using
    example 2b"""

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 4.17,  # wt%
        "CO2ppm": 1487.0,  # ppm
        "STppm": 1343.5,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
        "wt_g": 3.0,
    }  # wt% vapor in equilibrium with the melt

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # choose the options I want - everything else will use the default options
    my_models = [["bulk_composition", "melt+vapor_wtg"]]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(3774.7617761471683)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.4713653160583551)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(1472.3520719880657)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.00048209457695052205)
    assert result.loc[len(result) - 1, "P_bar"] == 2.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(
        -0.33980240602253176
    )
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.16490071166490516
    )
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(
        8.329271540222744e-05
    )


def test_degas_df_open():
    """simple test of calc_gassing function for open-system degassing using example 2c
    but with lower initial volatile content for speed"""

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 1.0,  # wt%
        "CO2ppm": 50.0,  # ppm
        "STppm": 100,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # choose the options I want - everything else will use the default options
    my_models = [["gassing_style", "open"], ["output csv", False]]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(197.13967305154458)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.38675667256337576)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(49.39514201474989)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.00011917735128162983)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(0.41711812367376133)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == 0.0
    assert result.loc[len(result) - 1, "xgS2_mf"] == 0.0


def test_regas_df_closed():
    "simple test of calc_gassing function for closed-system regassing using example 2d"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 4.17,  # wt%
        "CO2ppm": 1487,  # ppm
        "STppm": 1343.5,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
        "initial_CO2wtpc": 3.0,  # initial CO2 content of the system in wt%
        "final_P": 5000.0,
    }  # bar

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # choose the options I want - everything else will use the default options
    my_models = [
        ["gassing_direction", "regas"],
        ["bulk_composition", "melt+vapor_initialCO2"],
        ["output csv", False],
    ]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(3774.7617761471683)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.4713653160583551)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(1472.3520719880657)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.00048209457695052205)
    assert result.loc[len(result) - 1, "P_bar"] == 5100.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(0.456896945446573)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(2406.1752529769747)
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(
        0.0004136844111072347
    )


def test_regas_df_open():
    """simple test of calc_gassing function for open-system regassing using example 2d
    but to 4000 bar to save time"""

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 4.17,  # wt%
        "CO2ppm": 1487,  # ppm
        "STppm": 1343.5,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
        "initial_CO2wtpc": 3.0,  # initial CO2 content of the system in wt%
        "final_P": 4000.0,
    }  # bar

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # choose the options I want - everything else will use the default options
    my_models = [
        ["gassing_direction", "regas"],
        ["gassing_style", "open"],
        ["output csv", False],
    ]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(3774.7617761471683)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.4713653160583551)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(1472.3520719880657)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.00048209457695052205)
    assert result.loc[len(result) - 1, "P_bar"] == 4001.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(0.46560619026030636)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(1635.0957630618632)
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(
        0.0004476919049765029
    )


def test_degas_df_CHOAr_basalt():
    "simple test of calc_gassing function for CHOAr system in basalt using example 2e"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 2.0,  # wt%
        "CO2ppm": 500.0,  # ppm
        "STppm": 0.0,  # ppm
        "Xppm": 10.0,  # ppm <<< treating this as Ar
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    result = vf.calc_gassing(my_analysis, models=options)

    assert result.loc[0, "P_bar"] == pytest.approx(1432.8626980758336)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.417655396610054)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(494.37243543199065)
    assert result.loc[0, "xgX_mf"] == pytest.approx(0.08734713083466868)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(0.5808125442618355)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.004933477939764058
    )
    assert result.loc[len(result) - 1, "xgX_mf"] == pytest.approx(
        0.00024074332275451124
    )


def test_degas_df_CHONe_basalt():
    "simple test of calc_gassing function for CHONe system in basalt using example 2e"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 2.0,  # wt%
        "CO2ppm": 500.0,  # ppm
        "STppm": 0.0,  # ppm
        "Xppm": 10.0,  # ppm <<< treating this as Ar
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # choose the options I want - everything else will use the default options
    my_models = [
        ["species X", "Ne"],
        ["species X solubility", "Ne_Basalt_HughesIP"],
        ["output csv", False],
    ]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    # run calculation
    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(1378.1248030980487)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.41632410629870975)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(494.3570945815046)
    assert result.loc[0, "xgX_mf"] == pytest.approx(0.04824625574741737)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(0.5807041443952983)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.0049322249176338455
    )
    assert result.loc[len(result) - 1, "xgX_mf"] == pytest.approx(
        0.00047645662193990696
    )


def test_degas_df_CHOAr_rhyolite():
    "simple test of calc_gassing function for CHOAr system in rhyolite using example 2e"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 2.0,  # wt%
        "CO2ppm": 500.0,  # ppm
        "STppm": 0.0,  # ppm
        "Xppm": 10.0,  # ppm <<< treating this as Ar
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    # choose the options I want - everything else will use the default options
    my_models = [
        ["species X solubility", "Ar_Rhyolite_HughesIP"],
        ["output csv", False],
    ]

    # turn to dataframe with correct column headers and indexes
    my_models = vf.make_df_and_add_model_defaults(my_models)

    result = vf.calc_gassing(my_analysis, models=my_models)

    assert result.loc[0, "P_bar"] == pytest.approx(1337.3034231690124)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.41532902481154554)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(494.3456125370773)
    assert result.loc[0, "xgX_mf"] == pytest.approx(0.01699485123085667)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(0.5806225288411904)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.004931281928233859
    )
    assert result.loc[len(result) - 1, "xgX_mf"] == pytest.approx(
        0.00024063541075409293
    )


def test_degas_df_HSO():
    "simple test of calc_gassing function for HSO system using example 2e"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 2.0,  # wt%
        "CO2ppm": 0.0,  # ppm
        "STppm": 1000.0,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    result = vf.calc_gassing(my_analysis, models=options)

    assert result.loc[0, "P_bar"] == pytest.approx(380.16027020784526)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.39144451230686617)
    assert result.loc[0, "CO2T_ppmw"] == 0.0
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.0055645408964144945)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(-0.3838932210138193)
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == 0.0
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(
        0.00012487825695314437
    )


def test_degas_df_CSO():
    "simple test of calc_gassing function for CSO system using example 2e"

    my_analysis = {
        "Sample": "Sari15-04-33",
        "T_C": 1200.0,  # Temperature in 'C
        "SiO2": 47.89,  # wt%
        "TiO2": 0.75,  # wt%
        "Al2O3": 16.74,  # wt%
        "FeOT": 9.43,  # wt%
        "MnO": 0.18,  # wt%
        "MgO": 5.92,  # wt%
        "CaO": 11.58,  # wt%
        "Na2O": 2.14,  # wt%
        "K2O": 0.63,  # wt%
        "P2O5": 0.17,  # wt%
        "H2O": 0.0,  # wt%
        "CO2ppm": 500.0,  # ppm
        "STppm": 1000.0,  # ppm
        "Xppm": 0.0,  # ppm
        "Fe3FeT": 0.177,
    }

    my_analysis = pd.DataFrame(my_analysis, index=[0])

    result = vf.calc_gassing(my_analysis, models=options)

    assert result.loc[0, "P_bar"] == pytest.approx(1048.549372410781)
    assert result.loc[0, "fO2_DFMQ"] == pytest.approx(0.4082351490266145)
    assert result.loc[0, "CO2T_ppmw"] == pytest.approx(494.1488684153764)
    assert result.loc[0, "xgS2_mf"] == pytest.approx(0.0019195490893958809)
    assert result.loc[len(result) - 1, "P_bar"] == 1.0
    assert result.loc[len(result) - 1, "fO2_DFMQ"] == pytest.approx(
        -0.32400927886842723
    )
    assert result.loc[len(result) - 1, "CO2T_ppmw"] == pytest.approx(
        0.15829899800303915
    )
    assert result.loc[len(result) - 1, "xgS2_mf"] == pytest.approx(0.045219820386032165)
