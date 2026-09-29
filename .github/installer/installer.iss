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
Name: "chinesetraditional"; MessagesFile: ".github\installer\languages\ChineseTraditional.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: ".github\installer\languages\ChineseSimplified.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[CustomMessages]
chinesetraditional.CreateDesktopIcon=建立桌面捷徑 (&Create desktop shortcut)
chinesetraditional.LaunchProgram=立即啟動 StreamForge
chinesetraditional.AutoUpdate=啟用軟體啟動時自動檢查最新版本 (Enable auto-check for updates)
chinesetraditional.SettingsGroup=偏好設定 (Settings):

english.CreateDesktopIcon=Create desktop shortcut
english.LaunchProgram=Launch StreamForge now
english.AutoUpdate=Enable auto-check for updates on startup
english.SettingsGroup=Settings:

chinesesimplified.CreateDesktopIcon=创建桌面快捷方式 (&Create desktop shortcut)
chinesesimplified.LaunchProgram=立即启动 StreamForge
chinesesimplified.AutoUpdate=启用软件启动时自动检查最新版本 (Enable auto-check for updates)
chinesesimplified.SettingsGroup=偏好设置 (Settings):

japanese.CreateDesktopIcon=デスクトップにショートカットを作成する (&Create desktop shortcut)
japanese.LaunchProgram=StreamForge を今すぐ起動
japanese.AutoUpdate=起動時に最新バージョンの更新を自動確認する (Enable auto-check for updates)
japanese.SettingsGroup=設定 (Settings):

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autoupdate"; Description: "{cm:AutoUpdate}"; GroupDescription: "{cm:SettingsGroup}"; Flags: checkedonce

[Files]
; Copy all files from PyInstaller dist directory
Source: "dist\StreamForge\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram}"; Flags: postinstall nowait skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigDir, ConfigPath, ConfigContent: string;
  AutoUpdateVal, LangCode: string;
begin
  if CurStep = ssPostInstall then
  begin
    ConfigDir := ExpandConstant('{userappdata}\StreamForge');
    ConfigPath := ConfigDir + '\config.json';
    if WizardIsTaskSelected('autoupdate') then
      AutoUpdateVal := 'true'
    else
      AutoUpdateVal := 'false';

    case ActiveLanguage of
      'chinesetraditional': LangCode := 'zh_TW';
      'chinesesimplified': LangCode := 'zh_CN';
      'japanese': LangCode := 'ja_JP';
    else
      LangCode := 'en_US';
    end;

    if not DirExists(ConfigDir) then
      ForceDirectories(ConfigDir);

    ConfigContent := '{' + #13#10 +
      '  "language": "' + LangCode + '",' + #13#10 +
      '  "auto_check_update": ' + AutoUpdateVal + ',' + #13#10 +
      '  "install_date": "' + GetDateTimeString('yyyy/mm/dd hh:nn', '-', ':') + '",' + #13#10 +
      '  "preferred_format": "mp3"' + #13#10 +
      '}';
    SaveStringToFile(ConfigPath, ConfigContent, False);
  end;
end;
