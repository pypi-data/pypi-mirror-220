"""Classes for card data."""

from __future__ import annotations

import base64
import json
import random
import string
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import InitVar, dataclass, field, fields
from datetime import datetime
from enum import IntEnum
from typing import Any

from typing_extensions import Self

NS = {"ns": "http://www.emiratesid.ae/toolkit"}


# library command classes
class CMD(IntEnum):
    """List of commands."""

    ESTABLISH_CONTEXT = 1
    CLEANUP_CONETEXT = 2
    LIST_READERS = 3
    CONNECT_READER = 4
    DISCONNECT = 5
    READ_PUBLIC_DATA = 6
    READ_CERTIFICATE = 7
    CHECK_CARD_STATUS = 8
    GET_FINGER_INDEX = 9
    VERIFY_BIOMETRIC = 10
    MATCH_ON_CARD = 11
    PIN_RESET = 13
    AUTHENTICATE_PKI = 15
    SIGN_DATA = 16
    VERIFY_SIGNATURE = 17
    SET_NFC_PARAMS = 18
    GET_INTERFACE = 19
    CSN = 20
    CARD_VERSION = 21
    FAMILY_BOOK_DATA_REQUEST = 22
    CARD_GENUINE = 24
    GET_READER_WITH_EID = 54


@dataclass
class EIDContext:
    """class for storing context."""

    service_context: int = 0
    eid_card_context: str = ""
    card_reader_name: str = ""
    request_id: str = ""

    def gen_request_id(self) -> None:
        """Generate a new request_id."""
        letters = string.ascii_letters + string.digits
        random_str = "".join(random.choice(letters) for _ in range(40))
        self.request_id = base64.b64encode(random_str.encode("utf-8")).decode("utf-8")


class Request:
    """Reqeust base class."""

    def __init__(self) -> None:
        """Initialize request object."""
        self.context = EIDContext()

    @classmethod
    def establish_context(cls) -> dict[str, str | int]:
        """Request to establish context."""
        return {
            "cmd": CMD.ESTABLISH_CONTEXT.value,
            "config_params": "",
            "user_agent": "Chrome 114.0.0.0",
        }

    @property
    def request(self) -> dict[str, str | int]:
        return {"service_context": self.context.service_context}

    @property
    def list_readers(self) -> dict[str, str | int]:
        """List connected readers."""
        request = self.request.copy()
        request["cmd"] = CMD.LIST_READERS.value
        return request

    @property
    def reader_with_eid(self) -> dict[str, str | int]:
        """Request reader with EID inserted."""
        request = self.request.copy()
        request["cmd"] = CMD.GET_READER_WITH_EID.value
        return request

    @property
    def connect_to_reader(self) -> dict[str, str | int]:
        """Connect to selected reader."""
        request = self.request.copy()
        request["cmd"] = CMD.CONNECT_READER.value
        request["smartcard_reader"] = self.context.card_reader_name
        return request

    @property
    def read_eid_card(self) -> dict[str, str | int]:
        """Request for reading EID card."""
        request = self.request.copy()
        self.context.gen_request_id()
        request.update(
            {
                "cmd": CMD.READ_PUBLIC_DATA.value,
                "card_context": self.context.eid_card_context,
                "read_photography": True,
                "read_non_modifiable_data": True,
                "read_modifiable_data": True,
                "request_id": self.context.request_id,
                "signature_image": True,
                "address": True,
            }
        )
        return request

    @property
    def read_gcc_card(self) -> str:
        """Request for reading GCC card."""
        params = {
            "ReaderName": self.context.card_reader_name,
            "ReaderIndex": -1,
            "OutputFormat": "JSON",
            "SilentReading": True,
        }
        return f"ReadCard{json.dumps(params)}"


# EID Card data classes
@dataclass
class BaseClass:
    """Base class for card data classes."""

    @classmethod
    def from_xml_element(cls, root: ET.Element) -> Self:
        """Construct class from xml element."""
        _cls = object.__new__(cls)
        for cls_field in fields(_cls):
            element = root.find(f".ns:{cls_field.name}", NS)
            if element is not None:
                setattr(_cls, cls_field.name, element.text)
        return _cls


