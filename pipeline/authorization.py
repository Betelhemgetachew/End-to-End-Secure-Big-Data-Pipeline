PERMISSIONS = {

    "ADMIN": [
        "validate",
        "import",
        "encrypt",
        "verify_hash",
        "view_logs",
        "view_security_events",
        "export"
    ],

    "ANALYST": [
        "validate",
        "verify_hash"
    ],

    "AUDITOR": [
        "verify_hash",
        "view_logs",
        "view_security_events"
    ]

}

def has_permission(role, permission):
    """
    Check whether a role has a given permission.
    """

    return permission in PERMISSIONS.get(role, [])



    