import numpy as np
import pandas as pd
import math

import pprint

import shutil
import urllib.request as request
from contextlib import closing
import xmltodict

from obspy.clients.fdsn import Client

inv_client = Client("IRIS")

import logging

logger = logging.getLogger(__name__)


class GtsmMetadata:
    def __init__(self, network, fcid, gauge_weights=None):
        self.network = network
        self.fcid = fcid
        self.meta_df = self.get_meta_table()
        self.latitude = self.get_latitude()
        self.longitude = self.get_longitude()
        self.elevation = self.get_elevation()
        self.gap = self.get_gap()
        self.diameter = 0.087
        self.orientation = self.get_orientation()
        self.linearization = self.get_linearization_params()
        matrices = {}
        if not gauge_weights:
            self.gauge_weights = [1, 1, 1, 1]
        # matrices['weighted_strain_matrix'] = self.make_weighted_strain_matrix(gauge_weights=gauge_weights)
        matrices["lab_strain_matrix"] = self.get_lab_strain_matrix()
        matrices["er2010_strain_matrix"] = self.get_er2010_strain_matrix()
        matrices["ch_prelim_strain_matrix"] = self.get_ch_prelim_strain_matrix()
        self.strain_matrices = {k: v for k, v in matrices.items() if v is not None}
        self.atmp_response = self.get_atmp_response()
        self.tidal_params = self.get_tidal_params()

    #        self.xml = self.get_xml()
    #        self.detrend = self.get_detrend_xml()

    def get_xml(self):
        metadir = "../xml/"
        xml_path = "ftp://bsm.unavco.org/pub/bsm/level2/" + self.fcid + "/"
        xml_file = self.fcid + ".xml"
        with closing(request.urlopen(xml_path + xml_file)) as r:
            with open(metadir + xml_file, "wb") as f:
                shutil.copyfileobj(r, f)
        return xmltodict.parse(open(metadir + xml_file).read(), process_namespaces=True)

    def get_meta_table(self):
        url = "https://www.unavco.org/data/strain-seismic/bsm-data/lib/docs/bsm_metadata.txt"
        meta_df = pd.read_csv(url, sep="\s+", index_col="BNUM")
        return meta_df

    def get_latitude(self):
        try:
            lats = self.meta_df["LAT"]
            return float(lats[self.fcid])
        except:
            logger.info("no latitude found")
            exit(1)

    def get_longitude(self):
        try:
            longs = self.meta_df["LONG"]
            return float(longs[self.fcid])
        except:
            logger.info("no longitude found")
            exit(1)

    def get_elevation(self):
        try:
            elevations = self.meta_df["ELEV(m)"]
            return float(elevations[self.fcid])
        except:
            logger.info("no elevation found")
            exit(1)

    def get_gap(self):
        try:
            gaps = self.meta_df["GAP(m)"]
            return float(gaps[self.fcid])
        except:
            logger.info("no gap found for %s, using .0001" % self.fcid)
            return 0.0001

    def get_orientation(self):
        try:
            orientations = self.meta_df["CH0(EofN)"]
            return float(orientations[self.fcid])
        except Exception as e:
            logger.error(e)
            logger.error("No orientation found for %s, using 0 deg" % self.fcid)
            return 0

    def get_orientation_xml(self):
        for i, dic in enumerate(
            self.xml["strain_xml"]["inst_info"]["sensor_information"]["sensor_response"]
        ):
            if dic["sensor_type"] == "Gladwin_BSM_component_1_":
                orientation = float(
                    self.xml["strain_xml"]["inst_info"]["sensor_information"][
                        "sensor_response"
                    ][i]["orientation"]["#text"]
                )
        try:
            return orientation
        except Exception as e:
            logger.error(e)
            logger.error("No orientation found for %s, using 0 deg" % self.fcid)
            return 0

    def make_weighted_strain_matrix(self, gauge_weights=[1, 1, 1, 1]):
        # make strain matrix from manufacturers coefficients
        # logger.info(gauge_weights)
        c = 1.5
        d = 3
        scale_factors = np.array([[c, 0, 0], [0, d, 0], [0, 0, d]])
        gage_weights = np.array(
            [
                [gauge_weights[0], 0, 0, 0],
                [0, gauge_weights[1], 0, 0],
                [0, 0, gauge_weights[2], 0],
                [0, 0, 0, gauge_weights[3]],
            ]
        )
        orientations = np.array(
            [
                [
                    0.5,
                    0.5 * math.cos(math.radians(2 * (90 - self.orientation))),
                    0.5 * math.sin(math.radians(2 * (90 - self.orientation))),
                ],
                [
                    0.5,
                    0.5 * math.cos(math.radians(2 * (-30 - self.orientation))),
                    0.5 * math.sin(math.radians(2 * (-30 - self.orientation))),
                ],
                [
                    0.5,
                    0.5 * math.cos(math.radians(2 * (-150 - self.orientation))),
                    0.5 * math.sin(math.radians(2 * (-150 - self.orientation))),
                ],
                [
                    0.5,
                    0.5 * math.cos(math.radians(2 * (-120 - self.orientation))),
                    0.5 * math.sin(math.radians(2 * (-120 - self.orientation))),
                ],
            ]
        )

        # remove row from orientation matrix corresponding to gage weight of 0
        orientations = np.matmul(gage_weights, orientations)
        orientations = orientations[~np.all(orientations == 0, axis=1)]
        # scale gage_weights down to 3x3 identity if only using 3 gages
        gage_weights = gage_weights[:, ~np.all(gage_weights == 0, axis=0)]
        gage_weights = gage_weights[~np.all(gage_weights == 0, axis=1)]

        # calculate the strain matrix
        strain_matrix = np.matmul(
            np.matmul(np.linalg.inv(scale_factors), np.linalg.pinv(orientations)),
            np.linalg.inv(gage_weights),
        )

        # insert a column of zeros back in if one gage was dropped, leaving a 4x3 matrix
        for i in [0, 1, 2, 3]:
            if gauge_weights[i] == 0:
                strain_matrix = np.insert(strain_matrix, i, 0, axis=1)
        # print("strain_matrix: \n",strain_matrix)
        return strain_matrix

    def get_lab_strain_matrix(self):
        try:
            url = f"http://bsm.unavco.org/bsm/level2/{self.fcid}/{self.fcid}.README.txt"

            with request.urlopen(url) as response:
                lines = response.readlines()
            for i, line in enumerate(lines):
                line = line.decode("utf-8").rstrip()
                if line.startswith("  Manufacturer's Isotropic Strain Matrix"):
                    lab = np.array(
                        [
                            lines[i + 1].decode("utf-8").rstrip().split()[1:],
                            lines[i + 2].decode("utf-8").rstrip().split()[1:],
                            lines[i + 3].decode("utf-8").rstrip().split()[1:],
                        ]
                    )
            return lab.astype(float)
        except Exception as e:
            logger.error("Could not load lab strain matrix")
            return None

    def get_er2010_strain_matrix(self):
        url = f"http://bsm.unavco.org/bsm/level2/{self.fcid}/{self.fcid}.README.txt"
        try:
            with request.urlopen(url) as response:
                lines = response.readlines()
            for i, line in enumerate(lines):
                line = line.decode("utf-8").rstrip()
                if line.startswith("  Roeloffs 2010 Tidal Calibration"):
                    er2010 = np.array(
                        [
                            lines[i + 3].decode("utf-8").rstrip().split()[1:],
                            lines[i + 4].decode("utf-8").rstrip().split()[1:],
                            lines[i + 5].decode("utf-8").rstrip().split()[1:],
                        ]
                    )
                    return er2010.astype(float)
        except Exception as e:
            logger.error("Could not load ER2010 strain matrix")
            return None

    def get_ch_prelim_strain_matrix(self):
        url = f"http://bsm.unavco.org/bsm/level2/{self.fcid}/{self.fcid}.README.txt"
        try:
            with request.urlopen(url) as response:
                lines = response.readlines()
            for i, line in enumerate(lines):
                line = line.decode("utf-8").rstrip()
                if line.startswith("  CH Preliminary Tidal Calibration"):
                    ch_prelim = np.array(
                        [
                            lines[i + 3].decode("utf-8").rstrip().split()[1:],
                            lines[i + 4].decode("utf-8").rstrip().split()[1:],
                            lines[i + 5].decode("utf-8").rstrip().split()[1:],
                        ]
                    )
                    return ch_prelim.astype(float)
            return np.array([])
        except Exception as e:
            logger.error("Could not load ch_prelim strain matrix")
            return None

    def get_linearization_params(self):
        linearization = {}
        linearization["linear_date"] = self.meta_df.loc[self.fcid]["L_DATE"]
        linearization["CH0"] = int(self.meta_df.loc[self.fcid]["L0(cnts)"])
        linearization["CH1"] = int(self.meta_df.loc[self.fcid]["L1(cnts)"])
        linearization["CH2"] = int(self.meta_df.loc[self.fcid]["L2(cnts)"])
        linearization["CH3"] = int(self.meta_df.loc[self.fcid]["L3(cnts)"])
        return linearization

    def get_linearization_params_xml(self):
        # get reference strains from xml
        linear_dict = self.xml["strain_xml"]["inst_info"]["processing"][
            "bsm_processing_history"
        ][-1]["bsm_processing"]["linearization"]
        self.linearization = {}
        for key in linear_dict:
            # print(key, linear_dict[key])
            if key == "linear_date":
                self.linearization["linear_date"] = linear_dict[key]
            if key == "g0_value":
                self.linearization["CH0"] = float(linear_dict[key])
            if key == "g1_value":
                self.linearization["CH1"] = float(linear_dict[key])
            if key == "g2_value":
                self.linearization["CH2"] = float(linear_dict[key])
            if key == "g3_value":
                self.linearization["CH3"] = float(linear_dict[key])

    def get_gauge_weightings_xml(self):
        weight_dict = self.xml["strain_xml"]["inst_info"]["processing"][
            "bsm_processing_history"
        ][-1]["bsm_processing"]["gauge_weightings"]
        self.gauge_weightings = [
            int(weight_dict["gw0"]),
            int(weight_dict["gw1"]),
            int(weight_dict["gw2"]),
            int(weight_dict["gw3"]),
        ]

    def get_detrend_xml(self):
        detrend = {}
        for channel in [
            "detrend_start_date",
            "detrend_g0",
            "detrend_g1",
            "detrend_g2",
            "detrend_g3",
        ]:
            if channel == "detrend_start_date":
                detrend[channel] = self.xml["strain_xml"]["inst_info"]["processing"][
                    "bsm_processing_history"
                ][-1]["bsm_processing"]["timeseries_start_date"]
            else:
                detrend_dict = {}
                detrend_params = self.xml["strain_xml"]["inst_info"]["processing"][
                    "bsm_processing_history"
                ][-1]["bsm_processing"][channel]
                for key in detrend_params:
                    if key[0] != "@":
                        detrend_dict[key] = float(detrend_params[key])
                detrend[channel] = detrend_dict
        return detrend

    def get_atmp_response(self):
        url = f"http://bsm.unavco.org/bsm/level2/{self.fcid}/{self.fcid}.README.txt"
        try:
            with request.urlopen(url) as response:
                lines = response.readlines()
            baro = False
            atmp_coefficients = {}
            for line in lines:
                line = line.decode("utf-8").rstrip()
                if line.startswith("Barometric Response"):
                    baro = True
                if baro:
                    if line.startswith("CH"):
                        line = line.split()
                        atmp_coefficients[line[0]] = (
                            float(line[1]) * 1e-3
                        )  # microstrain
                        if line[0] == "CH3":
                            baro = False
            return atmp_coefficients
        except Exception as e:
            logger.error("Could not load atmp response")
            return None

    def get_tidal_params(self):
        url = f"http://bsm.unavco.org/bsm/level2/{self.fcid}/{self.fcid}.README.txt"
        try:
            with request.urlopen(url) as response:
                lines = response.readlines()
            tide = False
            tide_coefficients = {}
            for line in lines:
                line = line.decode("utf-8").rstrip()

                if line.startswith("Tidal Constituents"):
                    tide = True

                if tide:
                    if line.startswith("CH"):
                        line = line.split()
                        if line[1] == "M2":
                            doodson = "2 0 0 0 0 0"
                        elif line[1] == "O1":
                            doodson = "1-1 0 0 0 0"
                        elif line[1] == "P1":
                            doodson = "1 1-2 0 0 0"
                        elif line[1] == "K1":
                            doodson = "1 1 0 0 0 0"
                        elif line[1] == "N2":
                            doodson = "2-1 0 1 0 0"
                        elif line[1] == "S2":
                            doodson = "2 2-2 0 0 0"
                        tide_coefficients[(line[0], line[1], "phz")] = line[2]
                        tide_coefficients[(line[0], line[1], "amp")] = line[3]
                        tide_coefficients[(line[0], line[1], "doodson")] = doodson
            return tide_coefficients
        except Exception as e:
            logger.error("Could not load tidal parameters")
            return None

    def show(self):
        # pp = pprint.PrettyPrinter()
        logger.info(f"network: {self.network}")
        logger.info(f"fcid: {self.fcid}")
        logger.info(f"latitude: {self.latitude}")
        logger.info(f"longitude: {self.longitude}")
        logger.info(f"gap: {self.gap}")
        logger.info(f"orientation (CH0EofN): {self.orientation}")
        logger.info(f"reference strains:\n {self.linearization}")
        # logger.info(self.linearization)
        if len(self.strain_matrices):
            for key in self.strain_matrices:
                logger.info(f"{key}:\n {self.strain_matrices[key]}")
                # logger.info(self.strain_matrices[key])
                # pp.pprint(self.strain_matrices[key])
        logger.info(f"atmp coefficients:\n {self.atmp_response}")
        # logger.info(self.atmp_response)
        logger.info(f"tidal params:\n {self.tidal_params}")
        # logger.info(self.tidal_params)

        # print("reference strains:")
        # pp.pprint(self.linearization)
        # if len(self.strain_matrices):
        #     for key in self.strain_matrices:
        #         print(f"{key}:")
        #         print(self.strain_matrices[key])
        #         #pp.pprint(self.strain_matrices[key])
        # print("atmp coefficients:")
        # pp.pprint(self.atmp_response)
        # print("tidal params: ")
        # pp.pprint(self.tidal_params)
        # print("detrend params:")
        # pp.pprint(self.detrend)


