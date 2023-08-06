from numbers import Number
from typing import *

from rdkit import Chem
from rdkit.ML.Descriptors.MoleculeDescriptors import MolecularDescriptorCalculator

from ddbox.docking.vina import vina_docking
from ddbox.utils import json_to_pretty_str

from .descriptors import MOLECULE_DESCRIPTORS

TMoleculeDescriptor = TypeVar("TMoleculeDescriptor", bound="MoleculeDescriptor")


class MoleculeDescriptor:

    # https://datagrok.ai/help/domains/chem/descriptors

    BalabanJ: Number | str = None
    BertzCT: Number | str = None
    Chi0: Number | str = None
    Chi0n: Number | str = None
    Chi0v: Number | str = None
    Chi1: Number | str = None
    Chi1n: Number | str = None
    Chi1v: Number | str = None
    Chi2n: Number | str = None
    Chi2v: Number | str = None
    Chi3n: Number | str = None
    Chi3v: Number | str = None
    Chi4n: Number | str = None
    Chi4v: Number | str = None
    EState_VSA1: Number | str = None
    EState_VSA10: Number | str = None
    EState_VSA11: Number | str = None
    EState_VSA2: Number | str = None
    EState_VSA3: Number | str = None
    EState_VSA4: Number | str = None
    EState_VSA5: Number | str = None
    EState_VSA6: Number | str = None
    EState_VSA7: Number | str = None
    EState_VSA8: Number | str = None
    EState_VSA9: Number | str = None
    ExactMolWt: Number | str = None
    FpDensityMorgan1: Number | str = None
    FpDensityMorgan2: Number | str = None
    FpDensityMorgan3: Number | str = None
    FractionCSP3: Number | str = None
    HallKierAlpha: Number | str = None
    HeavyAtomCount: Number | str = None
    HeavyAtomMolWt: Number | str = None
    Ipc: Number | str = None
    Kappa1: Number | str = None
    Kappa2: Number | str = None
    Kappa3: Number | str = None
    LabuteASA: Number | str = None
    MaxAbsEStateIndex: Number | str = None
    MaxAbsPartialCharge: Number | str = None
    MaxEStateIndex: Number | str = None
    MaxPartialCharge: Number | str = None
    MinAbsEStateIndex: Number | str = None
    MinAbsPartialCharge: Number | str = None
    MinEStateIndex: Number | str = None
    MinPartialCharge: Number | str = None
    MolLogP: Number | str = None
    MolMR: Number | str = None
    MolWt: Number | str = None
    NHOHCount: Number | str = None
    NOCount: Number | str = None
    NumAliphaticCarbocycles: Number | str = None
    NumAliphaticHeterocycles: Number | str = None
    NumAliphaticRings: Number | str = None
    NumAromaticCarbocycles: Number | str = None
    NumAromaticHeterocycles: Number | str = None
    NumAromaticRings: Number | str = None
    NumHAcceptors: Number | str = None
    NumHDonors: Number | str = None
    NumHeteroatoms: Number | str = None
    NumRadicalElectrons: Number | str = None
    NumRotatableBonds: Number | str = None
    NumSaturatedCarbocycles: Number | str = None
    NumSaturatedHeterocycles: Number | str = None
    NumSaturatedRings: Number | str = None
    NumValenceElectrons: Number | str = None
    PEOE_VSA1: Number | str = None
    PEOE_VSA10: Number | str = None
    PEOE_VSA11: Number | str = None
    PEOE_VSA12: Number | str = None
    PEOE_VSA13: Number | str = None
    PEOE_VSA14: Number | str = None
    PEOE_VSA2: Number | str = None
    PEOE_VSA3: Number | str = None
    PEOE_VSA4: Number | str = None
    PEOE_VSA5: Number | str = None
    PEOE_VSA6: Number | str = None
    PEOE_VSA7: Number | str = None
    PEOE_VSA8: Number | str = None
    PEOE_VSA9: Number | str = None
    RingCount: Number | str = None
    SMR_VSA1: Number | str = None
    SMR_VSA10: Number | str = None
    SMR_VSA2: Number | str = None
    SMR_VSA3: Number | str = None
    SMR_VSA4: Number | str = None
    SMR_VSA5: Number | str = None
    SMR_VSA6: Number | str = None
    SMR_VSA7: Number | str = None
    SMR_VSA8: Number | str = None
    SMR_VSA9: Number | str = None
    SlogP_VSA1: Number | str = None
    SlogP_VSA10: Number | str = None
    SlogP_VSA11: Number | str = None
    SlogP_VSA12: Number | str = None
    SlogP_VSA2: Number | str = None
    SlogP_VSA3: Number | str = None
    SlogP_VSA4: Number | str = None
    SlogP_VSA5: Number | str = None
    SlogP_VSA6: Number | str = None
    SlogP_VSA7: Number | str = None
    SlogP_VSA8: Number | str = None
    SlogP_VSA9: Number | str = None
    TPSA: Number | str = None
    VSA_EState1: Number | str = None
    VSA_EState10: Number | str = None
    VSA_EState2: Number | str = None
    VSA_EState3: Number | str = None
    VSA_EState4: Number | str = None
    VSA_EState5: Number | str = None
    VSA_EState6: Number | str = None
    VSA_EState7: Number | str = None
    VSA_EState8: Number | str = None
    VSA_EState9: Number | str = None
    fr_Al_COO: Number | str = None
    fr_Al_OH: Number | str = None
    fr_Al_OH_noTert: Number | str = None
    fr_ArN: Number | str = None
    fr_Ar_COO: Number | str = None
    fr_Ar_N: Number | str = None
    fr_Ar_NH: Number | str = None
    fr_Ar_OH: Number | str = None
    fr_COO: Number | str = None
    fr_COO2: Number | str = None
    fr_C_O: Number | str = None
    fr_C_O_noCOO: Number | str = None
    fr_C_S: Number | str = None
    fr_HOCCN: Number | str = None
    fr_Imine: Number | str = None
    fr_NH0: Number | str = None
    fr_NH1: Number | str = None
    fr_NH2: Number | str = None
    fr_N_O: Number | str = None
    fr_Ndealkylation1: Number | str = None
    fr_Ndealkylation2: Number | str = None
    fr_Nhpyrrole: Number | str = None
    fr_SH: Number | str = None
    fr_aldehyde: Number | str = None
    fr_alkyl_carbamate: Number | str = None
    fr_alkyl_halide: Number | str = None
    fr_allylic_oxid: Number | str = None
    fr_amide: Number | str = None
    fr_amidine: Number | str = None
    fr_aniline: Number | str = None
    fr_aryl_methyl: Number | str = None
    fr_azide: Number | str = None
    fr_azo: Number | str = None
    fr_barbitur: Number | str = None
    fr_benzene: Number | str = None
    fr_benzodiazepine: Number | str = None
    fr_bicyclic: Number | str = None
    fr_diazo: Number | str = None
    fr_dihydropyridine: Number | str = None
    fr_epoxide: Number | str = None
    fr_ester: Number | str = None
    fr_ether: Number | str = None
    fr_furan: Number | str = None
    fr_guanido: Number | str = None
    fr_halogen: Number | str = None
    fr_hdrzine: Number | str = None
    fr_hdrzone: Number | str = None
    fr_imidazole: Number | str = None
    fr_imide: Number | str = None
    fr_isocyan: Number | str = None
    fr_isothiocyan: Number | str = None
    fr_ketone: Number | str = None
    fr_ketone_Topliss: Number | str = None
    fr_lactam: Number | str = None
    fr_lactone: Number | str = None
    fr_methoxy: Number | str = None
    fr_morpholine: Number | str = None
    fr_nitrile: Number | str = None
    fr_nitro: Number | str = None
    fr_nitro_arom: Number | str = None
    fr_nitro_arom_nonortho: Number | str = None
    fr_nitroso: Number | str = None
    fr_oxazole: Number | str = None
    fr_oxime: Number | str = None
    fr_para_hydroxylation: Number | str = None
    fr_phenol: Number | str = None
    fr_phenol_noOrthoHbond: Number | str = None
    fr_phos_acid: Number | str = None
    fr_phos_ester: Number | str = None
    fr_piperdine: Number | str = None
    fr_piperzine: Number | str = None
    fr_priamide: Number | str = None
    fr_prisulfonamd: Number | str = None
    fr_pyridine: Number | str = None
    fr_quatN: Number | str = None
    fr_sulfide: Number | str = None
    fr_sulfonamd: Number | str = None
    fr_sulfone: Number | str = None
    fr_term_acetylene: Number | str = None
    fr_tetrazole: Number | str = None
    fr_thiazole: Number | str = None
    fr_thiocyan: Number | str = None
    fr_thiophene: Number | str = None
    fr_unbrch_alkane: Number | str = None
    fr_urea: Number | str = None
    qed: Number | str = None

    def __init__(self) -> None:
        pass

    def _to_json_data(self) -> Mapping[str, Any]:
        return {descriptor: self.__getattribute__(descriptor) for descriptor in MOLECULE_DESCRIPTORS}


