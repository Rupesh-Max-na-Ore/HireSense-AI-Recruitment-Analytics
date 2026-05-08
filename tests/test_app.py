def test_streamlit_app_exists() -> None:
    """
    Basic sanity test for app existence.
    """

    with open("app.py") as file:
        content = file.read()

    assert "HireSense AI" in content
