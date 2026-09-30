; =====================================================================
; StreamForge Inno Setup Script
; Professional Windows Installer Builder
; =====================================================================

#define MyAppName "StreamForge"
#define MyAppVersion "1.1.0"
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
UninstallDisplayIcon={app}\assets\app_icon.ico
UninstallDisplayName={#MyAppName}
CloseApplications=no
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
chinesetraditional.AppRunningUninstallPrompt=偵測到 StreamForge 正在執行中！%n%n為了安全解除安裝，必須先關閉正在運行的程式。%n請問您是否要立即中斷並關閉 StreamForge？%n%n• 點選【是 (Yes)】：關閉程式並繼續解除安裝%n• 點選【否 (No)】：取消解除安裝（不中斷就不刪除任何檔案）
chinesetraditional.UninstallAbortedByUser=您已取消解除安裝。StreamForge 仍保持完整，未刪除任何檔案。
chinesetraditional.AppRunningSetupPrompt=偵測到 StreamForge 正在執行中！%n%n安裝程式需要先關閉正在運行的程式才能繼續更新或安裝檔案。%n請問您是否要立即中斷並關閉 StreamForge？%n%n• 點選【是 (Yes)】：關閉程式並繼續安裝%n• 點選【否 (No)】：取消安裝
chinesetraditional.UpgradePrompt=偵測到您的電腦中已安裝舊版 StreamForge (版本: %1)！%n%n本安裝精靈將為您直接升級更新至最新版本 (v%2)。%n安裝路徑：%3%n（您的個人偏好設定、下載檔案與紀錄將完整保留）%n%n請問您是否要立即升級更新？%n%n• 點選【是 (Yes)】：立即升級至 v%2%n• 點選【否 (No)】：取消安裝並結束
chinesetraditional.UpgradeFinished=StreamForge 已成功升級更新至最新版本 (v{#MyAppVersion})！

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
english.AppRunningUninstallPrompt=StreamForge is currently running!%n%nTo uninstall safely, the running application must be closed.%nWould you like to terminate StreamForge now?%n%n• Click [Yes]: Close the application and proceed with uninstallation%n• Click [No]: Cancel uninstallation (no files will be deleted)
english.UninstallAbortedByUser=Uninstallation cancelled. StreamForge remains intact and no files were deleted.
english.AppRunningSetupPrompt=StreamForge is currently running!%n%nSetup needs to close the running application to update or install files.%nWould you like to terminate StreamForge now?%n%n• Click [Yes]: Close the application and continue setup%n• Click [No]: Cancel setup
english.UpgradePrompt=Setup detected an earlier version of StreamForge (v%1) on your system!%n%nThis setup will upgrade it directly to the latest version (v%2).%nInstall Location: %3%n(Your settings and downloaded files will be preserved)%n%nWould you like to upgrade now?%n%n• Click [Yes]: Upgrade to v%2%n• Click [No]: Cancel and exit setup
english.UpgradeFinished=StreamForge has been successfully upgraded to the latest version (v{#MyAppVersion})!

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
chinesesimplified.AppRunningUninstallPrompt=检测到 StreamForge 正在运行中！%n%n为了安全卸载，必须先关闭正在运行的程序。%n请问您是否要立即中断并关闭 StreamForge？%n%n• 点击【是 (Yes)】：关闭程序并继续卸载%n• 点击【否 (No)】：取消卸载（不中断就不删除任何文件）
chinesesimplified.UninstallAbortedByUser=您已取消卸载。StreamForge 仍保持完整，未删除任何文件。
chinesesimplified.AppRunningSetupPrompt=检测到 StreamForge 正在运行中！%n%n安装程序需要先关闭正在运行的程序才能继续更新或安装文件。%n请问您是否要立即中断并关闭 StreamForge？%n%n• 点击【是 (Yes)】：关闭程序并继续安装%n• 点击【否 (No)】：取消安装
chinesesimplified.UpgradePrompt=检测到您的计算机中已安装旧版 StreamForge (版本: %1)！%n%n本安装向导将为您直接升级更新至最新版本 (v%2)。%n安装路径：%3%n（您的个人偏好设置、下载文件与记录将完整保留）%n%n请问您是否要立即升级更新？%n%n• 点击【是 (Yes)】：立即升级至 v%2%n• 点击【否 (No)】：取消安装并退出
chinesesimplified.UpgradeFinished=StreamForge 已成功升级更新至最新版本 (v{#MyAppVersion})！

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
japanese.AppRunningUninstallPrompt=StreamForge が現在実行中です！%n%n安全にアンインストールするには、実行中のアプリケーションを終了する必要があります。%nStreamForge を今すぐ終了しますか？%n%n• [はい (Yes)] をクリック：アプリを終了してアンインストールを続行します%n• [いいえ (No)] をクリック：アンインストールをキャンセルします（ファイルは削除されません）
japanese.UninstallAbortedByUser=アンインストールはキャンセルされました。StreamForge はそのまま保持され、ファイルは削除されていません。
japanese.AppRunningSetupPrompt=StreamForge が現在実行中です！%n%nファイルを更新またはインストールするには、実行中のアプリを閉じる必要があります。%nStreamForge を今すぐ終了しますか？%n%n• [はい (Yes)] をクリック：アプリを終了してインストールを続行します%n• [いいえ (No)] をクリック：インストールをキャンセルします
japanese.UpgradePrompt=コンピューターに以前のバージョンの StreamForge (v%1) が検出されました！%n%n最新バージョン (v%2) へ直接アップグレードします。%nインストール先：%3%n（設定とダウンロードファイルは保持されます）%n%n今すぐアップグレードしますか？%n%n• [はい (Yes)] をクリック：v%2 へアップグレード%n• [いいえ (No)] をクリック：キャンセルして終了
japanese.UpgradeFinished=StreamForge は最新バージョン (v{#MyAppVersion}) に正常にアップグレードされました！

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
korean.AppRunningUninstallPrompt=StreamForge가 현재 실행 중입니다!%n%n안전하게 제거하려면 실행 중인 응용 프로그램을 닫아야 합니다.%n지금 StreamForge를 종료하시겠습니까?%n%n• [예 (Yes)] 클릭: 앱을 종료하고 제거를 계속합니다%n• [아니요 (No)] 클릭: 제거를 취소합니다 (파일이 삭제되지 않습니다)
korean.UninstallAbortedByUser=제거가 취소되었습니다. StreamForge는 그대로 유지되며 파일이 삭제되지 않았습니다.
korean.AppRunningSetupPrompt=StreamForge가 현재 실행 중입니다!%n%n파일을 업데이트하거나 설치하려면 실행 중인 앱을 닫아야 합니다.%n지금 StreamForge를 종료하시겠습니까?%n%n• [예 (Yes)] 클릭: 앱을 종료하고 설치를 계속합니다%n• [아니요 (No)] 클릭: 설치를 취소합니다
korean.UpgradePrompt=컴퓨터에 이전 버전의 StreamForge (v%1)가 설치되어 있습니다!%n%n최신 버전 (v%2)으로 즉시 업그레이드합니다.%n설치 경로: %3%n(사용자 설정 및 다운로드 파일은 유지됩니다)%n%n지금 업그레이드하시겠습니까?%n%n• [예 (Yes)] 클릭: v%2(으)로 업그레이드%n• [아니요 (No)] 클릭: 취소하고 종료
korean.UpgradeFinished=StreamForge가 최신 버전 (v{#MyAppVersion})으로 성공적으로 업그레이드되었습니다!

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
spanish.AppRunningUninstallPrompt=¡StreamForge se está ejecutando actualmente!%n%nPara desinstalar de forma segura, se debe cerrar la aplicación en ejecución.%n¿Desea cerrar StreamForge ahora?%n%n• Haga clic en [Sí]: Cerrar la aplicación y continuar con la desinstalación%n• Haga clic en [No]: Cancelar la desinstalación (no se eliminará ningún archivo)
spanish.UninstallAbortedByUser=Desinstalación cancelada. StreamForge permanece intacto y no se eliminaron archivos.
spanish.AppRunningSetupPrompt=¡StreamForge se está ejecutando actualmente!%n%nEl instalador necesita cerrar la aplicación para actualizar o instalar archivos.%n¿Desea cerrar StreamForge ahora?%n%n• Haga clic en [Sí]: Cerrar la aplicación y continuar con la instalación%n• Haga clic en [No]: Cancelar la instalación
spanish.UpgradePrompt=¡Se ha detectado una versión anterior de StreamForge (v%1) en el equipo!%n%nEste instalador actualizará directamente a la última versión (v%2).%nRuta de instalación: %3%n(Su configuración y archivos descargados se conservarán)%n%n¿Desea actualizar ahora?%n%n• Haga clic en [Sí]: Actualizar a v%2%n• Haga clic en [No]: Cancelar y salir
spanish.UpgradeFinished=¡StreamForge se ha actualizado correctamente a la última versión (v{#MyAppVersion})!

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
french.AppRunningUninstallPrompt=StreamForge est actuellement en cours d'exécution !%n%nPour désinstaller en toute sécurité, l'application doit être fermée.%nVoulez-vous fermer StreamForge maintenant ?%n%n• Cliquez sur [Oui] : Fermer l'application et poursuivre la désinstallation%n• Cliquez sur [Non] : Annuler la désinstallation (aucun fichier ne sera supprimé)
french.UninstallAbortedByUser=Désinstallation annulée. StreamForge reste intact et aucun fichier n'a été supprimé.
french.AppRunningSetupPrompt=StreamForge est actuellement en cours d'exécution !%n%nL'assistant d'installation doit fermer l'application pour mettre à jour ou installer des fichiers.%nVoulez-vous fermer StreamForge maintenant ?%n%n• Cliquez sur [Oui] : Fermer l'application et continuer l'installation%n• Cliquez sur [Non] : Annuler l'installation
french.UpgradePrompt=Une version antérieure de StreamForge (v%1) a été détectée sur votre ordinateur !%n%nCet assistant va mettre à niveau vers la dernière version (v%2).%nEmplacement d'installation : %3%n(Vos paramètres et fichiers téléchargés seront conservés)%n%nSouhaitez-vous effectuer la mise à niveau maintenant ?%n%n• Cliquez sur [Oui] : Mettre à niveau vers v%2%n• Cliquez sur [Non] : Annuler et quitter
french.UpgradeFinished=StreamForge a été mis à niveau avec succès vers la dernière version (v{#MyAppVersion}) !

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
german.AppRunningUninstallPrompt=StreamForge wird derzeit ausgeführt!%n%nUm sicher zu deinstallieren, muss die ausgeführte Anwendung geschlossen werden.%nMöchten Sie StreamForge jetzt beenden?%n%n• Klicken Sie auf [Ja]: Anwendung beenden und mit der Deinstallation fortfahren%n• Klicken Sie auf [Nein]: Deinstallation abbrechen (es werden keine Dateien gelöscht)
german.UninstallAbortedByUser=Deinstallation abgebrochen. StreamForge bleibt unverändert und es wurden keine Dateien gelöscht.
german.AppRunningSetupPrompt=StreamForge wird derzeit ausgeführt!%n%nDas Setup muss die laufende Anwendung schließen, um Dateien zu aktualisieren oder zu installieren.%nMöchten Sie StreamForge jetzt beenden?%n%n• Klicken Sie auf [Ja]: Anwendung beenden und mit dem Setup fortfahren%n• Klicken Sie auf [Nein]: Setup abbrechen
german.UpgradePrompt=Es wurde eine frühere Version von StreamForge (v%1) auf Ihrem Computer erkannt!%n%nDieses Setup wird Sie direkt auf die neueste Version (v%2) aktualisieren.%nInstallationspfad: %3%n(Ihre Einstellungen und heruntergeladenen Dateien bleiben erhalten)%n%nMöchten Sie jetzt aktualisieren?%n%n• Klicken Sie auf [Ja]: Auf v%2 aktualisieren%n• Klicken Sie auf [Nein]: Abbrechen und beenden
german.UpgradeFinished=StreamForge wurde erfolgreich auf die neueste Version (v{#MyAppVersion}) aktualisiert!

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "autoupdate"; Description: "{cm:AutoUpdate}"; GroupDescription: "{cm:SettingsGroup}"; Flags: checkedonce

[Files]
; Copy all files from PyInstaller dist directory
Source: "dist\StreamForge\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_icon.ico"; Tasks: desktopicon

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

[Registry]
Root: HKA; Subkey: "Software\Classes\.sfpl"; ValueType: string; ValueName: ""; ValueData: "StreamForge.Playlist"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\StreamForge.Playlist"; ValueType: string; ValueName: ""; ValueData: "StreamForge Playlist File"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\StreamForge.Playlist\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\assets\app_icon.ico,0"
Root: HKA; Subkey: "Software\Classes\StreamForge.Playlist\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Code]
procedure ExitProcess(uExitCode: Integer); external 'ExitProcess@kernel32.dll stdcall';

function IsAppRunning(): Boolean;
var
  ResultCode: Integer;
begin
  if Exec('cmd.exe', '/c tasklist /FI "IMAGENAME eq {#MyAppExeName}" 2>nul | find /i "{#MyAppExeName}" >nul', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    Result := (ResultCode = 0)
  else
    Result := False;
end;

procedure KillApp();
var
  ResultCode: Integer;
  WaitCount: Integer;
begin
  Exec('taskkill.exe', '/f /im {#MyAppExeName} /im ffmpeg.exe /im ffprobe.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  WaitCount := 0;
  while IsAppRunning and (WaitCount < 15) do
  begin
    Sleep(200);
    WaitCount := WaitCount + 1;
  end;
end;

function InitializeSetup(): Boolean;
var
  PromptMsg: string;
begin
  Result := True;
  if IsAppRunning then
  begin
    PromptMsg := CustomMessage('AppRunningSetupPrompt');
    if MsgBox(PromptMsg, mbConfirmation, MB_YESNO) = IDYES then
    begin
      KillApp;
      Result := True;
    end
    else
    begin
      Result := False;
      Exit;
    end;
  end;
end;

function InitializeUninstall(): Boolean;
var
  PromptMsg: string;
begin
  Result := True;
  if IsAppRunning then
  begin
    PromptMsg := CustomMessage('AppRunningUninstallPrompt');
    if MsgBox(PromptMsg, mbConfirmation, MB_YESNO) = IDYES then
    begin
      KillApp;
      Result := True;
    end
    else
    begin
      MsgBox(CustomMessage('UninstallAbortedByUser'), mbInformation, MB_OK);
      Result := False;
      Exit;
    end;
  end;
end;

var
  MaintenancePage: TInputOptionWizardPage;
  IsAlreadyInstalled: Boolean;
  IsUpgradeMode: Boolean;
  IsRepairMode: Boolean;
  IsReinstallMode: Boolean;
  ExistingInstallDir: string;
  ExistingUninstallExe: string;
  InstalledVersion: string;

function ParseVersionPart(var S: string): Integer;
var
  DotPos: Integer;
  PartStr: string;
begin
  DotPos := Pos('.', S);
  if DotPos > 0 then
  begin
    PartStr := Copy(S, 1, DotPos - 1);
    S := Copy(S, DotPos + 1, Length(S));
  end
  else
  begin
    PartStr := S;
    S := '';
  end;
  Result := StrToIntDef(PartStr, 0);
end;

function CompareVersion(V1, V2: string): Integer;
var
  Num1, Num2: Integer;
  CleanV1, CleanV2: string;
begin
  Result := 0;
  CleanV1 := V1;
  CleanV2 := V2;
  if (Length(CleanV1) > 0) and ((CleanV1[1] = 'v') or (CleanV1[1] = 'V')) then
    CleanV1 := Copy(CleanV1, 2, Length(CleanV1));
  if (Length(CleanV2) > 0) and ((CleanV2[1] = 'v') or (CleanV2[1] = 'V')) then
    CleanV2 := Copy(CleanV2, 2, Length(CleanV2));

  while (CleanV1 <> '') or (CleanV2 <> '') do
  begin
    Num1 := ParseVersionPart(CleanV1);
    Num2 := ParseVersionPart(CleanV2);
    if Num1 < Num2 then
    begin
      Result := -1;
      Exit;
    end
    else if Num1 > Num2 then
    begin
      Result := 1;
      Exit;
    end;
  end;
end;

function DetectExistingInstallation(): Boolean;
var
  RegKey, RegKey2: string;
  UninstStr: string;
  CandidateDir: string;
begin
  Result := False;
  RegKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{9F82A4C1-3E2B-4A68-9B7E-7B93F678E201}_is1';
  RegKey2 := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\StreamForge_is1';
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
  end
  else if IsWin64 and RegKeyExists(HKLM64, RegKey2) then
  begin
    RegQueryStringValue(HKLM64, RegKey2, 'DisplayVersion', InstalledVersion);
    RegQueryStringValue(HKLM64, RegKey2, 'InstallLocation', ExistingInstallDir);
    RegQueryStringValue(HKLM64, RegKey2, 'UninstallString', UninstStr);
    Result := True;
  end
  else if RegKeyExists(HKCU, RegKey2) then
  begin
    RegQueryStringValue(HKCU, RegKey2, 'DisplayVersion', InstalledVersion);
    RegQueryStringValue(HKCU, RegKey2, 'InstallLocation', ExistingInstallDir);
    RegQueryStringValue(HKCU, RegKey2, 'UninstallString', UninstStr);
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
  end
  else
  begin
    // 檔案層級後備檢查
    CandidateDir := ExpandConstant('{autopf}\{#MyAppName}');
    if FileExists(AddBackslash(CandidateDir) + '{#MyAppExeName}') then
    begin
      ExistingInstallDir := CandidateDir;
      if FileExists(AddBackslash(CandidateDir) + 'unins000.exe') then
        ExistingUninstallExe := AddBackslash(CandidateDir) + 'unins000.exe';
      InstalledVersion := '{#MyAppVersion}';
      Result := True;
    end;
  end;
end;

procedure InitializeWizard();
var
  PromptMsg: string;
  VerComp: Integer;
begin
  IsRepairMode := False;
  IsReinstallMode := False;
  IsUpgradeMode := False;
  IsAlreadyInstalled := DetectExistingInstallation();

  if IsAlreadyInstalled then
  begin
    if InstalledVersion = '' then
      InstalledVersion := '1.0.0';

    VerComp := CompareVersion(InstalledVersion, '{#MyAppVersion}');

    if VerComp < 0 then
    begin
      // 升級更新模式 (Upgrade Mode)
      IsUpgradeMode := True;
      PromptMsg := FmtMessage(CustomMessage('UpgradePrompt'), [InstalledVersion, '{#MyAppVersion}', ExistingInstallDir]);
      if not WizardSilent then
      begin
        if MsgBox(PromptMsg, mbConfirmation, MB_YESNO) = IDNO then
        begin
          ExitProcess(0);
        end;
      end;
    end
    else
    begin
      // 相同版本或較新版本：詢問是否重新安裝或維護
      PromptMsg :=
        '偵測到您的電腦中已安裝 StreamForge (版本: ' + InstalledVersion + ')！'#13#10#13#10 +
        '安裝路徑：' + ExistingInstallDir + #13#10#13#10 +
        '請問您是否要重新安裝 StreamForge？'#13#10#13#10 +
        '• 點選【是 (Yes)】：進入安裝精靈進行重新安裝或維護'#13#10 +
        '• 點選【否 (No)】：取消並退出安裝精靈';

      case ActiveLanguage of
        'english':
          PromptMsg :=
            'StreamForge (v' + InstalledVersion + ') is already installed on your system!'#13#10#13#10 +
            'Install Location: ' + ExistingInstallDir + #13#10#13#10 +
            'Would you like to reinstall StreamForge?'#13#10#13#10 +
            '• Click [Yes]: Proceed with reinstallation or maintenance'#13#10 +
            '• Click [No]: Cancel and exit setup';
        'chinesesimplified':
          PromptMsg :=
            '检测到您的计算机中已安装 StreamForge (版本: ' + InstalledVersion + ')！'#13#10#13#10 +
            '安装路径：' + ExistingInstallDir + #13#10#13#10 +
            '您是否要重新安装 StreamForge？'#13#10#13#10 +
            '• 点击【是 (Yes)】：进入安装向导进行重新安装或维护'#13#10 +
            '• 点击【否 (No)】：取消并退出安装向导';
        'japanese':
          PromptMsg :=
            'コンピューターに StreamForge (v' + InstalledVersion + ') が既にインストールされています！'#13#10#13#10 +
            'インストール先：' + ExistingInstallDir + #13#10#13#10 +
            'StreamForge を再インストールしますか？'#13#10#13#10 +
            '• [はい (Yes)]：再インストールまたはメンテナンスを続行'#13#10 +
            '• [いいえ (No)]：インストールをキャンセルして終了';
        'korean':
          PromptMsg :=
            '컴퓨터에 StreamForge (v' + InstalledVersion + ')가 이미 설치되어 있습니다!'#13#10#13#10 +
            '설치 경로: ' + ExistingInstallDir + #13#10#13#10 +
            'StreamForge를 재설치하시겠습니까?'#13#10#13#10 +
            '• [예 (Yes)]: 재설치 또는 유지 관리 진행'#13#10 +
            '• [아니오 (No)]: 설치를 취소하고 종료';
      end;

      if not WizardSilent then
      begin
        if MsgBox(PromptMsg, mbConfirmation, MB_YESNO) = IDNO then
        begin
          ExitProcess(0);
        end;
      end;
    end;

    // 自動預填既有安裝目錄
    if ExistingInstallDir <> '' then
      WizardForm.DirEdit.Text := ExistingInstallDir;
  end;

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
    if (not IsAlreadyInstalled) or IsUpgradeMode then
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
    
    // In repair or upgrade mode, preserve existing config if present
    if not ((IsRepairMode or IsUpgradeMode) and FileExists(ConfigPath)) then
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
    end
    else if IsUpgradeMode then
    begin
      MsgBox(CustomMessage('UpgradeFinished'), mbInformation, MB_OK);
    end;
  end;
end;
