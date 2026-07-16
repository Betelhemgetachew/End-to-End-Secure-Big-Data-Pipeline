PERMISSIONS = {

    "ADMIN": [
        "validate",
        "import",
        "encrypt",
        "verify_hash",
        "view_logs",
        "view_security_events"
    ],

    "ANALYST": [
        "validate",
        "import"
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



    print(has_permission("ADMIN", "import"))
    print(has_permission("ADMIN", "view_logs"))

    print(has_permission("ANALYST", "import"))
    print(has_permission("ANALYST", "encrypt"))

    print(has_permission("AUDITOR", "verify_hash"))
    print(has_permission("AUDITOR", "import"))