import sys

# Dictionary mapping out the specific GCP audit log terms from your screenshots
gcp_glossary = {
    "UpdateConsumerPolicyRequest": (
        "API Method (Service Usage API Beta): "
        "Triggered when quotas, service restrictions, or consumer policies "
        "are updated for a Google Cloud project."
    ),
    "projects/.../consumerPolicies/default": (
        "Resource Path: "
        "Points to the default policy configuration governing which GCP "
        "APIs, features, or resource quotas are allowed or restricted."
    ),
    "kRedactedNonRoutableIp": (
        "Security Redaction: "
        "Google Cloud automatically strips or masks internal/non-routable "
        "caller IP addresses in audit records for privacy."
    ),
    "google.cloud.audit.AuditLog": (
        "Log Type: "
        "A standard administrative record tracking API calls, configuration "
        "tweaks, or service checks executed inside the project."
    ),
    "project-e225d085-08d3-4ec3-8cb": (
        "Target Project ID: "
        "The unique alphanumeric identifier for the GCP project where "
        "these background API calls and events are being logged."
    )
}

print("=" * 60)
print(" GCP AUDIT LOG FIELD DECODER ")
print("=" * 60)

for term, explanation in gcp_glossary.items():
    print(f"\n🔹 {term}")
    print(f"   ↳ {explanation}")

print("\n" + "=" * 60)
