from ml_auto_learning_app.security_service import SecurityService


def test_gsl_blocks_modifications_until_unlock_window() -> None:
    sec = SecurityService()
    sec.enable_gsl("alice", unlock_after_hours=24)
    assert sec.can_modify_settings("alice") is False


def test_whitelist_address() -> None:
    sec = SecurityService()
    sec.whitelist_address("alice", "0xABC")
    assert sec.is_address_whitelisted("alice", "0xABC") is True
