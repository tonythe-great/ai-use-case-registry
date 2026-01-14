"""Risk tier computation logic."""

# Data types that are considered high-risk (PII, sensitive data)
HIGH_RISK_DATA_TYPES = {
    "pii",
    "personal data",
    "health data",
    "financial data",
    "biometric",
    "biometric data",
    "location data",
    "genetic data",
}

# Data types that are considered medium-risk
MEDIUM_RISK_DATA_TYPES = {
    "customer data",
    "employee data",
    "usage data",
    "behavioral data",
}

# Data types that are considered low-risk
LOW_RISK_DATA_TYPES = {
    "public data",
    "aggregated data",
    "product data",
    "internal documents",
}

# Data residency locations that increase risk
HIGH_RISK_RESIDENCY = {"international", "multi-region", "unknown"}


def compute_risk_tier(
    data_types: list[str],
    data_residency: str,
    external_sharing: str,
) -> str:
    """
    Compute the risk tier based on use case attributes.

    Risk tiers:
    - high: Contains sensitive data, shares externally, or non-compliant residency
    - medium: Contains some customer/employee data or moderate risk factors
    - low: Internal data only, no external sharing, compliant residency

    Args:
        data_types: List of data types being processed
        data_residency: Where the data is stored
        external_sharing: Whether data is shared externally ("yes" or "no")

    Returns:
        Risk tier as string: "high", "medium", or "low"
    """
    risk_score = 0
    data_types_lower = {dt.lower() for dt in data_types}

    # Check for high-risk data types
    if data_types_lower & HIGH_RISK_DATA_TYPES:
        risk_score += 3

    # Check for medium-risk data types
    if data_types_lower & MEDIUM_RISK_DATA_TYPES:
        risk_score += 1

    # Check data residency
    if data_residency.lower() in HIGH_RISK_RESIDENCY:
        risk_score += 2

    # Check external sharing
    if external_sharing.lower() == "yes":
        risk_score += 2

    # Determine risk tier based on score
    if risk_score >= 3:
        return "high"
    elif risk_score >= 1:
        return "medium"
    else:
        return "low"
