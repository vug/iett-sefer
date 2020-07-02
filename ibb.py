"""
Simple API to interact with wdsl dataset about bus system
provided by Istanbul Municipality (IBB).
"""
from dataclasses import dataclass
import json
from pprint import pprint
from typing import List

from zeep import Client


class Clients(object):
    WSDL_DURAK = "https://api.ibb.gov.tr/iett/UlasimAnaVeri/HatDurakGuzergah.asmx?wsdl"
    WSDL_DUYURU = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"
    WSDL_SEFER = "https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl"
    WSDL_DETAY = "https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl"

    DURAK = Client(WSDL_DURAK)
    SEFER = Client(WSDL_SEFER)


def fetch(client, method_name, **kwargs):
    func = getattr(client.service, method_name)
    result = func(**kwargs)
    return json.loads(result)


def get_all_garajlar():
    return fetch(Clients.DURAK, "GetGaraj_json")


def get_all_duraklar():
    return fetch(Clients.DURAK, "GetDurak_json", DurakKodu="")


def get_durak(DurakKodu: str):
    return fetch(Clients.DURAK, "GetDurak_json", DurakKodu=DurakKodu)[0]


@dataclass
class AracKonum:
    Boylam: float
    Enlem: float
    Garaj: str
    Hiz: int
    KapiNo: str
    Operator: str
    Plaka: str
    Saat: str


def get_arac_konum() -> List[AracKonum]:
    konumlar_dict = fetch(Clients.SEFER, "GetFiloAracKonum_json")

    def dict_to_dataclass(d):
        ak = AracKonum(
            Boylam=float(d["Boylam"]),
            Enlem=float(d["Enlem"]),
            Garaj=d["Garaj"],
            Hiz=int(d["Hiz"]),
            KapiNo=d["KapiNo"],
            Operator=d["Operator"],
            Plaka=d["Plaka"],
            Saat=d["Saat"],
        )
        return ak

    return [dict_to_dataclass(k) for k in konumlar_dict]


def examples():
    """API usage examples."""
    garajlar = get_all_garajlar()
    pprint(garajlar[:3])

    duraklar = get_all_duraklar()
    pprint(duraklar[:3])

    durak = get_durak(DurakKodu="225981")
    pprint(durak)

    konumlar = get_arac_konum()
    pprint(konumlar)

    # durak_type = Clients.DURAK.get_type("ns0:GetDurak_jsonResult")
    # no types available

    import pickle

    with open("konumlar.pkl", "rb") as f:
        konums = pickle.load(f)
    coords = [(float(k["Boylam"]), float(k["Enlem"])) for k in konums]

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    x, y = zip(*coords)
    ax.scatter(x, y, s=1)
    plt.show()
