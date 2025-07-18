# Auto generated from patient_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-05-30T11:00:40
# Schema: PatientSchema
#
# id: https://example.org/patient-schema
# description: Generated from data dictionary
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Float, String

metamodel_version = "1.7.0"
version = None

# Namespaces
EX = CurieNamespace('ex', 'https://example.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = EX


# Types

# Class references



@dataclass(repr=False)
class Patient(YAMLRoot):
    """
    Auto-generated class for patient
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Patient"]
    class_class_curie: ClassVar[str] = "ex:Patient"
    class_name: ClassVar[str] = "Patient"
    class_model_uri: ClassVar[URIRef] = EX.Patient

    subject_characteristics: Optional[Union[dict, "SubjectCharacteristics"]] = None
    timing: Optional[Union[dict, "Timing"]] = None
    family_medical_history: Optional[Union[dict, "FamilyMedicalHistory"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.subject_characteristics is not None and not isinstance(self.subject_characteristics, SubjectCharacteristics):
            self.subject_characteristics = SubjectCharacteristics(**as_dict(self.subject_characteristics))

        if self.timing is not None and not isinstance(self.timing, Timing):
            self.timing = Timing(**as_dict(self.timing))

        if self.family_medical_history is not None and not isinstance(self.family_medical_history, FamilyMedicalHistory):
            self.family_medical_history = FamilyMedicalHistory(**as_dict(self.family_medical_history))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SubjectCharacteristics(YAMLRoot):
    """
    subject_characteristics fields
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["SubjectCharacteristics"]
    class_class_curie: ClassVar[str] = "ex:SubjectCharacteristics"
    class_name: ClassVar[str] = "SubjectCharacteristics"
    class_model_uri: ClassVar[URIRef] = EX.SubjectCharacteristics

    HONEST_BROKER_SUBJECT_ID: Optional[str] = None
    DATA_CONTRIBUTOR_ID: Optional[Union[str, "DATACONTRIBUTORIDEnum"]] = None
    DATA_SOURCE: Optional[Union[str, "DATASOURCEEnum"]] = None
    LAST_KNOWN_SURVIVAL_STATUS: Optional[Union[str, "LASTKNOWNSURVIVALSTATUSEnum"]] = None
    AGE_LAST_CONTACT: Optional[float] = None
    AGE_LAST_CONTACT_UNIT: Optional[Union[str, "AGELASTCONTACTUNITEnum"]] = None
    AGE_LAST_CONTACT_PRECISION: Optional[Union[str, "AGELASTCONTACTPRECISIONEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.HONEST_BROKER_SUBJECT_ID is not None and not isinstance(self.HONEST_BROKER_SUBJECT_ID, str):
            self.HONEST_BROKER_SUBJECT_ID = str(self.HONEST_BROKER_SUBJECT_ID)

        if self.DATA_CONTRIBUTOR_ID is not None and not isinstance(self.DATA_CONTRIBUTOR_ID, DATACONTRIBUTORIDEnum):
            self.DATA_CONTRIBUTOR_ID = DATACONTRIBUTORIDEnum(self.DATA_CONTRIBUTOR_ID)

        if self.DATA_SOURCE is not None and not isinstance(self.DATA_SOURCE, DATASOURCEEnum):
            self.DATA_SOURCE = DATASOURCEEnum(self.DATA_SOURCE)

        if self.LAST_KNOWN_SURVIVAL_STATUS is not None and not isinstance(self.LAST_KNOWN_SURVIVAL_STATUS, LASTKNOWNSURVIVALSTATUSEnum):
            self.LAST_KNOWN_SURVIVAL_STATUS = LASTKNOWNSURVIVALSTATUSEnum(self.LAST_KNOWN_SURVIVAL_STATUS)

        if self.AGE_LAST_CONTACT is not None and not isinstance(self.AGE_LAST_CONTACT, float):
            self.AGE_LAST_CONTACT = float(self.AGE_LAST_CONTACT)

        if self.AGE_LAST_CONTACT_UNIT is not None and not isinstance(self.AGE_LAST_CONTACT_UNIT, AGELASTCONTACTUNITEnum):
            self.AGE_LAST_CONTACT_UNIT = AGELASTCONTACTUNITEnum(self.AGE_LAST_CONTACT_UNIT)

        if self.AGE_LAST_CONTACT_PRECISION is not None and not isinstance(self.AGE_LAST_CONTACT_PRECISION, AGELASTCONTACTPRECISIONEnum):
            self.AGE_LAST_CONTACT_PRECISION = AGELASTCONTACTPRECISIONEnum(self.AGE_LAST_CONTACT_PRECISION)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Timing(YAMLRoot):
    """
    timing fields
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Timing"]
    class_class_curie: ClassVar[str] = "ex:Timing"
    class_name: ClassVar[str] = "Timing"
    class_model_uri: ClassVar[URIRef] = EX.Timing

    HONEST_BROKER_SUBJECT_ID: Optional[str] = None
    TIMEPOINT: Optional[Union[str, "TIMEPOINTEnum"]] = None
    AGE_AT: Optional[float] = None
    AGE_UNIT: Optional[Union[str, "AGEUNITEnum"]] = None
    AGE_PRECISION: Optional[Union[str, "AGEPRECISIONEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.HONEST_BROKER_SUBJECT_ID is not None and not isinstance(self.HONEST_BROKER_SUBJECT_ID, str):
            self.HONEST_BROKER_SUBJECT_ID = str(self.HONEST_BROKER_SUBJECT_ID)

        if self.TIMEPOINT is not None and not isinstance(self.TIMEPOINT, TIMEPOINTEnum):
            self.TIMEPOINT = TIMEPOINTEnum(self.TIMEPOINT)

        if self.AGE_AT is not None and not isinstance(self.AGE_AT, float):
            self.AGE_AT = float(self.AGE_AT)

        if self.AGE_UNIT is not None and not isinstance(self.AGE_UNIT, AGEUNITEnum):
            self.AGE_UNIT = AGEUNITEnum(self.AGE_UNIT)

        if self.AGE_PRECISION is not None and not isinstance(self.AGE_PRECISION, AGEPRECISIONEnum):
            self.AGE_PRECISION = AGEPRECISIONEnum(self.AGE_PRECISION)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FamilyMedicalHistory(YAMLRoot):
    """
    family_medical_history fields
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["FamilyMedicalHistory"]
    class_class_curie: ClassVar[str] = "ex:FamilyMedicalHistory"
    class_name: ClassVar[str] = "FamilyMedicalHistory"
    class_model_uri: ClassVar[URIRef] = EX.FamilyMedicalHistory

    HONEST_BROKER_SUBJECT_ID: Optional[str] = None
    RELATION_HONEST_BROKER_SUBJECT_ID: Optional[str] = None
    RELATION: Optional[Union[str, "RELATIONEnum"]] = None
    CONDITION: Optional[Union[str, "CONDITIONEnum"]] = None
    SOURCE: Optional[Union[str, "SOURCEEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.HONEST_BROKER_SUBJECT_ID is not None and not isinstance(self.HONEST_BROKER_SUBJECT_ID, str):
            self.HONEST_BROKER_SUBJECT_ID = str(self.HONEST_BROKER_SUBJECT_ID)

        if self.RELATION_HONEST_BROKER_SUBJECT_ID is not None and not isinstance(self.RELATION_HONEST_BROKER_SUBJECT_ID, str):
            self.RELATION_HONEST_BROKER_SUBJECT_ID = str(self.RELATION_HONEST_BROKER_SUBJECT_ID)

        if self.RELATION is not None and not isinstance(self.RELATION, RELATIONEnum):
            self.RELATION = RELATIONEnum(self.RELATION)

        if self.CONDITION is not None and not isinstance(self.CONDITION, CONDITIONEnum):
            self.CONDITION = CONDITIONEnum(self.CONDITION)

        if self.SOURCE is not None and not isinstance(self.SOURCE, SOURCEEnum):
            self.SOURCE = SOURCEEnum(self.SOURCE)

        super().__post_init__(**kwargs)


# Enumerations
class DATACONTRIBUTORIDEnum(EnumDefinitionImpl):

    Baylor = PermissibleValue(text="Baylor")
    Indiana = PermissibleValue(text="Indiana")
    MGH = PermissibleValue(text="MGH")
    Maryland = PermissibleValue(text="Maryland")
    Michigan = PermissibleValue(text="Michigan")
    Nebraska = PermissibleValue(text="Nebraska")
    NorthShore = PermissibleValue(text="NorthShore")

    _defn = EnumDefinition(
        name="DATACONTRIBUTORIDEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "UChicago Monogenic Diabetes Research Group",
            PermissibleValue(text="UChicago Monogenic Diabetes Research Group"))
        setattr(cls, "Barbara Davis Center / UColorado",
            PermissibleValue(text="Barbara Davis Center / UColorado"))
        setattr(cls, "Boston Children's",
            PermissibleValue(text="Boston Children's"))

class DATASOURCEEnum(EnumDefinitionImpl):

    EHR = PermissibleValue(text="EHR")

    _defn = EnumDefinition(
        name="DATASOURCEEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Self-reported",
            PermissibleValue(text="Self-reported"))

class LASTKNOWNSURVIVALSTATUSEnum(EnumDefinitionImpl):

    Alive = PermissibleValue(
        text="Alive",
        description="Showing characteristics of life; displaying signs of life.")
    Dead = PermissibleValue(
        text="Dead",
        description="The cessation of life.")
    Unknown = PermissibleValue(
        text="Unknown",
        description="Reported as unknown by the data contributor.")

    _defn = EnumDefinition(
        name="LASTKNOWNSURVIVALSTATUSEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Not Reported",
            PermissibleValue(
                text="Not Reported",
                description="Not provided or available."))

class AGELASTCONTACTUNITEnum(EnumDefinitionImpl):

    Years = PermissibleValue(text="Years")
    Months = PermissibleValue(text="Months")
    Weeks = PermissibleValue(text="Weeks")
    Days = PermissibleValue(text="Days")

    _defn = EnumDefinition(
        name="AGELASTCONTACTUNITEnum",
    )

class AGELASTCONTACTPRECISIONEnum(EnumDefinitionImpl):

    Approximate = PermissibleValue(text="Approximate")
    Exact = PermissibleValue(text="Exact")

    _defn = EnumDefinition(
        name="AGELASTCONTACTPRECISIONEnum",
    )

class TIMEPOINTEnum(EnumDefinitionImpl):

    Diagnosis = PermissibleValue(text="Diagnosis")
    Relapse = PermissibleValue(text="Relapse")
    Remission = PermissibleValue(text="Remission")

    _defn = EnumDefinition(
        name="TIMEPOINTEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Prediabetes Diagnosis",
            PermissibleValue(text="Prediabetes Diagnosis"))

class AGEUNITEnum(EnumDefinitionImpl):

    Years = PermissibleValue(text="Years")
    Months = PermissibleValue(text="Months")
    Weeks = PermissibleValue(text="Weeks")
    Days = PermissibleValue(text="Days")

    _defn = EnumDefinition(
        name="AGEUNITEnum",
    )

class AGEPRECISIONEnum(EnumDefinitionImpl):

    Approximate = PermissibleValue(text="Approximate")
    Exact = PermissibleValue(text="Exact")

    _defn = EnumDefinition(
        name="AGEPRECISIONEnum",
    )

class RELATIONEnum(EnumDefinitionImpl):

    Father = PermissibleValue(text="Father")
    Mother = PermissibleValue(text="Mother")
    Son = PermissibleValue(text="Son")
    Daughter = PermissibleValue(text="Daughter")
    Brother = PermissibleValue(text="Brother")
    Sister = PermissibleValue(text="Sister")
    Niece = PermissibleValue(text="Niece")
    Nephew = PermissibleValue(text="Nephew")
    Other = PermissibleValue(text="Other")

    _defn = EnumDefinition(
        name="RELATIONEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Spouse/Partner",
            PermissibleValue(text="Spouse/Partner"))
        setattr(cls, "Grandfather (Paternal)",
            PermissibleValue(text="Grandfather (Paternal)"))
        setattr(cls, "Grandfather (Maternal)",
            PermissibleValue(text="Grandfather (Maternal)"))
        setattr(cls, "Grandmother (paternal)",
            PermissibleValue(text="Grandmother (paternal)"))
        setattr(cls, "Grandmother (maternal)",
            PermissibleValue(text="Grandmother (maternal)"))
        setattr(cls, "Uncle (paternal)",
            PermissibleValue(text="Uncle (paternal)"))
        setattr(cls, "Uncle (maternal)",
            PermissibleValue(text="Uncle (maternal)"))
        setattr(cls, "Aunt (paternal)",
            PermissibleValue(text="Aunt (paternal)"))
        setattr(cls, "Aunt (maternal)",
            PermissibleValue(text="Aunt (maternal)"))
        setattr(cls, "First cousin (paternal)",
            PermissibleValue(text="First cousin (paternal)"))
        setattr(cls, "First cousin (maternal)",
            PermissibleValue(text="First cousin (maternal)"))
        setattr(cls, "First cousin (pat/mat unknown)",
            PermissibleValue(text="First cousin (pat/mat unknown)"))
        setattr(cls, "Great-grandfather (paternal)",
            PermissibleValue(text="Great-grandfather (paternal)"))
        setattr(cls, "Great-grandfather (maternal)",
            PermissibleValue(text="Great-grandfather (maternal)"))
        setattr(cls, "Great-grandmother (paternal)",
            PermissibleValue(text="Great-grandmother (paternal)"))
        setattr(cls, "Great-grandmother (maternal)",
            PermissibleValue(text="Great-grandmother (maternal)"))
        setattr(cls, "Great-uncle (paternal)",
            PermissibleValue(text="Great-uncle (paternal)"))
        setattr(cls, "Great-uncle (maternal)",
            PermissibleValue(text="Great-uncle (maternal)"))
        setattr(cls, "Great-aunt (paternal)",
            PermissibleValue(text="Great-aunt (paternal)"))
        setattr(cls, "Great-aunt (maternal)",
            PermissibleValue(text="Great-aunt (maternal)"))

class CONDITIONEnum(EnumDefinitionImpl):

    Prediabetes = PermissibleValue(text="Prediabetes")

    _defn = EnumDefinition(
        name="CONDITIONEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Type 1 Diabetes",
            PermissibleValue(text="Type 1 Diabetes"))
        setattr(cls, "Type 2 Diabetes",
            PermissibleValue(text="Type 2 Diabetes"))
        setattr(cls, "Monogenic Diabetes",
            PermissibleValue(text="Monogenic Diabetes"))
        setattr(cls, "Gestational Diabetes",
            PermissibleValue(text="Gestational Diabetes"))
        setattr(cls, "Diabetes, NOS",
            PermissibleValue(text="Diabetes, NOS"))

class SOURCEEnum(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="SOURCEEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Confirmed by genetic test",
            PermissibleValue(text="Confirmed by genetic test"))
        setattr(cls, "Clinical diagnosis only",
            PermissibleValue(text="Clinical diagnosis only"))

# Slots
class slots:
    pass

slots.patient__subject_characteristics = Slot(uri=EX.subject_characteristics, name="patient__subject_characteristics", curie=EX.curie('subject_characteristics'),
                   model_uri=EX.patient__subject_characteristics, domain=None, range=Optional[Union[dict, SubjectCharacteristics]])

slots.patient__timing = Slot(uri=EX.timing, name="patient__timing", curie=EX.curie('timing'),
                   model_uri=EX.patient__timing, domain=None, range=Optional[Union[dict, Timing]])

slots.patient__family_medical_history = Slot(uri=EX.family_medical_history, name="patient__family_medical_history", curie=EX.curie('family_medical_history'),
                   model_uri=EX.patient__family_medical_history, domain=None, range=Optional[Union[dict, FamilyMedicalHistory]])

slots.subjectCharacteristics__HONEST_BROKER_SUBJECT_ID = Slot(uri=EX.HONEST_BROKER_SUBJECT_ID, name="subjectCharacteristics__HONEST_BROKER_SUBJECT_ID", curie=EX.curie('HONEST_BROKER_SUBJECT_ID'),
                   model_uri=EX.subjectCharacteristics__HONEST_BROKER_SUBJECT_ID, domain=None, range=Optional[str])

slots.subjectCharacteristics__DATA_CONTRIBUTOR_ID = Slot(uri=EX.DATA_CONTRIBUTOR_ID, name="subjectCharacteristics__DATA_CONTRIBUTOR_ID", curie=EX.curie('DATA_CONTRIBUTOR_ID'),
                   model_uri=EX.subjectCharacteristics__DATA_CONTRIBUTOR_ID, domain=None, range=Optional[Union[str, "DATACONTRIBUTORIDEnum"]])

slots.subjectCharacteristics__DATA_SOURCE = Slot(uri=EX.DATA_SOURCE, name="subjectCharacteristics__DATA_SOURCE", curie=EX.curie('DATA_SOURCE'),
                   model_uri=EX.subjectCharacteristics__DATA_SOURCE, domain=None, range=Optional[Union[str, "DATASOURCEEnum"]])

slots.subjectCharacteristics__LAST_KNOWN_SURVIVAL_STATUS = Slot(uri=EX.LAST_KNOWN_SURVIVAL_STATUS, name="subjectCharacteristics__LAST_KNOWN_SURVIVAL_STATUS", curie=EX.curie('LAST_KNOWN_SURVIVAL_STATUS'),
                   model_uri=EX.subjectCharacteristics__LAST_KNOWN_SURVIVAL_STATUS, domain=None, range=Optional[Union[str, "LASTKNOWNSURVIVALSTATUSEnum"]])

slots.subjectCharacteristics__AGE_LAST_CONTACT = Slot(uri=EX.AGE_LAST_CONTACT, name="subjectCharacteristics__AGE_LAST_CONTACT", curie=EX.curie('AGE_LAST_CONTACT'),
                   model_uri=EX.subjectCharacteristics__AGE_LAST_CONTACT, domain=None, range=Optional[float])

slots.subjectCharacteristics__AGE_LAST_CONTACT_UNIT = Slot(uri=EX.AGE_LAST_CONTACT_UNIT, name="subjectCharacteristics__AGE_LAST_CONTACT_UNIT", curie=EX.curie('AGE_LAST_CONTACT_UNIT'),
                   model_uri=EX.subjectCharacteristics__AGE_LAST_CONTACT_UNIT, domain=None, range=Optional[Union[str, "AGELASTCONTACTUNITEnum"]])

slots.subjectCharacteristics__AGE_LAST_CONTACT_PRECISION = Slot(uri=EX.AGE_LAST_CONTACT_PRECISION, name="subjectCharacteristics__AGE_LAST_CONTACT_PRECISION", curie=EX.curie('AGE_LAST_CONTACT_PRECISION'),
                   model_uri=EX.subjectCharacteristics__AGE_LAST_CONTACT_PRECISION, domain=None, range=Optional[Union[str, "AGELASTCONTACTPRECISIONEnum"]])

slots.timing__HONEST_BROKER_SUBJECT_ID = Slot(uri=EX.HONEST_BROKER_SUBJECT_ID, name="timing__HONEST_BROKER_SUBJECT_ID", curie=EX.curie('HONEST_BROKER_SUBJECT_ID'),
                   model_uri=EX.timing__HONEST_BROKER_SUBJECT_ID, domain=None, range=Optional[str])

slots.timing__TIMEPOINT = Slot(uri=EX.TIMEPOINT, name="timing__TIMEPOINT", curie=EX.curie('TIMEPOINT'),
                   model_uri=EX.timing__TIMEPOINT, domain=None, range=Optional[Union[str, "TIMEPOINTEnum"]])

slots.timing__AGE_AT = Slot(uri=EX.AGE_AT, name="timing__AGE_AT", curie=EX.curie('AGE_AT'),
                   model_uri=EX.timing__AGE_AT, domain=None, range=Optional[float])

slots.timing__AGE_UNIT = Slot(uri=EX.AGE_UNIT, name="timing__AGE_UNIT", curie=EX.curie('AGE_UNIT'),
                   model_uri=EX.timing__AGE_UNIT, domain=None, range=Optional[Union[str, "AGEUNITEnum"]])

slots.timing__AGE_PRECISION = Slot(uri=EX.AGE_PRECISION, name="timing__AGE_PRECISION", curie=EX.curie('AGE_PRECISION'),
                   model_uri=EX.timing__AGE_PRECISION, domain=None, range=Optional[Union[str, "AGEPRECISIONEnum"]])

slots.familyMedicalHistory__HONEST_BROKER_SUBJECT_ID = Slot(uri=EX.HONEST_BROKER_SUBJECT_ID, name="familyMedicalHistory__HONEST_BROKER_SUBJECT_ID", curie=EX.curie('HONEST_BROKER_SUBJECT_ID'),
                   model_uri=EX.familyMedicalHistory__HONEST_BROKER_SUBJECT_ID, domain=None, range=Optional[str])

slots.familyMedicalHistory__RELATION_HONEST_BROKER_SUBJECT_ID = Slot(uri=EX.RELATION_HONEST_BROKER_SUBJECT_ID, name="familyMedicalHistory__RELATION_HONEST_BROKER_SUBJECT_ID", curie=EX.curie('RELATION_HONEST_BROKER_SUBJECT_ID'),
                   model_uri=EX.familyMedicalHistory__RELATION_HONEST_BROKER_SUBJECT_ID, domain=None, range=Optional[str])

slots.familyMedicalHistory__RELATION = Slot(uri=EX.RELATION, name="familyMedicalHistory__RELATION", curie=EX.curie('RELATION'),
                   model_uri=EX.familyMedicalHistory__RELATION, domain=None, range=Optional[Union[str, "RELATIONEnum"]])

slots.familyMedicalHistory__CONDITION = Slot(uri=EX.CONDITION, name="familyMedicalHistory__CONDITION", curie=EX.curie('CONDITION'),
                   model_uri=EX.familyMedicalHistory__CONDITION, domain=None, range=Optional[Union[str, "CONDITIONEnum"]])

slots.familyMedicalHistory__SOURCE = Slot(uri=EX.SOURCE, name="familyMedicalHistory__SOURCE", curie=EX.curie('SOURCE'),
                   model_uri=EX.familyMedicalHistory__SOURCE, domain=None, range=Optional[Union[str, "SOURCEEnum"]])
