"""
Branding configuration for Voice Cloner
Customize with your logo, colors, and company information
"""

from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class BrandingConfig:
    """Application branding configuration"""

    # Application Identity
    app_name: str = "Voice Cloner Pro"
    app_version: str = "0.1.0"
    app_tagline: str = "AI-Powered Voice Cloning for Music Production"
    
    # Company Information
    company_name: str = "Your Company Name"
    company_website: str = "https://yourcompany.com"
    company_email: str = "support@yourcompany.com"
    
    # Colors (RGB)
    primary_color: tuple = (13, 71, 161)  # Blue
    primary_light: tuple = (21, 101, 192)  # Lighter blue
    accent_color: tuple = (0, 204, 0)  # Green
    text_color: tuple = (255, 255, 255)  # White
    background_dark: tuple = (43, 43, 43)  # Dark gray
    background_darker: tuple = (30, 30, 30)  # Darker gray
    
    # Logo Paths
    logo_path: Optional[Path] = None  # Main logo (PNG/SVG)
    icon_path: Optional[Path] = None  # App icon (ICO/PNG)
    favicon_path: Optional[Path] = None  # Favicon (ICO)
    
    # Legal
    license_type: str = "MIT"
    copyright_year: str = "2025"
    privacy_policy_url: str = "https://yourcompany.com/privacy"
    terms_url: str = "https://yourcompany.com/terms"
    
    # Support
    support_url: str = "https://yourcompany.com/support"
    documentation_url: str = "https://yourcompany.com/docs"
    bug_report_url: str = "https://github.com/yourcompany/voicecloner/issues"
    
    # Features
    enable_auto_updates: bool = True
    enable_telemetry: bool = False
    enable_feedback: bool = True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "app_tagline": self.app_tagline,
            "company_name": self.company_name,
            "company_website": self.company_website,
            "primary_color": self.primary_color,
            "accent_color": self.accent_color,
            "copyright_year": self.copyright_year,
        }


# Default branding - CUSTOMIZE THIS WITH YOUR LOGO AND COMPANY INFO
DEFAULT_BRANDING = BrandingConfig(
    app_name="Voice Cloner Pro",
    app_version="0.1.0",
    app_tagline="AI-Powered Voice Cloning for Music Production",
    company_name="Your Company Name",
    company_website="https://yourcompany.com",
    company_email="support@yourcompany.com",
    logo_path=Path("assets/logo.png"),
    icon_path=Path("assets/icon.ico"),
)


def get_branding() -> BrandingConfig:
    """Get branding configuration"""
    return DEFAULT_BRANDING


def set_branding(config: BrandingConfig):
    """Set custom branding configuration"""
    global DEFAULT_BRANDING
    DEFAULT_BRANDING = config


def get_logo_path() -> Optional[Path]:
    """Get logo path"""
    return get_branding().logo_path


def get_icon_path() -> Optional[Path]:
    """Get icon path"""
    return get_branding().icon_path


def get_app_title() -> str:
    """Get application title with version"""
    branding = get_branding()
    return f"{branding.app_name} v{branding.app_version}"


def get_about_text() -> str:
    """Get about dialog text"""
    branding = get_branding()
    return (
        f"{branding.app_name} v{branding.app_version}\n\n"
        f"{branding.app_tagline}\n\n"
        f"© {branding.copyright_year} {branding.company_name}\n"
        f"{branding.license_type} License\n\n"
        f"Website: {branding.company_website}\n"
        f"Support: {branding.support_url}"
    )


def get_stylesheet(theme: str = "dark") -> str:
    """Get styled stylesheet with custom branding colors"""
    branding = get_branding()
    r, g, b = branding.primary_color
    r_light, g_light, b_light = branding.primary_light
    acc_r, acc_g, acc_b = branding.accent_color
    
    primary_hex = f"#{r:02x}{g:02x}{b:02x}"
    primary_light_hex = f"#{r_light:02x}{g_light:02x}{b_light:02x}"
    accent_hex = f"#{acc_r:02x}{acc_g:02x}{acc_b:02x}"
    
    return f"""
        QMainWindow {{
            background-color: #2b2b2b;
            color: #ffffff;
        }}
        QLabel {{
            color: #ffffff;
        }}
        QPushButton {{
            background-color: {primary_hex};
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {primary_light_hex};
        }}
        QPushButton:pressed {{
            background-color: {primary_hex};
        }}
        QPushButton.primary {{
            background-color: {accent_hex};
            color: black;
        }}
        QPushButton.primary:hover {{
            background-color: #00ff00;
        }}
        QTextEdit {{
            background-color: #1e1e1e;
            color: #00ff00;
            border: 1px solid #3e3e3e;
            font-family: Courier;
        }}
        QProgressBar {{
            border: 1px solid #3e3e3e;
            border-radius: 4px;
            text-align: center;
            background-color: #1e1e1e;
        }}
        QProgressBar::chunk {{
            background-color: {accent_hex};
        }}
        QComboBox, QSpinBox, QDoubleSpinBox {{
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3e3e3e;
            padding: 4px;
        }}
    """
