def menu_by_role(role: str):
    if role == "owner":
        return ["➕ Add Channel", "📢 Broadcast", "📊 Admin Panel"]
    if role == "premium":
        return ["➕ Add Channel", "📢 Broadcast", "⭐ Premium", "⚙ Settings"]
    if role == "restricted":
        return ["🆘 Contact Support"]
    if role == "blocked":
        return []
    return ["➕ Add Channel", "📢 Broadcast", "⭐ Premium", "⚙ Settings"]
