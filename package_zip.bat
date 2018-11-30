set VERSION=1.1
set ZIP7="C:\Program Files\7-Zip\7z.exe"
rmdir /s /q dist/sxtool
del /s /q  dist/sxtool-%VERSION%.zip
pyinstaller -y -w sxtool.py || exit /b 1
copy /y example*.s?? dist\sxtool
cd dist\sxtool

del /q Qt5dbus.dll Qt5Network.dll Qt5Qml.dll Qt5Quick.dll Qt5Svg.dll Qt5WebSockets.dll
cd PyQt5\Qt
rmdir /s /q translations bin plugins\iconengines plugins\imageformats plugins\platformthemes
cd plugins\platforms
del /q qminimal.dll qoffscreen.dll qwebgl.dll
cd ..\..\..\..

del /q libssl-1_1-x64.dll ucrtbase.dll libGLESv2.dll libcrypto-1_1-x64.dll
del /q _bz2.pyd _hashlib.pyd _lzma.pyd _socket.pyd _ssl.pyd select.pyd unicodedata.pyd

:: let's keep these, just in case...
:: del /q VCRUNTIME140.dll MSVCP140.dll 
:: del /q api-ms-win-core-*.dll api-ms-win-crt-*.dll

rem Encodings to keep
rem __init__.pyc aliases.pyc latin_1.pyc raw_unicode_escape.pyc unicode_escape.pyc unicode_internal.pyc utf_8.pyc utf_8_sig.pyc
rem Removing other encodings
%ZIP7% d base_library.zip -r base64_codec.pyc big5.pyc big5hkscs.pyc bz2_codec.pyc charmap.pyc cp*.pyc euc_*.pyc gb*.pyc ^
hex_codec.pyc hp_roman8.pyc hz.pyc idna.pyc iso*.pyc johab.pyc koi8_*.pyc kz1048.pyc mac_*.pyc mbcs.pyc oem.pyc palmos.pyc ^
ptcp154.pyc punycode.pyc quopri_codec.pyc rot_13.pyc shift_jis*.pyc tis_620.pyc undefined.pyc utf_7.pyc ^
utf_1*.pyc utf_3*.pyc uu_codec.pyc zlib_codec.pyc

"C:\Program Files\7-Zip\7z.exe" a ..\sxtool-%VERSION%.zip *
cd ..
echo DONE
pause



