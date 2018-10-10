VERSION=1.1

rmdir /s /q dist
pyinstaller -w sxtool.py
copy /y example*.s?? dist\sxtool
cd dist
( 
    cd sxtool
    del /q Qt5dbus.dll Qt5Network.dll Qt5Qml.dll Qt5Quick.dll Qt5Svg.dll Qt5WebSockets.dll
    del /q _bz2.pyd _hashlib.pyd _lzma.pyd _socket.pyd _ssl.pyd select.pyd unicodedata.pyd
    del /q libssl-1_1-x64.dll ucrtbase.dll VCRUNTIME140.dll MSVCP140.dll libGLESv2.dll libcrypto-1_1-x64.dll
    del /q api-ms-win-core-*.dll api-ms-win-crt-*.dll
    cd PyQt5\Qt
    rmdir /s /q translations bin plugins\iconengines plugins\imageformats plugins\platformthemes
    cd plugins\platforms
    del /q qminimal.dll qoffscreen.dll qwebgl.dll
)
cd ..\..\..\..\..


"C:\Program Files\7-Zip\7z.exe" a sxtool-%VERSION%.zip sxtool\*.*
echo DONE
pause



