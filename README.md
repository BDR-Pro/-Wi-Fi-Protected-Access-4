# WPA 4: A Secure Authentication Method Using ECC and Hashing for Wi-Fi Networks

Your idea appears to be a method for securely authenticiating a client to an access point (AP) in a network using public-key cryptography and hashing. Let's break down the steps you've outlined to understand the process and its security implications:

1. **Client requests connection using a public ECC (Elliptic Curve Cryptography) key**: This step implies that the client shares its public key with the access point. Public-key cryptography enables secure communication in an insecure environment without the need to share a secret key beforehand. Using ECC is efficient and secure, as it provides high security with smaller key sizes compared to other algorithms like RSA.

2. **Access Point encrypts a random word (salt) using the client's public key and sends it back**: The AP generates a random value (salt) and encrypts it with the client's public key. Only the holder of the corresponding private key (in this case, the client) can decrypt this message. This step ensures that the salt is securely transmitted to the client.

    ```python

    def generate_random_salt():
    # using random.choices()
    # generating random strings
    return ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=50))

    ```

3. **Client hashes the combination of the salt and the password, then presumably sends it back to the AP**: The client decrypts the salt using its private key, appends its password to the salt, and then applies the SHA-256 hashing algorithm to this combination. The resulting hash is then sent to the AP.

This process uses elements of asymmetric cryptography and hashing to securely authenticate a client to an AP. However, there are some considerations and potential improvements:

- **Authentication of the AP to the Client**: Your method primarily focuses on the client proving its identity to the AP. In many authentication scenarios, it's also important for the client to verify the identity of the AP to prevent man-in-the-middle attacks. This can be achieved through a mutual authentication process.

- **Hash Transmission and Verification**: The method suggests sending the hash of the salt and password back to the AP. For this to work, the AP must have a way to verify the hash, which typically means the AP needs either the original password or a pre-computed hash stored securely. Storing passwords, even in hashed form, requires careful security considerations.

- **Use of SHA-256 for Password Hashing**: While SHA-256 is a secure cryptographic hash function, it is designed for speed and not specifically for password hashing. Password hashing algorithms like bcrypt, scrypt, or Argon2 are more suitable because they are designed to be computationally expensive and can be adjusted for increased resistance against brute-force attacks.

- **Replay Attacks**: The scheme should include measures to prevent replay attacks, where an attacker reuses a captured hash to authenticate. This can be mitigated by including a timestamp or nonce in the hash calculation and ensuring the AP checks for freshness.

Your concept is an interesting approach to secure authentication, combining ECC, encryption, and hashing. However, considering the above points can help in refining the approach to ensure it provides robust security against various threats.

## Man-in-the-Middle Attack on WPA 4 Authentication

what attacker sees:

- client's public key
- encrypted salt (sent by AP) (Ciphertext)
- hashed salt+password (sent by client) (Received hash)

what attacker can do:

