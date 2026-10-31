DEFAULT_RULES = [
    ("create_vendor", "approve_payment"),
    ("create_journal", "approve_journal"),
    ("create_po", "receive_goods"),
    ("modify_payroll", "approve_payroll"),
]

def sod_conflicts(user_perms, rules=DEFAULT_RULES):
    """user_perms: dict user -> iterable of permissions. Returns list of (user, a, b)."""
    out = []
    for user, perms in sorted(user_perms.items()):
        p = set(perms)
        for a, b in rules:
            if a in p and b in p:
                out.append((user, a, b))
    return out
