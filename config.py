"""Pipeline settings: time windows, LMI weights, grant keyword map, model."""
from datetime import date, timedelta

CFPB_API = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
GRANTS_API = "https://api.grants.gov/v1/api/search2"

MODEL = "claude-opus-5-5"


def windows(today: date | None = None):
    """Two rolling 12-month windows ending on the last full month."""
    today = today or date.today()
    end = today.replace(day=1) - timedelta(days=1)          # last day of last full month
    start = date(end.year - 1, end.month, 1) + timedelta(days=32)
    start = start.replace(day=1)                             # first day 11 months before end's month
    prev_end = start - timedelta(days=1)
    prev_start = date(start.year - 1, start.month, 1)
    return (prev_start.isoformat(), prev_end.isoformat()), (start.isoformat(), end.isoformat())


# Minimum complaints in the recent window to be a candidate signal.
MIN_VOLUME = 300

# Products excluded from the growth baseline and candidate list. Credit reporting is ~6M
# complaints/yr, concentrated on the three bureaus and heavily driven by credit-repair
# template filings, so it swamps every other signal.
EXCLUDE_PRODUCTS = {"Credit reporting or other personal consumer reports"}

# Low/middle-income relevance, 0-5. Keys are (product, sub_product); sub_product "*" = default.
LMI_WEIGHTS = {
    ("Payday loan, title loan, personal loan, or advance loan", "*"): 5,
    ("Prepaid card", "Government benefit card"): 5,
    ("Prepaid card", "*"): 4,
    ("Money transfer, virtual currency, or money service", "Domestic (US) money transfer"): 4,
    ("Money transfer, virtual currency, or money service", "International money transfer"): 5,
    ("Money transfer, virtual currency, or money service", "Mobile or digital wallet"): 4,
    ("Money transfer, virtual currency, or money service", "Virtual currency"): 1,
    ("Money transfer, virtual currency, or money service", "*"): 3,
    ("Mortgage", "FHA mortgage"): 5,
    ("Mortgage", "VA mortgage"): 4,
    ("Mortgage", "USDA mortgage"): 5,
    ("Mortgage", "Manufactured home loan"): 5,
    ("Mortgage", "Reverse mortgage"): 3,
    ("Mortgage", "*"): 2,
    ("Debt collection", "Medical debt"): 5,
    ("Debt collection", "Rental debt"): 5,
    ("Debt collection", "Payday loan debt"): 5,
    ("Debt collection", "*"): 4,
    ("Vehicle loan or lease", "*"): 4,
    ("Student loan", "*"): 4,
    ("Checking or savings account", "*"): 3,
    ("Debt or credit management", "*"): 4,
    ("Credit card", "Store credit card"): 3,
    ("Credit card", "*"): 2,
}

# Grants.gov searches per signal. Keys match product or "product|sub_product".
GRANT_KEYWORDS = {
    "Payday loan, title loan, personal loan, or advance loan": ['CDFI', 'financial empowerment', 'financial literacy', 'credit union'],
    "Prepaid card|Government benefit card": ['"SNAP"', '"TANF"', 'benefit delivery'],
    "Prepaid card": ['"financial education"', 'unbanked'],
    "Money transfer, virtual currency, or money service": ['immigrant', 'refugee', 'financial literacy', 'elder fraud'],
    "Mortgage|FHA mortgage": ['"housing counseling"', 'homeownership', 'foreclosure'],
    "Mortgage|VA mortgage": ['veteran', '"housing counseling"'],
    "Mortgage|USDA mortgage": ['rural housing', '"housing counseling"'],
    "Mortgage|Manufactured home loan": ['manufactured housing', '"housing counseling"'],
    "Mortgage": ['"housing counseling"', 'homeownership'],
    "Debt collection": ['"legal aid"', 'legal services', '"financial education"'],
    "Debt collection|Rental debt": ['eviction', 'rental assistance', 'legal services'],
    "Debt collection|Medical debt": ['medical debt', 'legal services'],
    "Vehicle loan or lease": ['transportation', 'CDFI', 'financial literacy'],
    "Student loan": ['student debt', 'college completion'],
    "Checking or savings account": ['"financial education"', 'unbanked'],
    "Debt or credit management": ['credit counseling', '"financial education"'],
    "Credit card": ['"financial education"'],
}

# Grants.gov filters: posted/forecasted only, social-sector funding categories
# (Community Development, Consumer Protection, Employment/Labor/Training, Housing,
# Income Security & Social Services, Food & Nutrition, Law/Justice/Legal Services).
# Without the category filter, phrase matches hit applicant boilerplate (nuclear, parks…).
GRANT_STATUSES = "forecasted|posted"
GRANT_CATEGORIES = "CD|CP|ELT|HO|ISS|FN|LJL"