@dataclass(init=False)
class NonModifiableData(BaseClass):
    IdType: str
    IssueDate: str
    ExpiryDate: str
    TitleArabic: str
    FullNameArabic: str
    TitleEnglish: str
    FullNameEnglish: str
    Gender: str
    NationalityArabic: str
    NationalityEnglish: str
    NationalityCode: str
    DateOfBirth: str
    PlaceOfBirthArabic: str
    PlaceOfBirthEnglish: str


@dataclass(init=False)
class ModifiableData(BaseClass):
    OccupationCode: str
    OccupationArabic: str
    OccupationEnglish: str
    FamilyId: str
    OccupationTypeArabic: str
    OccupationTypeEnglish: str
    OccupationFieldCode: str
    CompanyNameArabic: str
    CompanyNameEnglish: str
    MaritalStatusCode: str
    HusbandIdNumber: str
    SponsorTypeCode: str
    SponsorUnifiedNumber: str
    SponsorName: str
    ResidencyTypeCode: str
    ResidencyNumber: str
    ResidencyExpiryDate: str
    PassportNumber: str
    PassportTypeCode: str
    PassportCountryCode: str
    PassportCountryArabic: str
    PassportCountryEnglish: str
    PassportIssueDate: str
    PassportExpiryDate: str
    QualificationLevelCode: str
    QualificationLevelArabic: str
    QualificationLevelEnglish: str
    DegreeDescriptionArabic: str
    DegreeDescriptionEnglish: str
    FieldOfStudyCode: str
    FieldOfStudyArabic: str
    FieldOfStudyEnglish: str
    PlaceOfStudyArabic: str
    PlaceOfStudyEnglish: str
    DateOfGraduation: str
    MotherFullNameArabic: str
    MotherFullNameEnglish: str


@dataclass(init=False)
class HomeAddress(BaseClass):
    AddressTypeCode: str
    LocationCode: str
    EmiratesCode: str
    EmiratesDescArabic: str
    EmiratesDescEnglish: str
    CityCode: str
    CityDescArabic: str
    CityDescEnglish: str
    StreetArabic: str
    StreetEnglish: str
    POBOX: str
    AreaCode: str
    AreaDescArabic: str
    AreaDescEnglish: str
    BuildingNameArabic: str
    BuildingNameEnglish: str
    FlatNo: str
    ResidentPhoneNumber: str
    MobilePhoneNumber: str
    Email: str


@dataclass(init=False)
class WorkAddress(BaseClass):
    AddressTypeCode: str
    LocationCode: str
    CompanyNameArabic: str
    CompanyNameEnglish: str
    EmiratesCode: str
    EmiratesDescArabic: str
    EmiratesDescEnglish: str
    CityCode: str
    CityDescArabic: str
    CityDescEnglish: str
    StreetArabic: str
    StreetEnglish: str
    POBOX: str
    AreaCode: str
    AreaDescArabic: str
    AreaDescEnglish: str
    BuildingNameArabic: str
    BuildingNameEnglish: str
    LandPhoneNumber: str
    MobilePhoneNumber: str
    Email: str


@dataclass
class EIDCardData:
    xml_data: InitVar[str]
    IdNumber: str | None = field(init=False)
    CardNumber: str | None = field(init=False)
    NonModifiableData: NonModifiableData = field(init=False)
    ModifiableData: ModifiableData = field(init=False)
    HomeAddress: HomeAddress = field(init=False)
    WorkAddress: WorkAddress = field(init=False)
    CardHolderPhoto: str | None = field(init=False)
    HolderSignatureImage: str | None = field(init=False)

    def __post_init__(self, xml_data: str) -> None:
        """Fill attribute values from xml_data."""
        root = ET.fromstring(xml_data)
        body = root.find(".//ns:PublicData", NS)
        if body is None:
            return
        for child in body:
            if "IdNumber" in child.tag:
                self.IdNumber = child.text
            if "CardNumber" in child.tag:
                self.CardNumber = child.text
            if "NonModifiableData" in child.tag:
                self.NonModifiableData = NonModifiableData.from_xml_element(child)
            if "ModifiableData" in child.tag:
                self.ModifiableData = ModifiableData.from_xml_element(child)
            if "HomeAddress" in child.tag:
                self.HomeAddress = HomeAddress.from_xml_element(child)
            if "WorkAddress" in child.tag:
                self.WorkAddress = WorkAddress.from_xml_element(child)
            if "CardHolderPhoto" in child.tag:
                self.CardHolderPhoto = child.text
            if "HolderSignatureImage" in child.tag:
                self.HolderSignatureImage = child.text


