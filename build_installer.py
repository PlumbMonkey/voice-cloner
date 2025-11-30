"""
Installer builder for Voice Cloner Desktop Application
Creates Windows, macOS, and Linux installers with custom branding
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess
import json


class InstallerBuilder:
    """Build installers for different platforms"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.dist_dir = project_root / "dist"
        self.build_dir = project_root / "build"
        self.src_dir = project_root / "src"

    def build_windows_installer(self, version: str = "0.1.0"):
        """Build Windows executable with PyInstaller"""
        print("🔨 Building Windows executable...")

        # Ensure assets exist
        assets_dir = self.project_root / "assets"
        if not assets_dir.exists():
            assets_dir.mkdir(parents=True)
            print(f"⚠️ Created {assets_dir}")
            print("   Add your logo.png and icon.ico to this folder!")

        # Build with PyInstaller
        spec_file = self.project_root / "build_desktop.spec"
        cmd = [sys.executable, "-m", "PyInstaller", str(spec_file)]

        try:
            result = subprocess.run(cmd, cwd=str(self.project_root), capture_output=True)
            if result.returncode == 0:
                print("✅ Windows executable built successfully!")
                exe_path = self.dist_dir / "VoiceCloner" / "VoiceCloner.exe"
                print(f"📦 Output: {exe_path}")
                return exe_path
            else:
                print("❌ Build failed!")
                print(result.stderr.decode())
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def build_windows_msi(self, version: str = "0.1.0"):
        """Build Windows MSI installer"""
        print("🔨 Building Windows MSI installer...")

        msi_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" Name="Voice Cloner Pro" Language="1033" Version="{version}"
             UpgradeCode="12345678-1234-1234-1234-123456789012">
        <Package InstallerVersion="200" Compressed="yes" />
        <Media Id="1" Cabinet="VoiceCloner.cab" EmbedCab="yes" />
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="Voice Cloner Pro" />
            </Directory>
        </Directory>
        <Feature Id="ProductFeature" Title="Voice Cloner Pro" Level="1">
            <ComponentRef Id="MainExecutable" />
        </Feature>
    </Product>
</Wix>"""

        print("⚠️ MSI installer requires WiX Toolset")
        print("   Download from: https://wixtoolset.org/releases/")
        print("   Or use NSIS for easier setup")

    def build_nsis_installer(self, version: str = "0.1.0"):
        """Generate NSIS installer script"""
        print("🔨 Generating NSIS installer script...")

        nsis_script = f"""
; Voice Cloner Pro Installer
; Generated with NSIS

!include "MUI2.nsh"

; Basic settings
Name "Voice Cloner Pro v{version}"
OutFile "VoiceCloner-Setup-{version}.exe"
InstallDir "$PROGRAMFILES\\VoiceCloner"
RequestExecutionLevel admin

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Installation files
Section "Install"
    SetOutPath "$INSTDIR"
    File /r "dist\\VoiceCloner\\*.*"
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\\Voice Cloner Pro"
    CreateShortCut "$SMPROGRAMS\\Voice Cloner Pro\\Voice Cloner.lnk" "$INSTDIR\\VoiceCloner.exe"
    CreateShortCut "$DESKTOP\\Voice Cloner Pro.lnk" "$INSTDIR\\VoiceCloner.exe"
SectionEnd

; Uninstaller
Section "Uninstall"
    RMDir /r "$INSTDIR"
    Delete "$SMPROGRAMS\\Voice Cloner Pro\\Voice Cloner.lnk"
    Delete "$DESKTOP\\Voice Cloner Pro.lnk"
    RMDir "$SMPROGRAMS\\Voice Cloner Pro"
