Selkie
=============
```
 _______ _______        _     _ _____ _______
 |______ |______ |      |____/    |   |______
 ______| |______ |_____ |    \_ __|__ |______
```

Selkie is a python library that mimics different browser fingerprints. It can be used to scrap web pages that require unique vists based on browser fingerprints. It focuses to act like humans with different random fingerprints.

Selkie is built on webkit for pyqt. Uses Spynner python library as base.
Dependencies
-----------------

  * `PyQt > 4.4.3 <http://www.riverbankcomputing.co.uk/software/pyqt/download>`

Install
----------------
    git clone https://github.com/rohit-dua/selkie.git
    cd selkie
    pip install -r requirements.txt

Usage
---------------
```python
import selkie
driver = selkie.Driver()
fingerprint_cookiejar = selkie.FingerprintCookiejar()
driver.get('http://example.com', fingerprint_cookiejar = fingerprint_cookiejar)
```
Each unique fingerprint can be saved as string.
```python
fingerprint_cookiejar = selkie.FingerprintCookiejar()
save_fingerprint = fingerprint_cookiejar.to_string  #save as string

fingerprint_cookiejar.from_string(save_fingerprint) #load from string
```
Fingerprint can be explicitly randamized.
```python
driver.randamize_fingerprint()
```