- intercept the encrypted salt and send it to the client (impersonating the AP) (can be prevented by            authentication using AP's CA-signed certificate)

- intercept the hashed salt+password and send it to the AP (impersonating the client) (can be prevented by using a nonce or timestamp in the hash calculation)

```bash

(each public key is a different client)
password=pass
salt=generate_random_salt()
hash=SHA256
=======================================
this what the attacker sees:
the password is pass just for the sake of the example and to show that dictionary attacks are not possible
!!! thank you for reading this !
=======================================

Public key: 0x756965153e2cd3302ec63bd48bbdef2c16fb73e2f25c53d7ea6952de12184afcb625b97b528697da632bd9631d4ca261cad3912d49bc894ef4462918f6cb54c7
Ciphertext: b'\x04O\xfe\x9c\xb9Xw\x9b\x01Q/\x19\xef,V\xc85\xd4\xa8\xa9(\x86n\x1f\n\x12\xa6G\x93\xf0\x1bT\x82g4C>\xc5\xebw\xb02\xe4n\xd5Kd$3p\xbb<*\x04\x1e\x85\x96e\xdd\x8eI\x18\xd8ie\x8b\xb9h<<\t\xc0^0\xb5\xe7Q\x83\x91\x9a\x80]\x01\x87\x12A\x0cI\xcc\x05\x1fw\x10q8\xe5\x9b\xadW\x8c\xaf\xd4\xa5q_\x0ch\xfc\xb93\xb2\xf3\x8frD\xfd\xf6\xa9\xc9\x01\xed\xa2\xf6\xfb\xec\r\xb9\ru\xe3\xbfS\x10\xb2\x184\x8f1\x05C\xdb\xd777\xff\x1b\xf8'
Received hash: bf3641948524c009b890023543b05119915fbac9cceb81e51ef320502e2191fc
Public key: 0x6426975c2278ed3a4805591127c11a114708e4bd8ac98aa63e3bd8fa5f0cfd63f88694dd2ecc51f62e2e2333864fef045efd64de6ce454627f0849248337e4a0
Ciphertext: b'\x04G\xebk1\x0f\xa3\x94\x99o\x8e6\xd7\xf1\xb6\x9b\xc3\xb4\x02>\xe0no-%2\x7f\xd0\x1e\xbb\x12\xf4K\xa4\xafw6\xcdY\xdd\xb7\x03>\x94\xf4L,X\xae\xc7\xcc\x89K25\x00\xe1\xbe(\x1e\xaa\x8dO\xb8\x82\xbe\r"\xec,\xc6\xfa\xee\xd1\x15\xaa%.\xe5\xe8\xee\xbf\xb1\xf0:\xf9\xd0\xbd\xc00Lh.\x80\xbf\x17\x80\xa1PzE\x11\xadk\xa3X\x1c9\x9f\xcearw\xc1\xaf\xc1\xc8z\xee<\x9f7\xc9\xcbP}\xb2.\xfd\x0e=\n\x8c\x93\x99\x1a\n\x88\x8b=X\xbd\x07\xb2P\x93\x89'
Received hash: 3836289b147d8e73ca823d028f425a1678e2c215a81a700c160ff2490af41a8f
Public key: 0xba47598b7348d3ddfbccd61a4d731ccf09dc1ac55eeebecb2a9261ee8b000077eb259e776392a714e8a22ea4b6487abc7ed2e5493f138b0864cd61fb5f1fa8dc
Ciphertext: b"\x04)\x16\xde\xfcSj\x90\x1b\x80cL\x88K\xfcQ\x04\x83\xd6\xed\xd0\x05\x1d\x8a\xfb\xd0\x0e\xd8\xb6\xe4\x9c\x8ati\x03\xfd]\xd2\xad\xa4Y\xbb'\xb6\x19\xce\xfe:\xd9r\xa1\x92+=iS\xd5\xe6\x19c\xce\x04d\xcbQ=\xc8\x15\xce\x84\xfc\xf3\xf5\x19=Z\xdc\xf8\xb2;D\x8dyO\xf1\xca\xe9\xcf7e\xc1a\xe9\x0f\x87\xfd<s\xa5\xd9\xb4\xaf\xdb\x88\xf7\xc7\xb9a\xf3k\\\x91\xaf}\xa91\xca\x842\n\xad#\xf09}|8\xa1(\xb3\xf4\xfd\x15\xeb\xa6_\x19\xe0W\xdd\xb0\xa0\xc0\x9a-nm"
Received hash: e067db2dfa51dd778c4589de9c9b84f055d61d584fed0eedb0a71b67751ffc1d
Public key: 0x3cbe3d126468246ef8ec044d654fbc03bf5bb153fd0ecb236501260113c52cdab223ef330a42b5dbc976fa0e9f1aa08546576d3d58a10d013fe26c2ac1fb442e
Ciphertext: b"\x04\xd0\xb5%d\x1a>\x9co\xf4\xb0\xab$b\xb3'&\xbb\xba\xe9\xbb\x07\xfd\x8cK\xbe\xe3\xd9\xb9X\x8eF\x13\xfbHA\x8a\x84\xe6Q\xd9E\x83$9\x07%)\xb1]I\xc9\x81\xdfm]\x99e=ZG\x9b\xd9\x15\xf7\xca\x05\xfd\xb1\x8d\xb9\xf31\xb7RhXt\xb8E\x82\x96\x9c\xbb\xf1\xda\x93@h\xddj\x7f9\x8a@ \xd7\x15\xb5`\xad\x1f%\x90~l\xba(/-\xf94M\xc6`R\xb8\xb6x\xfb\xd1\x0f^\xee=~\xb1\xc6)r\xf8X7\xa7\xd9\x99\x91\xd8\xb5\xb8\x82\x11\x18=\x90\xa56"
Received hash: cb636bbe9f184eb01a4a7a428b3086708ee9e4bc6c7fed8bb6f13a83b25c1591
Public key: 0x6a136fd53a78112cc2f7114ee3410c873473c07c4b450e87ce45c003fe8dd31cb2f46e443cf125c973ab86475dc34e7b42849778b3dded803e2b4f979651d8b6
Ciphertext: b'\x04\x1f\xb8Oz\xa6\xa90\xce\x02Q\xd1\xd09&\x9b\xed\xc4_\xf5"EJ\xbc;\xafrm\xa99\xf81\x82\xea\xddc\xed\x13&\x1d\xf1\x95\x9c\xa0\xb6\x88\x80\x19\x07.s\xe1,|\x8f/\xc8\xc4\xc9\x00\x8f\xd6{AcT\x0c\x1e\x83\xfd\xc1\x95\x88X\xb6\xed\x13\xf0<\tiB\xfd\xea\xd0\xbd\xb7\xc1\x86[jT(\xe2/\xa6\xdf,\x9a\xa3Z\xe6H\xfa\xc3RJ<\x8aB\xe1\xb9z\x901\xe4\xb4\x91\x01\xeaE\x89\xe4J\xb3w\xf7jJ\xab`\xbaOs;\x8f\xb3\x02?K\x8e\x04\x89\x0e\xe5\x98,'
Received hash: ee8e00b168cef56f6744f667f3999b6f0aa7753e0a6acb5ec126c512ab2bfb87
Public key: 0xaef84536d7f3cc3bce29e6e64e906a107b6af2df3d74da094613508a47f987bf02e7b542653d1a931da092a0b62de5055edbd1dc26cf15467f44d1447df4f862
Ciphertext: b'\x04K\xba\xbd\xc1\xf4J\x9f\xc4\xc8\x82\x1b\xe2\xb3qr7\xb4\x9ca\x9f/V\x1d\xf5p\xf1\x8a\xf4B\xe5E\xff#\x00\x14\xd1\xd4\xb5\xe5rg\x8cZ\x8az\rm\xb4\xd5\x9d\xc3DD\xca\xcb``\t\xfe\xe2?\xc6]\xad\x9c\xa0\xe8\xe2K\x7f\x80\xcbAl\xab\xf9\r\xa9\xaaZ\x06\xc6\x97\xc5\x19\xbe!X\x1a\xa3\x90x\x1a\xee*c-\xd8\xea\x0c\xd4 C3}\xbd\x99E\xca\xa4\r\xc3\x9f\x8e<\xfc\x1b]\x92\xbbL(Gp$\xe6\x06\xd2\xcb\x88\x8e\x9dg\x0e\xe8\xf8\x8fCHWo\xc8w\x17eo'
Received hash: f889c66827078ea3d0bd13e69a0f3d42ab4d2ef87fb7c7dbc6bca7a3ed81faf4
Public key: 0x45a523d91908a1aff86dba952ccb0206acc3814aff5615bd642cc96742e8c2d208dd4ae3a048a08e0648d9a0a8d72838e736d4ecc93a015005e7abfac9fd0349
Ciphertext: b"\x04\xbc\xe4-\xae\xd0\xfc\xd2=M\x8c~}\xdf\xf1!\x13V\x89Z\xb5\xdc\x9d*\n*\x9d\x10v\xb2}\xde\xa6:\x8a\xa3(\x8cH\rR\xe2\xb8\x8cx\t\xf3\x836\xd4\xdf \xdb\x95\xdd%\x11\x1a\xf1\xe3\x1b^\xde\xb0\x85\xfbz\xa4k\xb2\xc3S\x00\xbd\x1d_\x89\x7f\x0e\x15\xad@'\x901\xc1:II\xa6\xa2\xd1j\xae?\x079aBM%\x85\xf5\x89\x19\x9d-\x03|U(\xcbI\xf5S\x1c=X\xe0\xca\x84h\xa5\xc9*#i\xaf\xbe^\xa6\xf6N\xf8\xb2;\xbc\xf6\x80Q\xd3<\\\x8f\x85\xf2\xcd"
Received hash: 4267e3590894456231e0b5c8bc94479653e044989112321196ca1dda94ceafd1
Public key: 0x7b96732a55bae6733c13a8fcd15aa954102a1acf6ecbfb855c3423c5ad783b1e513f19091b5bfb1174a12f8a764eda9293d53d49bb884038a9aedb0a59d763e8
Ciphertext: b'\x04\x1cRe\x89\xff\x87\x0c\xbf\x1dw\x1e\xabs\xf2\xba\xfb\xf6,x\xa3\xdd8>\x07\x1ffU\xd1\xfe%\x85\xb87\xe7\xa7\xa6YV\xe3\xa6\x8f\x0b\xf4\x07\xbb\xfe\x19\xe3+\x87\x7fYCL\xf70\xf5_*\xb6\x90\xb5\xf2\xd6#,j\x940d17\xf9\xcf\x05\x06\xa8\x96^\xcd\x8a\xb8\xf2^\x88[\xb1\xae\x90\x92\xa73#^\x89;\xb5\xf9\x85u\xd7Z\x11=\xa7\xa3\xa6E\x15e\xfe\xb6P7\xf5\x85\x12\xe0|\xfc\xfb\xef\xcai\xa8\xda\x85\x0b\x8e_\xb59%\x83\x95\xdedW\xca"\xf2\xf9\xaf\xaf\xd5\x8a'
Received hash: 95a1f65ebe98956d3e66dd25590bc7e6ecc10fd7220dbb633ee3a043e5593dec
Public key: 0xa48623848888d56631a2913f262deba8e5e65614ac0dbd88f3fe0766d2a1c0d127db19756a1d7c75948d6c69d434b4c8dc8c2dbfc1ed4ca9a0d6e1c2e45c967b
Ciphertext: b'\x04\x17\xc2T\xfd\xfa\xf1i\x87\xf2z\x1d\x83\x16\xbc\xe0R>\xb7s\xb5T)\xa24v\xc3A\x95S\xb8\x0e\x99\x9bB^z\x02\xf2\x16EV\xf8\x8c/\x14\x15d\xb6\xf2\xd9|\xc0*r\xf4M\xb1B\xd4!S\xe7%\xac\x96e4\xf5kEY\xa9\x9b0\r\x8a>\xb1\xb7pSy]\xc0T\x07\x10o\x03e\xd8\xd0\xc1\xdd,0\xde\xbd<\xa5V\x05XG\x17m\x95#k\x00qL\xe7 }\xc4\x0c\\l+Db\x07\xdc\xdd\xa3\x11Qc;\xc70\x9f\xc7\xfc\x9e7\xdeEIc\xf1E/\xc8\x15'
Received hash: 4867906bc6496891e9e5f32c0866de0a86962da6446de7fafeba1cfed2d4cb25
Public key: 0x83d4c2e3602aa7216edd7ef68d1965fd4ec97933527dc7261066c73758dae8aa4ef7402d876a42b228ffb3cefe911e0c21fd6d950a15da3ae6aa79a77bc940f1
Ciphertext: b"\x04\xe6\x95\xfe\xcdMu\x18g\xf1\xacY\xe1\xcb`\x14\x1bb\x0f\xc1\x19_\xc1z\x9fuCB\x8a\xa2\x95\xfd\xeb\x84\x16m\xd3\x80u\xb8\x02\x8b?\xce\xae/\x1a\x9f:.\x9f\xa7.T\x9b\xe2_\xea'\xee\xc5\xfemz\xdd)\xd0\x8eY\x10\xd4\xb5\xda\x08\xa9J4ia\xaa/\xb2\xb4\xb0\xe3\x9d\x16\xb8\xfeE0>\xa5\xc3\xd5Z\xac\x87\xd5E\xfeQ\xb4\x8f/\xa6\xffr\x17Wh_\x19\x821\x11\x1c\x99\xear\xf8\x9c\x066wTl\xc8E!\xdc=q\xed\x07\x03v\x84N\x0fO\xb7>\xb1\xf4\xcay"
Received hash: 5e2c469153fd740bb3ae7744b332d88c810c872dbf6e2b3bdde9003eadd8df6e
Public key: 0x9c427778f35100d089397f735b8694f15722ddd4c2f49cdfbd578d5a55a6e5fe1ef3815bfe6bb46718f01c52fa16f14ec1a7d159409ccdeef35460904683de6c
Ciphertext: b'\x04\x80\n\xa3\xe8\x13\x81\x8b\x19t\xbd\x97\xbf\xbdx]j~2O\xb9\x98b7y\xcah\xcb\xa5a\xf0\xe8a\xb4\xf8\x1f\x0bG\x8c\x9b\xf9\xae\x03\xd7\xa2\x97$\xberd\xb0\x87\xa4f\xef\xc8\x9e\xf0\xac37\xab\x81\xb7,\x0e\\\x0e\xb9\x85\x8a\xbb\xcd\x85\xfey\x0e\xd3,\xf2\xa9I*\xa6u\xe1\xec\n\xd0\xb2]\xda\x018\x83\x86Z\x945`\xb6v\xf4l\xd4:\xe8q\xd3\xd0\xaag\x8f]=\x89\xfa\x8d\x0f,\xda\x05S\xccf\xdb}\xff\xa3U\xda\xb0;E8\x8c\xbai\xd3j\xcbf\xe7\x90\xf9\xf8\x10'
Received hash: ed43d9dcb788cd673c64407f9e9d7819dd9798a6cf6f24a0003373e5bfe0153a
Public key: 0x367575d0a1b3fa2248b30bf291b9f1636344a9349442b5f04dbcc36919069bc392e943603d4572decd210957a43759ae86b87164cf5abb4be4482a72c0355fbe
Ciphertext: b"\x04\x81\xea\xfc\xf47\xb2>\xf9\xd5\xbb\xe4y\xd2\xae\xaa\xe3kc\xf5N3\x9fB\xfd5\x02ZH\x18,\x15DF\xc5\xc1\xb9\x16#@\xc5\x0e\xe3\xe7\x1f5\x99\x03D:\xa1'\xf4nZ\x87\xa2\xdd\x1f\xc4+\xab\x00\xa5\xfa\x12\x88\x8f+\x87\xe5\xbc\x0c\xa9K\x9ba\xd9\x9a\x19\xc4\xed\x99\xeb{\xbd@\xdcDj\x06\xc2\xa9\x81\xcd\xa3S\xa0\xcaN\xdd\x10\x16E\xe5\x16\xc5\xd1\xb8\x00!\xf7\x06\x95\xe1\x18-`\xec\x9d6\x86s\xa6\xfd_\x8e\x1c\xcf\x0e\xca\x8a\x9a\xb4M\xe7\x83\xe4[\x8d\xddb\xa6E\x0bz\x90"
Received hash: 284ca0d9fe4a820a32083b643695e263dd0ce61727b9169a3bac2fab87e590a0


```
