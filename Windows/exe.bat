g++ src\WN_S.cpp -o src\WN_S && src\WN_S
ECHO WN_S ejecutado

g++ src\WN_G.cpp -o src\WN_G && src\WN_G
ECHO WN_G ejecutado

g++ src\WN_RELATIONS.cpp -o src\WN_RELATIONS && src\WN_RELATIONS
ECHO WN_RELATIONS ejecutado

pip install -r requirements.txt

py src\WN_SOrden.py
ECHO WN_SOrden ejecutado

py src\WN_GOrden.py
ECHO WN_GOrden ejecutado

py src\WN_RELATIONSOrden.py
ECHO WN_RELATIONSOrden ejecutado

pause