SectionEnd
"""

        nsis_file = self.project_root / "VoiceCloner-Installer.nsi"
        with open(nsis_file, "w") as f:
            f.write(nsis_script)

        print(f"✅ NSIS script generated: {nsis_file}")
        print("   Install NSIS from: https://nsis.sourceforge.io/")
        print("   Then run: makensis VoiceCloner-Installer.nsi")

    def build_macos_app(self, version: str = "0.1.0"):
        """Build macOS app bundle"""
        print("🔨 Building macOS app bundle...")

        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            str(self.project_root / "build_desktop.spec"),
            "--osx-bundle-identifier",
            "com.voicecloner.pro",
        ]

        try:
            result = subprocess.run(cmd, cwd=str(self.project_root), capture_output=True)
            if result.returncode == 0:
                print("✅ macOS app bundle built successfully!")
                app_path = self.dist_dir / "VoiceCloner.app"
                print(f"📦 Output: {app_path}")
                return app_path
            else:
                print("❌ Build failed!")
                print(result.stderr.decode())
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def build_linux_package(self, version: str = "0.1.0"):
        """Generate Linux package files"""
        print("🔨 Generating Linux package files...")

        # AppImage configuration
        appimage_config = {
            "AppImage": {
                "path": "dist/VoiceCloner/VoiceCloner",
                "exe": "VoiceCloner",
            },
            "AppDir": {
                "path": "dist/VoiceCloner",
                "icon": "assets/icon.png",
                "desktop": "voicecloner.desktop",
            },
        }

        # Desktop entry file
        desktop_entry = f"""[Desktop Entry]
Type=Application
Name=Voice Cloner Pro
Exec=VoiceCloner %F
Icon=voicecloner
Categories=Audio;Multimedia;
"""

        desktop_file = self.project_root / "voicecloner.desktop"
        with open(desktop_file, "w") as f:
            f.write(desktop_entry)

        print(f"✅ Linux package files generated: {desktop_file}")
        print("   Install appimagetool to create AppImage")

    def create_installer_menu(self):
        """Display installer options menu"""
        print("\n" + "=" * 50)
        print("🚀 Voice Cloner Installer Builder")
        print("=" * 50)
        print("\nAvailable installer options:")
        print("1. Windows EXE (PyInstaller)")
        print("2. Windows MSI (WiX Toolset required)")
        print("3. Windows Installer Script (NSIS)")
        print("4. macOS App Bundle")
        print("5. Linux AppImage (experimental)")
        print("6. Build All")
        print("\n" + "=" * 50)

    def build_all(self, version: str = "0.1.0"):
        """Build all installers"""
        print(f"\n🚀 Building Voice Cloner v{version}...\n")

        # Windows
        if sys.platform == "win32":
            self.build_windows_installer(version)
            self.build_nsis_installer(version)
        # macOS
        elif sys.platform == "darwin":
            self.build_macos_app(version)
        # Linux
        elif sys.platform == "linux":
            self.build_linux_package(version)

        print("\n✅ Build process complete!")


def main():
    """Main entry point"""
    project_root = Path(__file__).parent
    builder = InstallerBuilder(project_root)

    builder.create_installer_menu()

    if len(sys.argv) > 1:
        option = sys.argv[1]
        version = sys.argv[2] if len(sys.argv) > 2 else "0.1.0"

        if option == "1":
            builder.build_windows_installer(version)
        elif option == "2":
            builder.build_windows_msi(version)
        elif option == "3":
            builder.build_nsis_installer(version)
        elif option == "4":
            builder.build_macos_app(version)
        elif option == "5":
            builder.build_linux_package(version)
        elif option == "6":
            builder.build_all(version)
        else:
            print("Invalid option")
    else:
        choice = input("Select option (1-6): ").strip()
        version = input("Enter version (default 0.1.0): ").strip() or "0.1.0"

        if choice == "1":
            builder.build_windows_installer(version)
        elif choice == "2":
            builder.build_windows_msi(version)
        elif choice == "3":
            builder.build_nsis_installer(version)
        elif choice == "4":
            builder.build_macos_app(version)
        elif choice == "5":
            builder.build_linux_package(version)
        elif choice == "6":
            builder.build_all(version)
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
