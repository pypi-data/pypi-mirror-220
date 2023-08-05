from __future__ import annotations

import mknodes


def test_virtual_files():
    nav = mknodes.Nav()
    subnav = nav.add_nav("subsection")
    page = subnav.add_page("page")
    img = mknodes.BinaryImage(data=b"", path="Test.jpg")
    page.append(img)