# def bottlename2fdsn(bottlename):
#     '''
#     convert bottlename to location and channel
#     :param bottlename: str
#     :return: location: str, channel: str
#     '''
#     codes = {"BatteryVolts": ["T0", "RE1"], "CH0": ["T0", "RS1"], "CH1": ["T0", "RS2"], "CH2": ["T0", "RS3"],
#              "CH3": ["T0", "RS4"], "CalOffsetCH0G1": ["T1", "RCA"], "CalOffsetCH0G2": ["T2", "RCA"],
#              "CalOffsetCH0G3": ["T3", "RCA"], "CalOffsetCH1G1": ["T1", "RCB"], "CalOffsetCH1G2": ["T2", "RCB"],
#              "CalOffsetCH1G3": ["T3", "RCB"], "CalOffsetCH2G1": ["T1", "RCC"], "CalOffsetCH2G2": ["T2", "RCC"],
#              "CalOffsetCH2G3": ["T3", "RCC"], "CalOffsetCH3G1": ["T1", "RCD"], "CalOffsetCH3G2": ["T2", "RCD"],
#              "CalOffsetCH3G3": ["T3", "RCD"], "CalStepCH0G1": ["T4", "RCA"], "CalStepCH0G2": ["T5", "RCA"],
#              "CalStepCH0G3": ["T6", "RCA"], "CalStepCH1G1": ["T4", "RCB"], "CalStepCH1G2": ["T5", "RCB"],
#              "CalStepCH1G3": ["T6", "RCB"], "CalStepCH2G1": ["T4", "RCC"], "CalStepCH2G2": ["T5", "RCC"],
#              "CalStepCH2G3": ["T6", "RCC"], "CalStepCH3G1": ["T4", "RCD"], "CalStepCH3G2": ["T5", "RCD"],
#              "CalStepCH3G3": ["T6", "RCD"], "DownholeDegC": ["T0", "RKD"], "LoggerDegC": ["T0", "RK1"],
#              "PowerBoxDegC": ["T0", "RK2"], "PressureKPa": ["TS", "RDO"], "RTSettingCH0": ["T0", "RCA"],
#              "RTSettingCH1": ["T0", "RCB"], "RTSettingCH2": ["T0", "RCC"], "RTSettingCH3": ["T0", "RCD"],
#              "Rainfallmm": ["TS", "RRO"], "SolarAmps": ["T0", "REO"], "SystemAmps": ["T0", "RE2"],
#              "CalOffsetCH0G0": ["T7", "RCA"], "CalOffsetCH1G0": ["T7", "RCB"], "CalOffsetCH2G0": ["T7", "RCC"],
#              "CalOffsetCH3G0": ["T7", "RCD"], "CalStepCH0G0": ["T8", "RCA"], "CalStepCH1G0": ["T8", "RCB"],
#              "CalStepCH2G0": ["T8", "RCC"], "CalStepCH3G0": ["T8", "RCD"]}
#     location = codes[bottlename][0]
#     channel = codes[bottlename][1]
#     return location, channel


def fdsn2bottlename(channel):
    """
    convert location and channel into bottlename
    :param channel: str
    :return: str
    """
    codes = {
        "RS1": "CH0",
        "LS1": "CH0",
        "BS1": "CH0",
        "RS2": "CH1",
        "LS2": "CH1",
        "BS2": "CH1",
        "RS3": "CH2",
        "LS3": "CH2",
        "BS3": "CH2",
        "RS4": "CH3",
        "LS4": "CH3",
        "BS4": "CH3",
        "RDO": "atmp",
        "LDO": "atmp",
    }

    return codes[channel]
