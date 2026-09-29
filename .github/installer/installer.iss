; =====================================================================
; StreamForge Inno Setup Script
; Professional Windows Installer Builder
; =====================================================================

#define MyAppName "StreamForge"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "The StreamForge Team & Contributors"
#define MyAppURL "https://github.com/nwchenyw/StreamForge"
#define MyAppExeName "StreamForge.exe"

[Setup]
; Unique application GUID for clean upgrades and uninstallation
AppId={{9F82A4C1-3E2B-4A68-9B7E-7B93F678E201}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}/releases

; Base source directory is project root
SourceDir=..\..

; Allow user to choose any directory or USB drive
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=no
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=no

; MIT License Page
LicenseFile=LICENSE

; Output configuration (outputs directly into installer/ directory under project root)
OutputDir=installer
OutputBaseFilename=StreamForge-Setup-v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; Support 64-bit installation
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequiredOverridesAllowed=commandline dialog

; App display in Windows Add/Remove Programs
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName} v{#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
english.CreateDesktopIcon=建立桌面捷徑 (Create desktop shortcut)
english.LaunchProgram=立即啟動 StreamForge

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autoupdate"; Description: "啟用軟體啟動時自動檢查最新版本 (Enable auto-check for updates)"; GroupDescription: "更新與偏好設定 (Settings):"; Flags: checkedonce

[Files]
; Copy all files from PyInstaller dist directory
Source: "dist\StreamForge\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: postinstall nowait skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigDir, ConfigPath, ConfigContent: string;
  AutoUpdateVal: string;
begin
  if CurStep = ssPostInstall then
  begin
    ConfigDir := ExpandConstant('{userappdata}\StreamForge');
    ConfigPath := ConfigDir + '\config.json';
    if WizardIsTaskSelected('autoupdate') then
      AutoUpdateVal := 'true'
    else
      AutoUpdateVal := 'false';

    if not DirExists(ConfigDir) then
      ForceDirectories(ConfigDir);

    if not FileExists(ConfigPath) then
    begin
      ConfigContent := '{' + #13#10 +
        '  "auto_check_update": ' + AutoUpdateVal + ',' + #13#10 +
        '  "install_date": "' + GetDateTimeString('yyyy/mm/dd hh:nn', '-', ':') + '",' + #13#10 +
        '  "preferred_format": "mp3"' + #13#10 +
        '}';
      SaveStringToFile(ConfigPath, ConfigContent, False);
    end;
  end;
end;