# GCC ID related classes
@dataclass
class MiscellaneousTextData:
    FirstNameArabic: str
    LastNameArabic: str
    MiddleName1Arabic: str
    MiddleName2Arabic: str
    MiddleName3Arabic: str
    MiddleName4Arabic: str
    BloodGroup: str
    CPRNO: str
    DateOfBirth: str
    FirstNameEnglish: str
    LastNameEnglish: str
    MiddleName1English: str
    MiddleName2English: str
    MiddleName3English: str
    MiddleName4English: str
    Gender: str
    Email: str
    ContactNo: str
    ResidenceNo: str
    FlatNo: str
    BuildingNo: str
    BuildingAlpha: str
    BuildingAlphaArabic: str
    RoadNo: str
    RoadName: str
    RoadNameArabic: str
    BlockNo: str
    BlockName: str
    BlockNameArabic: str
    GovernorateNo: str
    GovernorateNameEnglish: str
    GovernorateNameArabic: str
    EmployerName1Arabic: str
    EmployerName2Arabic: str
    EmployerName3Arabic: str
    EmployerName4Arabic: str
    LatestEducationDegreeArabic: str
    OccupationDescription1Arabic: str
    OccupationDescription2Arabic: str
    OccupationDescription3Arabic: str
    OccupationDescription4Arabic: str
    SponsorNameArabic: str
    ClearingAgentIndicator: str
    EmployerFlag1: str
    EmployerFlag2: str
    EmployerFlag3: str
    EmployerFlag4: str
    EmployerName1: str
    EmployerName2: str
    EmployerName3: str
    EmployerName4: str
    EmployerNo1: str
    EmployerNo2: str
    EmployerNo3: str
    EmployerNo4: str
    EmploymentFlag1: str
    EmploymentFlag2: str
    EmploymentFlag3: str
    EmploymentFlag4: str
    LaborForceParticipation: str
    LatestEducationDegree: str
    OccupationDescription1: str
    OccupationDescription2: str
    OccupationDescription3: str
    OccupationDescription4: str
    SponsorCPRNoorUnitNo: str
    SponsorFlag: str
    SponsorName: str
    LfpNameEnglish: str
    LfpNameArabic: str
    EnglishCountryName: str
    ArabicCountryName: str
    IACOCode: str
    Alpha2Code: str
    Alpha3Code: str
    Nationality: str
    PlaceOfBirth: str
    ArabicPlaceOfBirth: str
    CountryOfBirth: str
    PassportNo: str
    PassportType: str
    PassportSequnceNo: str
    IssueDate: str
    ExpiryDate: str
    VisaNo: str
    VisaExpiryDate: str
    VisaType: str
    ResidentPermitNo: str
    ResidentPermitExpiryDate: str
    TypeOfResident: str


@dataclass
class GCCIDCardData:
    """Card data class."""

    AddressArabic: str
    AddressEnglish: str
    ArabicFirstName: str
    ArabicFullName: str
    ArabicLastName: str
    ArabicMiddleName2: str
    ArabicMiddleName3: str
    ArabicMiddleName4: str
    ArabicMiddleName5: str
    BirthDate: str
    CardCountry: str
    CardexpiryDate: str
    CardIssueDate: str
    CardSerialNumber: str
    CardVersion: str
    EmploymentFlag: str
    EmploymentId: str
    EmploymentNameArabic: str
    EmploymentNameEnglish: str
    EnglishFirstName: str
    EnglishFullName: str
    EnglishLastName: str
    EnglishMiddleName2: str
    EnglishMiddleName3: str
    EnglishMiddleName4: str
    EnglishMiddleName5: str
    FingerprintCode: str
    Gender: str
    IacoNationalityCode: str
    IsoNationalityCode: str
    IdNumber: str
    IsMatchOnCardAvailiable: str
    MiscellaneousBinaryData: dict[str, str]
    MiscellaneousTextData: MiscellaneousTextData
    NationalityCode: str
    OccupationArabic: str
    OccupationEnglish: str
    PassportExpiryDate: str
    PassportIssueDate: str
    PassportNumber: str
    PassportType: str
    Photo: str
    PhotoB64Encoded: str
    Signature: str
    SignB64Encoded: str
    SponserId: str
    SponserNameArabic: str
    SponserNameEnglish: str
    ErrorDescription: str

    def __post_init__(self) -> None:
        if isinstance(self.MiscellaneousTextData, dict):
            self.MiscellaneousTextData = MiscellaneousTextData(
                **self.MiscellaneousTextData
            )


