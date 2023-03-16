# Django中密码的加密与解密

## 加密

```
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

pbkdf2_sha256

PBKDF2PasswordHasher

    salt 是长度22的random string : 0-9 a-z A-Z
    iterations: 2600000

    func: pbkdf2
    func: hashlib.sha256
    key_func: hashlib.pbkdf2_hmac(sha_256, password, salt, 2600000, 0)
        base64.b64encode(hash).decode('ascii').strip()

password: algorithm$iterations$salt$hash
```

默认配置中使用的hasher是 PBKDF2PasswordHasher.

输入：用户的密码，一个随机的salt(长度22), 迭代次数是260000, 算法是sha256

输出：`{}${}${}${}` 算法，迭代次数，salt，加密后的hash。

可以得到当salt一样时，输出的hash也是一样的。

PBKDF2_HMAC的原理如下：

1. 输入参数：需要提供以下参数：密码、盐值（随机数）、迭代次数、以及使用的哈希函数。
1. 首先将密码和盐值拼接在一起，作为初始的输入值。
1. 通过哈希函数对初始输入值进行哈希运算，得到第一次哈希结果H0。
1. 然后，将H0与密码和盐值拼接在一起，再进行哈希运算，得到第二次哈希结果H1。
1. 重复这个过程，直到迭代次数达到指定的值。每次哈希运算的输入值为前一次的哈希结果，加上密码和盐值。
1. 最终的结果是最后一次哈希的结果，即Hn。
1. Hn就是生成的密钥。由于盐值的存在，相同的密码生成的密钥也会不同，这增加了破解的难度。
1. PBKDF2_HMAC的安全性取决于迭代次数和使用的哈希函数的强度。一般来说，迭代次数越多，算法越安全，但是也会增加计算时间。常见的哈希函数有SHA-256和SHA-512等。

## 解密

```python
self.encode(password, decoded['salt'], decoded['iterations'])
# 该函数使用一种通过避免基于内容的短路行为来防止时间分析的方法，使其适用于密码学。
secrets.compare_digest(force_bytes(val1), force_bytes(val2)) 
```

拿到密码和password_hash.

取出password_hash中的salt和iterations和我们传入的passwd，得出一个password_hash, 然后和之前的passwd_hash相比是不是完全相等。

```python
import base64
import hashlib


def test1():
    ret = hashlib.pbkdf2_hmac('sha256', b'abcdef123456', b'UmSEU7e5ecmD0KPa7t4Zzj', 260000)
    ret = base64.b64encode(ret).decode('ascii').strip()
    print(ret)


def test2(iterations=260000):
    passwd = b'abcdef123456'
    salt = b'UmSEU7e5ecmD0KPa7t4Zzj'

    init = passwd + salt
    h0 = hashlib.sha256(init).digest()

    for i in range(iterations - 1):
        h0 = h0 + init
        h0 = hashlib.sha256(h0).digest()

    ret = base64.b64encode(h0).decode('ascii').strip()
    print(ret)


if __name__ == '__main__':
    test2()
    test2()

```

----

基于内容的短路行为是一种用于防止时间分析攻击的技术。时间分析攻击是一种基于密码系统的运行时间或者响应时间的差异来推断密码信息的攻击方法。

基于内容的短路行为的原理是在密码比较操作中引入一些随机的操作，使得即使输入了相同的密码，计算所需的时间也会随机化。这样一来，攻击者就不能通过密码比较操作的响应时间来推断密码信息了。

具体实现方式是在密码比较操作中，使用一些随机的比较操作来代替固定的比较操作，这些比较操作的结果与输入的密码内容无关。例如，可以在密码比较操作中引入一些随机的比较操作，如随机选择两个比特位进行比较，或者使用随机数对密码进行异或操作，等等。

使用基于内容的短路行为来防止时间分析攻击需要注意以下几点：

1. 随机化操作必须是密集的，以便有效地隐藏比较操作的响应时间。
1. 随机化操作必须是无关的，以免被攻击者用于推断密码信息。
1. 密码比较操作的实现必须在计算时间和随机化操作之间进行平衡，以保持系统的性能。

总之，基于内容的短路行为是一种有效的防止时间分析攻击的技术，可以提高密码系统的安全性。但是，需要注意平衡安全性和性能之间的关系。