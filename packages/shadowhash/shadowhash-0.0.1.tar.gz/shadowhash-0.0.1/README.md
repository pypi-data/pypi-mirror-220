# shadowhash

Generate /etc/shadow crypt hashes. You can see the list and format of hashes in
`man 5 crypt`.

## Usage

By default a [yescrypt](https://www.openwall.com/yescrypt/) hash will be generated (used in latest GNU/Linux):
```
$ shadowhash P4ssw0rd
$y$j9T$t7MgdzAA4NZLiAVe.dLJD/$eKtF1WXeiYj5aJe3pD9eAMkHYXHrLIgYrzL1Juz5aQ2
```

There is option to create other hashes types and send passwords from stdin:
```
$ echo P4ssw0rd | shadowhash -t 5
$5$DZ3bXwsPgopGm0CQ$Rhg3l4OYopgQkH..BNm/MytzVd0n75oj8KAMDvGpA95
```

## Installation

```
pip install shadowhash
```