@dataclass
class CardDataField:
    """Class to represent Card data field."""

    name: str
    value_fn: Callable[  # noqa: E731
        [EIDCardData | GCCIDCardData], Any
    ] = lambda val: val


CARDDATA_FIELDS: tuple[CardDataField, ...] = (
    CardDataField(name="IdNumber", value_fn=lambda val: val.IdNumber),
    CardDataField(
        name="IssueDate",
        value_fn=lambda val: datetime.strptime(
            val.NonModifiableData.IssueDate
            if isinstance(val, EIDCardData)
            else val.CardIssueDate,
            "%d/%m/%Y",
        ),
    ),
    CardDataField(
        name="ExpiryDate",
        value_fn=lambda val: datetime.strptime(
            val.NonModifiableData.ExpiryDate
            if isinstance(val, EIDCardData)
            else val.CardexpiryDate,
            "%d/%m/%Y",
        ),
    ),
    CardDataField(
        name="CardNumber",
        value_fn=lambda val: val.CardNumber
        if isinstance(val, EIDCardData)
        else val.CardSerialNumber,
    ),
    CardDataField(
        name="FirstNameEnglish",
        value_fn=lambda val: val.NonModifiableData.FullNameEnglish.split(",")[0]
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.FirstNameEnglish,
    ),
    CardDataField(
        name="MiddleNameEnglish",
        value_fn=lambda val: val.NonModifiableData.FullNameEnglish.split(",")[1]
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.MiddleName1English,
    ),
    CardDataField(
        name="LastNameEnglish",
        value_fn=lambda val: val.NonModifiableData.FullNameEnglish.split(",")[-2]
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.LastNameEnglish,
    ),
    CardDataField(
        name="FirstNameArabic",
        value_fn=lambda val: val.NonModifiableData.FullNameArabic.split(",")[0]
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.FirstNameArabic,
    ),
    CardDataField(
        name="MiddleNameArabic",
        value_fn=lambda val: val.NonModifiableData.FullNameArabic.split(",")[1]
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.MiddleName1Arabic,
    ),
    CardDataField(
        name="LastNameArabic",
        value_fn=lambda val: val.NonModifiableData.FullNameArabic.split(",")[-2]
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.LastNameArabic,
    ),
    CardDataField(
        name="Gender",
        value_fn=lambda val: val.NonModifiableData.Gender
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.Gender,
    ),
    CardDataField(
        name="Email",
        value_fn=lambda val: val.WorkAddress.Email or val.HomeAddress.Email
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.Email,
    ),
    CardDataField(
        name="Mobile",
        value_fn=lambda val: val.WorkAddress.MobilePhoneNumber
        or val.HomeAddress.MobilePhoneNumber
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.ContactNo,
    ),
    CardDataField(
        name="DateOfBirth",
        value_fn=lambda val: datetime.strptime(
            val.NonModifiableData.DateOfBirth
            if isinstance(val, EIDCardData)
            else val.BirthDate,
            "%d/%m/%Y",
        ),
    ),
    CardDataField(
        name="NationalityArabic",
        value_fn=lambda val: val.NonModifiableData.NationalityArabic
        if isinstance(val, EIDCardData)
        else "",
    ),
    CardDataField(
        name="NationalityEnglish",
        value_fn=lambda val: val.NonModifiableData.NationalityEnglish
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.Nationality,
    ),
    CardDataField(
        name="PlaceOfBirthEnglish",
        value_fn=lambda val: val.NonModifiableData.PlaceOfBirthEnglish
        if isinstance(val, EIDCardData)
        else val.MiscellaneousTextData.CountryOfBirth,
    ),
    CardDataField(
        name="PlaceOfBirthArabic",
        value_fn=lambda val: val.NonModifiableData.PlaceOfBirthArabic
        if isinstance(val, EIDCardData)
        else "",
    ),
    CardDataField(
        name="OccupationEnglish",
        value_fn=lambda val: val.ModifiableData.OccupationEnglish
        if isinstance(val, EIDCardData)
        else val.OccupationEnglish,
    ),
    CardDataField(
        name="OccupationArabic",
        value_fn=lambda val: val.ModifiableData.OccupationArabic
        if isinstance(val, EIDCardData)
        else val.OccupationArabic,
    ),
    CardDataField(
        name="CompanyNameEnglish",
        value_fn=lambda val: val.ModifiableData.CompanyNameEnglish
        if isinstance(val, EIDCardData)
        else val.EmploymentNameEnglish,
    ),
    CardDataField(
        name="CompanyNameArabic",
        value_fn=lambda val: val.ModifiableData.CompanyNameArabic
        if isinstance(val, EIDCardData)
        else val.EmploymentNameArabic,
    ),
    CardDataField(
        name="SponsorUnifiedNumber",
        value_fn=lambda val: val.ModifiableData.SponsorUnifiedNumber
        if isinstance(val, EIDCardData)
        else val.SponserId,
    ),
    CardDataField(
        name="SponsorName",
        value_fn=lambda val: val.ModifiableData.SponsorName
        if isinstance(val, EIDCardData)
        else val.SponserNameEnglish,
    ),
    CardDataField(
        name="PassportNumber",
        value_fn=lambda val: val.ModifiableData.PassportNumber
        if isinstance(val, EIDCardData)
        else val.PassportNumber,
    ),
    CardDataField(
        name="PassportIssueDate",
        value_fn=lambda val: datetime.strptime(
            val.ModifiableData.PassportIssueDate, "%d/%m/%Y"
        )
        if isinstance(val, EIDCardData)
        and val.ModifiableData.PassportIssueDate is not None
        else (
            datetime.strptime(val.PassportIssueDate, "%d/%m/%Y")
            if isinstance(val, GCCIDCardData) and val.PassportIssueDate is not None
            else None
        ),
    ),
    CardDataField(
        name="PassportExpiryDate",
        value_fn=lambda val: datetime.strptime(
            val.ModifiableData.PassportExpiryDate, "%d/%m/%Y"
        )
        if isinstance(val, EIDCardData)
        and val.ModifiableData.PassportExpiryDate is not None
        else (
            datetime.strptime(val.PassportExpiryDate, "%d/%m/%Y")
            if isinstance(val, GCCIDCardData) and val.PassportExpiryDate is not None
            else None
        ),
    ),
    CardDataField(
        name="Photo",
        value_fn=lambda val: val.CardHolderPhoto
        if isinstance(val, EIDCardData)
        else val.PhotoB64Encoded,
    ),
)