TMolecule = TypeVar("TMolecule", bound="Molecule")


class Molecule:

    _inchi_key: str = None
    _inchi: str = None
    _smiles: str = None

    mol: Chem.rdchem.Mol
    desciptor: MoleculeDescriptor
    is_fetched: bool = False

    def __init__(self) -> None:
        self.desciptor = MoleculeDescriptor()

    @property
    def inchi_key(self) -> str:
        if self.is_valid:
            return Chem.MolToInchiKey(self.mol)
        return self._inchi_key

    @property
    def inchi(self) -> str:
        if self.is_valid:
            return Chem.MolToInchi(self.mol)
        return self._inchi

    @property
    def smiles(self) -> str:
        if self.is_valid:
            return Chem.MolToSmiles(self.mol)
        return self._smiles

    @property
    def is_valid(self) -> str:
        if self.mol is not None:
            try:
                Chem.SanitizeMol(self.mol)
                return True
            except ValueError:
                pass
        return False

    def dock(self, receptor_id, center: Tuple[float, float, float] | None = None, size: Tuple[float, float, float] | None = None):
        output_path = vina_docking(receptor_id, self.smiles, center, size)
        with open(output_path, 'r', encoding='utf-8') as f:
            output = f.read()
        return output

    def _fetch_descriptors(self) -> TMolecule:
        if self.is_valid:
            mol_descriptor_calculator = MolecularDescriptorCalculator(MOLECULE_DESCRIPTORS)
            values = list(mol_descriptor_calculator.CalcDescriptors(self.mol))
            for index in range(len(MOLECULE_DESCRIPTORS)):
                self.desciptor.__setattr__(MOLECULE_DESCRIPTORS[index], values[index])
        return self

    def _override_data(self):
        self._inchi_key = self.inchi_key
        self._inchi = self.inchi
        self._smiles = self.smiles
        self._fetch_descriptors()

    @staticmethod
    def from_inchi(inchi) -> TMolecule:
        molecule = Molecule()
        molecule._inchi = inchi
        molecule.mol = Chem.MolFromInchi(inchi)
        molecule._override_data()
        return molecule

    @staticmethod
    def from_smiles(smiles) -> TMolecule:
        molecule = Molecule()
        molecule._smiles = smiles
        molecule.mol = Chem.MolFromSmiles(smiles)
        molecule._override_data()
        return molecule

    def __getitem__(self, key):
        if hasattr(self.desciptor, key):
            return getattr(self.desciptor, key)
        return self.__getattribute__(key)

    def __str__(self) -> str:
        data = {
            'inchi_key': self.inchi_key,
            'inchi': self.inchi,
            'smiles': self.smiles,
            'descriptors': self.desciptor._to_json_data()
        }
        return json_to_pretty_str(data)
