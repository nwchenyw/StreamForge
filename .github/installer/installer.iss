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

; Output configuration (outputs directly into installer/ directory under project root)
OutputDir=installer
OutputBaseFilename=StreamForge-Setup-v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=yes

; Support 64-bit installation
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequiredOverridesAllowed=commandline dialog

; App display in Windows Settings and Control Panel (應用程式與控制台一鍵正常解除安裝)
SetupIconFile=assets\app_icon.ico
CreateUninstallRegKey=yes
Uninstallable=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
CloseApplications=force
RestartApplications=no
ChangesAssociations=yes

[Languages]
Name: "chinesetraditional"; MessagesFile: ".github\installer\languages\ChineseTraditional.isl"; LicenseFile: ".github\installer\licenses\License_zh_TW.txt"
Name: "english"; MessagesFile: "compiler:Default.isl"; LicenseFile: ".github\installer\licenses\License_en.txt"
Name: "chinesesimplified"; MessagesFile: ".github\installer\languages\ChineseSimplified.isl"; LicenseFile: ".github\installer\licenses\License_zh_CN.txt"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"; LicenseFile: ".github\installer\licenses\License_ja.txt"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"; LicenseFile: ".github\installer\licenses\License_en.txt"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"; LicenseFile: ".github\installer\licenses\License_en.txt"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"; LicenseFile: ".github\installer\licenses\License_en.txt"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"; LicenseFile: ".github\installer\licenses\License_en.txt"