@dataclass
class CardData:
    card_data: EIDCardData | GCCIDCardData = field(repr=False)
    IdNumber: str = ""
    IssueDate: datetime | None = None
    ExpiryDate: datetime | None = None
    CardNumber: str = ""
    FirstNameEnglish: str = ""
    MiddleNameEnglish: str = ""
    LastNameEnglish: str = ""
    FirstNameArabic: str = ""
    MiddleNameArabic: str = ""
    LastNameArabic: str = ""
    Gender: str = ""
    Email: str = ""
    Mobile: str = ""
    DateOfBirth: datetime | None = None
    NationalityEnglish: str = ""
    NationalityArabic: str = ""
    PlaceOfBirthEnglish: str = ""
    PlaceOfBirthArabic: str = ""
    OccupationEnglish: str = ""
    OccupationArabic: str = ""
    CompanyNameEnglish: str = ""
    CompanyNameArabic: str = ""
    SponsorUnifiedNumber: str = ""
    SponsorName: str = ""
    PassportNumber: str = ""
    PassportIssueDate: datetime | None = None
    PassportExpiryDate: datetime | None = None
    Photo: str = ""

    def __post_init__(self) -> None:
        """Fill in field values from card data."""
        for card_field in CARDDATA_FIELDS:
            setattr(self, card_field.name, card_field.value_fn(self.card_data))
