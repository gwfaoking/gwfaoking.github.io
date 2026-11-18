# MOA All-in-One Privacy Policy

Effective date: November 18, 2026

MOA All-in-One ("the app") is a tool for opening, editing, compressing and encrypting the files on your phone. The app has no sign-up, the developer runs no server for it, and it never sends your information to the developer or sells it to anyone. This policy explains what the app accesses and how that information is handled.

## 1. Information sent to the developer

None. The app contains no advertising, analytics or crash-reporting tools, and the files, contacts and settings it handles never leave your phone for the developer.

## 2. What the app accesses and why

All processing happens on your phone.

- **All files access (storage)**: used by the file explorer, the document/image/music/video viewers, compression and extraction, and encryption/decryption in the secure folders and secure gallery. The app only reads and writes files you choose or open.
- **Contacts (read and write)**: when you run a contacts backup, the app reads your contacts and saves them to a password-protected backup file (.moac); when you restore, it writes the contacts from that file back to your phone. Backup files are saved only where you choose.
- **Music and audio**: used to list the music stored on your phone in the music library.
- **Notifications**: used for playback controls and compression progress/completion.
- **Biometrics**: used to unlock the app lock and secure folders with a fingerprint or face. Android handles your biometric data; the app only receives whether authentication succeeded.

Each permission is requested only after its purpose is shown, either on the first-run permission screen or the first time you use the feature that needs it. If you decline, every other feature keeps working. You can revoke permissions at any time in Settings > Apps > MOA All-in-One > Permissions.

## 3. Information stored on your phone

- **App settings and recent files**: stored inside the app only. Recent-file history can be turned off or cleared in Settings > Recent files.
- **Encrypted files (secure folders, secure gallery)**: encrypted with AES-256-GCM using a key derived from the password you set. The developer never knows your password or key, so a forgotten password cannot be recovered by the developer (password hints and recovery work only on your phone).
- **App lock PIN**: stored only as a non-reversible hash.
- **Passwords entered for compression jobs**: kept encrypted with an Android Keystore key only while that compression job is running.

App data is excluded from Android auto backup (Google Drive backup).

## 4. Internet use

The app uses the internet only when a file you open requires it.

- **Secure mail and HTML mail viewer**: remote images or decryption scripts inside a mail file may contact the server of the organization that sent the mail. Remote images can be turned off in Settings > Secure mail browser. Any information exchanged there is governed by that organization's privacy policy.
- **Document scanner**: the scanner uses the ML Kit document scanner in Google Play services. Scanned images are processed on your phone, but Google Play services may send diagnostic and usage information to Google to provide and improve the feature. See Google's Privacy Policy (https://policies.google.com/privacy).

Ordinary document viewing and the code editor do not access the internet.

## 5. Sharing with third parties

The app does not provide or sell your information to third parties. When you send a file to another app with the Share feature, it goes only to the app you choose.

## 6. Deleting information

The developer stores no information about you, so there is nothing to request deletion of. App data on your phone can be removed completely in Settings > Apps > MOA All-in-One > Storage > Clear data, or by uninstalling the app. Files you created in your phone's storage (backups, archives, encrypted files and so on) remain after uninstalling; delete them yourself if you no longer need them.

## 7. Children

The app is not directed at children under 14 and does not knowingly collect information from children.

## 8. Changes to this policy

If this policy changes, we will announce it through an app update and on this page, and update the effective date.

## 9. Contact

For privacy questions, please email:

- Developer: gwfaoking
- Email: yjpp0921@gmail.com
