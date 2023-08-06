from enum import Enum


class CBIService(Enum):
    """Descriptive names for CBi service options"""

    TransactionHistory7 = 1
    TransactionHistory30 = 2
    TransactionHistory60 = 3
    TransactionHistory90 = 4
    TransactionHistory180 = 5
    BankStatement30 = 6
    BankStatement60 = 7
    BankStatement90 = 8
    BankStatement180 = 9
    Beneficiaries = 10
    AccountInfo = 11
    PersonalInfo = 12
    ContactInfo = 13
    Address = 14


class CBiInsight(Enum):
    """Descriptive names for CBi Data Insight Services"""

    Affordability = 1
    DebitOrder = 2
    IncomeVerification = 3
    StrikeDate = 4


class DeliveryMethod(Enum):
    """Descriptive names for link delivery mechanisms"""

    NONE = 0
    Email = 1
    SMS = 2
    WhatsApp = 4
    GetLink = 8


class IDType(Enum):
    """Descriptive names for types of ID acceptable to Authentifi"""

    IDNumber = 1
    Passport = 2
    TempIDNumber = 3
    CompanyRegNumber = 4


class CBiPurpose(Enum):
    """Descriptive names for purpose types, as retrieved from a call to /Request/GetPurpose/14"""

    AccountOpening = 1
    AdministrativeAssessment = 2
    AffordabilityAssessment = 3
    ComplianceAssessment = 4
    CreditAssessment = 5
    DebtRecovery = 6
    RiskAssessment = 7


class EngagementMethod(Enum):
    """Descriptive names for engagement methods, as retrieved from a call to Request/GetEngagementMethod"""

    InBranch = 1
    Online = 2
    CallCenter = 3
    SalesAgent = 4
    Other = 5


class CBiResult(Enum):
    """Descriptive names for result status integers for CBI client interactions"""

    Unknown = 0
    Created = 1
    InviteAccepted = 2
    Success = 3
    Cancelled = 4
    Failed = 5
    FilesReady = 6
    TimedOut = 7
    OnLandingPage = 8
    OnSafePage = 9
    OnCancelPage = 10
    OnCancelSucessPage = 11
    OnSucessPage = 12
    OnFinalPage = 13
