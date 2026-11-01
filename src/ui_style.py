"""Shared AppKit presentation primitives for the HUD and its settings window."""
from __future__ import annotations

import AppKit as A
from Foundation import NSMakeRect


def rgb(hex_code: int, alpha: float = 1.0) -> A.NSColor:
    return A.NSColor.colorWithCalibratedRed_green_blue_alpha_(
        ((hex_code >> 16) & 0xFF) / 255.0,
        ((hex_code >> 8) & 0xFF) / 255.0,
        (hex_code & 0xFF) / 255.0,
        alpha,
    )


# LOVER's dark-plum palette comes from the companion reflection UI: it makes the
# floating panel feel like a private pause rather than an operational alert.
PALETTE = {
    "bg": rgb(0x1B0B18),
    "text": rgb(0xFFF9FC),
    "muted": rgb(0xD9C5D2),
    "accent": rgb(0xFFB7CF),
    "lavender": rgb(0xD8D9FF),
    "green": rgb(0x4ADE80),
    "amber": rgb(0xFBBF24),
    "red": rgb(0xFB7185),
    "surface": rgb(0x3A1730),
    "row": rgb(0x2A1022),
    "field": rgb(0x24101E),
    "edge": rgb(0xA26182),
    "track": rgb(0x74425F),
}

# Opaque layers need their own contrast; white-on-white vibrancy colors disappear
# when macOS substitutes a solid backdrop for Reduce Transparency.
SOLID_PALETTE = {
    "bg": rgb(0x1B0B18),
    "surface": rgb(0x3A1730),
    "row": rgb(0x2A1022),
    "field": rgb(0x24101E),
    "edge": rgb(0x74425F),
    "track": rgb(0x74425F),
}

RADIUS_FIELD = 8
RADIUS_CARD = 12


def make_surface(radius: float, color: A.NSColor,
                 border: A.NSColor | None = None) -> A.NSView:
    """Create a layer-backed visual surface without application state or behavior."""
    surface = A.NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 1, 1))
    surface.setWantsLayer_(True)
    surface.layer().setBackgroundColor_(color.CGColor())
    surface.layer().setCornerRadius_(radius)
    if border is not None:
        surface.layer().setBorderColor_(border.CGColor())
        surface.layer().setBorderWidth_(0.75)
    return surface


def make_label(text: str, x: float, y: float, width: float, height: float,
               size: float = 13, color: A.NSColor | None = None,
               bold: bool = False, selectable: bool = False) -> A.NSTextField:
    field = A.NSTextField.alloc().initWithFrame_(NSMakeRect(x, y, width, height))
    field.setStringValue_(text)
    field.setBezeled_(False)
    field.setDrawsBackground_(False)
    field.setEditable_(False)
    field.setSelectable_(selectable)
    field.setTextColor_(PALETTE["text"] if color is None else color)
    font = A.NSFont.boldSystemFontOfSize_(size) if bold else A.NSFont.systemFontOfSize_(size)
    field.setFont_(font)
    return field


def style_button(button: A.NSButton, *, font_size: float = 11,
                 radius: float = 16, primary: bool = False) -> A.NSButton:
    """Apply the same quiet pill treatment used by actions on the HUD."""
    button.setBordered_(False)
    button.setFont_(A.NSFont.boldSystemFontOfSize_(font_size)
                    if primary else A.NSFont.systemFontOfSize_(font_size))
    button.setContentTintColor_(A.NSColor.whiteColor() if primary else PALETTE["text"])
    button.setWantsLayer_(True)
    button.layer().setBackgroundColor_((PALETTE["green"] if primary else PALETTE["row"]).CGColor())
    button.layer().setBorderColor_((PALETTE["green"] if primary else PALETTE["edge"]).CGColor())
    button.layer().setBorderWidth_(0.75)
    button.layer().setCornerRadius_(radius)
    return button
