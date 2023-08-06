# This is replaced during release process.
__version_suffix__ = '168'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.23.17"
KUBECTL_SHA512 = {
    "linux": "3b1ebf273e48809984cccd8f3a4c999e1f9f1b9a8f91637f4cdef29b0b74408cec3f68898c5c12ef5675f8e4d335100aba765730f0f4cf0d13ee75d28c571bf3",
    "darwin": "5ce19fcaa82dc4794e804650835495aa49ee6edd9509536384804e9aebf29e34a152c077d25605abcac391dfcab6fa98c3b911bb8e7863193f8e62875836315c",
}
STERN_VERSION = "1.19.0"
STERN_SHA256 = {
    "linux": "fcd71d777b6e998c6a4e97ba7c9c9bb34a105db1eb51637371782a0a4de3f0cd",
    "darwin": "18a42e08c5f995ffabb6100f3a57fe3c2e2b074ec14356912667eeeca950e849",
}
KUBELOGIN_VERSION = "v1.28.0"
KUBELOGIN_SHA256 = {
    "linux": "83282148fcc70ee32b46edb600c7e4232cbad02a56de6dc17e43e843fa55e89e",
    "darwin": "8169c6e85174a910f256cf21f08c4243a4fb54cd03a44e61b45129457219e646",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