[CustomMessages]
chinesetraditional.CreateDesktopIcon=建立桌面捷徑 (&Create desktop shortcut)
chinesetraditional.LaunchProgram=立即啟動 StreamForge
chinesetraditional.AutoUpdate=啟用軟體啟動時自動檢查最新版本 (Enable auto-check for updates)
chinesetraditional.SettingsGroup=偏好設定 (Settings):
chinesetraditional.MaintenanceTitle=維護與安裝選項
chinesetraditional.MaintenanceSubTitle=偵測到本機已安裝相同版本的 StreamForge (v{#MyAppVersion})。
chinesetraditional.MaintenancePrompt=請選擇您要執行的作業：
chinesetraditional.MaintenanceReinstall=🔄 重新安裝 (Reinstall) - 完整重新安裝軟體並重新配置選項
chinesetraditional.MaintenanceRepair=🛠️ 修復安裝 (Repair) - 快速修復與還原程式檔案（保留個人偏好設定）
chinesetraditional.MaintenanceUninstall=🗑️ 移除軟體 (Uninstall) - 從本電腦中完整解除安裝 StreamForge
chinesetraditional.ConfirmUninstall=您確定要立即啟動解除安裝精靈，從電腦中移除 StreamForge 嗎？
chinesetraditional.RepairFinished=StreamForge 程式檔案已成功修復並還原！

english.CreateDesktopIcon=Create desktop shortcut
english.LaunchProgram=Launch StreamForge now
english.AutoUpdate=Enable auto-check for updates on startup
english.SettingsGroup=Settings:
english.MaintenanceTitle=Maintenance Options
english.MaintenanceSubTitle=Setup detected that StreamForge (v{#MyAppVersion}) is already installed on your system.
english.MaintenancePrompt=Please select the operation you want to perform:
english.MaintenanceReinstall=🔄 Reinstall - Reinstall all files and reconfigure options
english.MaintenanceRepair=🛠️ Repair - Restore and repair missing or corrupted files (preserves user settings)
english.MaintenanceUninstall=🗑️ Uninstall - Completely remove StreamForge from this computer
english.ConfirmUninstall=Are you sure you want to launch the uninstaller and remove StreamForge from your computer?
english.RepairFinished=StreamForge program files have been successfully repaired and restored!

chinesesimplified.CreateDesktopIcon=创建桌面快捷方式 (&Create desktop shortcut)
chinesesimplified.LaunchProgram=立即启动 StreamForge
chinesesimplified.AutoUpdate=启用软件启动时自动检查最新版本 (Enable auto-check for updates)
chinesesimplified.SettingsGroup=偏好设置 (Settings):
chinesesimplified.MaintenanceTitle=维护与安装选项
chinesesimplified.MaintenanceSubTitle=检测到本机已安装相同版本的 StreamForge (v{#MyAppVersion})。
chinesesimplified.MaintenancePrompt=请选择您要执行的操作：
chinesesimplified.MaintenanceReinstall=🔄 重新安装 (Reinstall) - 完整重新安装软件并重新配置选项
chinesesimplified.MaintenanceRepair=🛠️ 修复安装 (Repair) - 快速修复与还原程序文件（保留个人偏好设置）
chinesesimplified.MaintenanceUninstall=🗑️ 卸载软件 (Uninstall) - 从本电脑中完整卸载 StreamForge
chinesesimplified.ConfirmUninstall=您确定要立即启动卸载向导，从计算机中移除 StreamForge 吗？
chinesesimplified.RepairFinished=StreamForge 程序文件已成功修复并还原！

japanese.CreateDesktopIcon=デスクトップにショートカットを作成する (&Create desktop shortcut)
japanese.LaunchProgram=StreamForge を今すぐ起動
japanese.AutoUpdate=起動時に最新バージョンの更新を自動確認する (Enable auto-check for updates)
japanese.SettingsGroup=設定 (Settings):
japanese.MaintenanceTitle=メンテナンスオプション
japanese.MaintenanceSubTitle=同じバージョンの StreamForge (v{#MyAppVersion}) が既にインストールされています。
japanese.MaintenancePrompt=実行する操作を選択してください：
japanese.MaintenanceReinstall=🔄 再インストール (Reinstall) - すべてのファイルを再インストールし、設定を再構成します
japanese.MaintenanceRepair=🛠️ 修復 (Repair) - 破損または欠落しているファイルを修復・復元します（設定を保持）
japanese.MaintenanceUninstall=🗑️ アンインストール (Uninstall) - コンピューターから StreamForge を完全に削除します
japanese.ConfirmUninstall=アンインストーラーを起動して StreamForge をコンピューターから削除してもよろしいですか？
japanese.RepairFinished=StreamForge プログラムファイルは正常に修復および復元されました！

korean.CreateDesktopIcon=바탕 화면 바로가기 만들기 (&Create desktop shortcut)
korean.LaunchProgram=지금 StreamForge 실행
korean.AutoUpdate=시작 시 최신 버전 자동 업데이트 확인 (Enable auto-check for updates)
korean.SettingsGroup=기본 설정 (Settings):
korean.MaintenanceTitle=유지 관리 옵션
korean.MaintenanceSubTitle=동일한 버전의 StreamForge (v{#MyAppVersion})가 이미 설치되어 있습니다.
korean.MaintenancePrompt=수행할 작업을 선택하십시오:
korean.MaintenanceReinstall=🔄 재설치 (Reinstall) - 모든 파일을 다시 설치하고 설정을 재구성합니다
korean.MaintenanceRepair=🛠️ 복구 (Repair) - 프로그램 파일을 빠르게 복구 및 복원합니다（설정 유지）
korean.MaintenanceUninstall=🗑️ 제거 (Uninstall) - 컴퓨터에서 StreamForge를 완전히 제거합니다
korean.ConfirmUninstall=제거 프로그램을 시작하여 컴퓨터에서 StreamForge를 제거하시겠습니까?
korean.RepairFinished=StreamForge 프로그램 파일이 성공적으로 복구 및 복원되었습니다!

spanish.CreateDesktopIcon=Crear un acceso directo en el escritorio (&Create desktop shortcut)
spanish.LaunchProgram=Iniciar StreamForge ahora
spanish.AutoUpdate=Comprobar actualizaciones automáticamente al iniciar (Enable auto-check for updates)
spanish.SettingsGroup=Configuración (Settings):
spanish.MaintenanceTitle=Opciones de mantenimiento
spanish.MaintenanceSubTitle=Se ha detectado la misma versión de StreamForge (v{#MyAppVersion}) ya instalada.
spanish.MaintenancePrompt=Seleccione la operación que desea realizar:
spanish.MaintenanceReinstall=🔄 Reinstalar - Reinstalar todos los archivos y reconfigurar las opciones
spanish.MaintenanceRepair=🛠️ Reparar - Reparar y restaurar archivos dañados（conserva su configuración）
spanish.MaintenanceUninstall=🗑️ Desinstalar - Desinstalar completamente StreamForge del equipo
spanish.ConfirmUninstall=¿Está seguro de que desea iniciar el desinstalador y eliminar StreamForge del equipo?
spanish.RepairFinished=¡Los archivos de StreamForge se han reparado y restaurado correctamente!

french.CreateDesktopIcon=Créer un raccourci sur le Bureau (&Create desktop shortcut)
french.LaunchProgram=Lancer StreamForge maintenant
french.AutoUpdate=Vérifier automatiquement les mises à jour au démarrage (Enable auto-check for updates)
french.SettingsGroup=Paramètres (Settings):
french.MaintenanceTitle=Options de maintenance
french.MaintenanceSubTitle=La même version de StreamForge (v{#MyAppVersion}) est déjà installée sur votre ordinateur.
french.MaintenancePrompt=Veuillez sélectionner l'opération à effectuer :
french.MaintenanceReinstall=🔄 Réinstaller - Réinstaller tous les fichiers et reconfigurer les options
french.MaintenanceRepair=🛠️ Réparer - Réparer et restaurer les fichiers endommagés（conserve vos paramètres）
french.MaintenanceUninstall=🗑️ Désinstaller - Supprimer complètement StreamForge de cet ordinateur
french.ConfirmUninstall=Êtes-vous sûr de vouloir lancer le désinstallateur et supprimer StreamForge de cet ordinateur ?
french.RepairFinished=Les fichiers du programme StreamForge ont été réparés et restaurés avec succès !

german.CreateDesktopIcon=Desktop-Verknüpfung erstellen (&Create desktop shortcut)
german.LaunchProgram=StreamForge jetzt starten
german.AutoUpdate=Beim Programmstart automatisch nach Updates suchen (Enable auto-check for updates)
german.SettingsGroup=Einstellungen (Settings):
german.MaintenanceTitle=Wartungsoptionen
german.MaintenanceSubTitle=Dieselbe Version von StreamForge (v{#MyAppVersion}) ist bereits installiert.
german.MaintenancePrompt=Bitte wählen Sie die auszuführende Aktion:
german.MaintenanceReinstall=🔄 Neu installieren - Alle Dateien neu installieren und Optionen konfigurieren
german.MaintenanceRepair=🛠️ Reparieren - Dateien reparieren und wiederherstellen（Einstellungen beibehalten）
german.MaintenanceUninstall=🗑️ Deinstallieren - StreamForge vollständig von diesem Computer entfernen
german.ConfirmUninstall=Möchten Sie das Deinstallationsprogramm wirklich starten und StreamForge von Ihrem Computer entfernen?
german.RepairFinished=StreamForge-Programmdateien wurden erfolgreich repariert und wiederhergestellt!

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "autoupdate"; Description: "{cm:AutoUpdate}"; GroupDescription: "{cm:SettingsGroup}"; Flags: checkedonce

[Files]
; Copy all files from PyInstaller dist directory
Source: "dist\StreamForge\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram}"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
; 解除安裝時徹底清理所有運行生成的快取與資料夾，不殘留任何垃圾檔案
Type: filesandordirs; Name: "{app}\_internal"
Type: filesandordirs; Name: "{app}\ffmpeg_bin"
Type: filesandordirs; Name: "{app}\assets"
Type: filesandordirs; Name: "{app}\downloads"
Type: files; Name: "{app}\*.*"
Type: dirifempty; Name: "{app}"

[Code]
procedure ExitProcess(uExitCode: Integer); external 'ExitProcess@kernel32.dll stdcall';

var
  MaintenancePage: TInputOptionWizardPage;
  IsAlreadyInstalled: Boolean;
  IsRepairMode: Boolean;
  IsReinstallMode: Boolean;
  ExistingInstallDir: string;
  ExistingUninstallExe: string;
  InstalledVersion: string;

function DetectExistingInstallation(): Boolean;
var
  RegKey: string;
  UninstStr: string;
begin
  Result := False;
  RegKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1';
  InstalledVersion := '';
  ExistingInstallDir := '';
  UninstStr := '';

  if IsWin64 and RegKeyExists(HKLM64, RegKey) then
  begin
    RegQueryStringValue(HKLM64, RegKey, 'DisplayVersion', InstalledVersion);
    RegQueryStringValue(HKLM64, RegKey, 'InstallLocation', ExistingInstallDir);
    RegQueryStringValue(HKLM64, RegKey, 'UninstallString', UninstStr);
    Result := True;
  end
  else if RegKeyExists(HKLM32, RegKey) then
  begin
    RegQueryStringValue(HKLM32, RegKey, 'DisplayVersion', InstalledVersion);
    RegQueryStringValue(HKLM32, RegKey, 'InstallLocation', ExistingInstallDir);
    RegQueryStringValue(HKLM32, RegKey, 'UninstallString', UninstStr);
    Result := True;
  end
  else if RegKeyExists(HKCU, RegKey) then
  begin
    RegQueryStringValue(HKCU, RegKey, 'DisplayVersion', InstalledVersion);
    RegQueryStringValue(HKCU, RegKey, 'InstallLocation', ExistingInstallDir);
    RegQueryStringValue(HKCU, RegKey, 'UninstallString', UninstStr);
    Result := True;
  end;

  if Result then
  begin
    ExistingUninstallExe := RemoveQuotes(UninstStr);
    if (ExistingInstallDir = '') and FileExists(ExistingUninstallExe) then
      ExistingInstallDir := ExtractFilePath(ExistingUninstallExe);
    if not FileExists(ExistingUninstallExe) and (ExistingInstallDir <> '') then
    begin
      if FileExists(AddBackslash(ExistingInstallDir) + 'unins000.exe') then
        ExistingUninstallExe := AddBackslash(ExistingInstallDir) + 'unins000.exe';
    end;
  end;
end;

procedure InitializeWizard();
begin
  IsRepairMode := False;
  IsReinstallMode := False;
  IsAlreadyInstalled := DetectExistingInstallation() and (InstalledVersion = '{#MyAppVersion}');

  MaintenancePage := CreateInputOptionPage(
    wpWelcome,
    CustomMessage('MaintenanceTitle'),
    CustomMessage('MaintenanceSubTitle'),
    CustomMessage('MaintenancePrompt'),
    True, False);

  MaintenancePage.Add(CustomMessage('MaintenanceReinstall'));
  MaintenancePage.Add(CustomMessage('MaintenanceRepair'));
  MaintenancePage.Add(CustomMessage('MaintenanceUninstall'));
  MaintenancePage.SelectedValueIndex := 0;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;

  if PageID = MaintenancePage.ID then
  begin
    if not IsAlreadyInstalled then
      Result := True;
    Exit;
  end;

  if IsAlreadyInstalled and IsRepairMode then
  begin
    if (PageID = wpLicense) or (PageID = wpSelectDir) or 
       (PageID = wpSelectProgramGroup) or (PageID = wpSelectTasks) then
    begin
      Result := True;
      Exit;
    end;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  if CurPageID = MaintenancePage.ID then
  begin
    case MaintenancePage.SelectedValueIndex of
      0: // Reinstall
      begin
        IsReinstallMode := True;
        IsRepairMode := False;
        if ExistingInstallDir <> '' then
          WizardForm.DirEdit.Text := ExistingInstallDir;
      end;
      1: // Repair
      begin
        IsRepairMode := True;
        IsReinstallMode := False;
        if ExistingInstallDir <> '' then
          WizardForm.DirEdit.Text := ExistingInstallDir;
      end;
      2: // Uninstall
      begin
        if MsgBox(CustomMessage('ConfirmUninstall'), mbConfirmation, MB_YESNO) = IDYES then
        begin
          if FileExists(ExistingUninstallExe) then
            Exec(ExistingUninstallExe, '', '', SW_SHOW, ewNoWait, ResultCode)
          else
            MsgBox('Cannot find uninstaller: ' + ExistingUninstallExe, mbError, MB_OK);
          ExitProcess(0);
        end;
        Result := False;
        Exit;
      end;
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ConfigDir: string;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    ConfigDir := ExpandConstant('{userappdata}\StreamForge');
    if DirExists(ConfigDir) then
      DelTree(ConfigDir, True, True, True);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigDir, ConfigPath, ConfigContent: string;
  AutoUpdateVal, LangCode: string;
begin
  if CurStep = ssPostInstall then
  begin
    ConfigDir := ExpandConstant('{userappdata}\StreamForge');
    ConfigPath := ConfigDir + '\config.json';
    
    // In repair mode, preserve existing config if present
    if not (IsRepairMode and FileExists(ConfigPath)) then
    begin
      if WizardIsTaskSelected('autoupdate') then
        AutoUpdateVal := 'true'
      else
        AutoUpdateVal := 'false';

      case ActiveLanguage of
        'chinesetraditional': LangCode := 'zh_TW';
        'chinesesimplified': LangCode := 'zh_CN';
        'japanese': LangCode := 'ja_JP';
        'korean': LangCode := 'ko_KR';
        'spanish': LangCode := 'es_ES';
        'french': LangCode := 'fr_FR';
        'german': LangCode := 'de_DE';
        'english': LangCode := 'en_US';
      else
        LangCode := 'zh_TW';
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

    if IsRepairMode then
    begin
      MsgBox(CustomMessage('RepairFinished'), mbInformation, MB_OK);
    end;
  end;
end;
