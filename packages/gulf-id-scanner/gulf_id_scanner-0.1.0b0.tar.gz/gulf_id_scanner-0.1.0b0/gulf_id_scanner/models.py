"""Classes for card data."""

from __future__ import annotations

import base64
import json
import random
import string
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass, field, fields
from datetime import datetime
from enum import IntEnum

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

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class EstablishContext:
    """Establish context request."""

    cmd: CMD = CMD.ESTABLISH_CONTEXT.value
    config_params: str = ""
    user_agent: str = "Chrome 114.0.0.0"

    def __str__(self):
        return repr(self.__dict__)


@dataclass
class EIDContext:
    """class for storing context."""

    service_context: str = ""
    eid_card_context: str = ""
    card_reader_name: str = ""
    request_id: str = ""

    def gen_request_id(self) -> str:
        """Generate a new request_id."""
        letters = string.ascii_letters + string.digits
        random_str = "".join(random.choice(letters) for _ in range(40))
        self.request_id = base64.b64encode(random_str.encode("utf-8")).decode("utf-8")


class EIDRequest:
    """Reqeust base class."""

    def __init__(self, context: EIDContext) -> None:
        """Initialize request object."""
        self.context = context
        self.request: dict[str, str] = {"service_context": context.service_context}

    def list_readers(self) -> dict[str, str]:
        """List connected readers."""
        request = self.request.copy()
        request["cmd"] = CMD.LIST_READERS
        return request

    def reader_with_eid(self) -> dict[str, str]:
        """Request reader with EID inserted."""
        request = self.request.copy()
        request["cmd"] = CMD.GET_READER_WITH_EID
        return request

    def connect_to_reader(self, reader_name: str) -> dict[str, str]:
        """Connect to selected reader."""
        request = self.request.copy()
        request["cmd"] = CMD.CONNECT_READER
        request["smartcard_reader"] = reader_name
        return request

    def read_card_data(self) -> dict[str, str]:
        """Read card data."""
        request = self.request.copy()
        self.context.gen_request_id()
        request.update(
            {
                "cmd": CMD.READ_PUBLIC_DATA,
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


# EID Card data classes
class BaseClass:
    """Base class for card data classes."""

    @classmethod
    def from_xml_element(cls, root: ET.Element) -> Self:
        """Construct class from xml element."""
        _cls = object.__new__(cls)
        for cls_field in fields(_cls):
            element = root.find(f".ns:{cls_field.name}", NS)
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
    StreetArabic: str
    StreetEnglish: str
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
    IdNumber: str
    CardNumber: str
    NonModifiableData: NonModifiableData
    ModifiableData: ModifiableData
    HomeAddress: HomeAddress
    WorkAddress: WorkAddress
    CardHolderPhoto: str
    HolderSignatureImage: str

    @classmethod
    def from_xml(cls, data: str) -> EIDCardData:
        """Construct class from xml data."""
        root = ET.fromstring(data)
        return EIDCardData(
            IdNumber=root.find(".//ns:IdNumber", NS).text,
            CardNumber=root.find(".//ns:CardNumber", NS).text,
            NonModifiableData=NonModifiableData.from_xml_element(
                root.find(".//ns:NonModifiableData", NS)
            ),
            ModifiableData=ModifiableData.from_xml_element(
                root.find(".//ns:ModifiableData", NS)
            ),
            HomeAddress=HomeAddress.from_xml_element(
                root.find(".//ns:HomeAddress", NS)
            ),
            WorkAddress=WorkAddress.from_xml_element(
                root.find(".//ns:WorkAddress", NS)
            ),
            CardHolderPhoto=root.find(".//ns:CardHolderPhoto", NS).text,
            HolderSignatureImage=root.find(".//ns:HolderSignatureImage", NS).text,
        )


# GCC ID related classes
@dataclass
class GCCIDRequest:
    """Gulf ID read request."""

    ReadCardInfo: bool = True
    ReadPersonalInfo: bool = True
    ReadAddressDetails: bool = True
    ReadBiometrics: bool = True
    ReadEmploymentInfo: bool = True
    ReadImmigrationDetails: bool = True
    ReadTrafficDetails: bool = True
    ReaderName: str = ""
    ReaderIndex: int = -1
    OutputFormat: str = "JSON"
    ValidateCard: bool = False
    SilentReading: bool = True

    def __repr__(self) -> str:
        """Return request string."""
        return f"ReadCard{json.dumps(self.__dict__)}"


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
        self.MiscellaneousTextData = MiscellaneousTextData(**self.MiscellaneousTextData)


@dataclass
class CardDataField:
    """Class to represent Card data field."""

    name: str
    value_fn: Callable[  # noqa: E731
        [EIDCardData | GCCIDCardData], str
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
            val.ModifiableData.PassportIssueDate  # TODO check if value is not there
            if isinstance(val, EIDCardData)
            else val.PassportIssueDate,
            "%d/%m/%Y",
        ),
    ),
    CardDataField(
        name="PassportExpiryDate",
        value_fn=lambda val: datetime.strptime(
            val.ModifiableData.PassportExpiryDate
            if isinstance(val, EIDCardData)
            else val.PassportExpiryDate,
            "%d/%m/%Y",
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
