import urllib2
def unzip(data):
    import gzip
    import StringIO
    data = StringIO.StringIO(data)
    gz = gzip.GzipFile(fileobj=data)
    data = gz.read()
    gz.close()
    return data

f = urllib2.urlopen("https://kickass.to/movies/")
buf = f.read()
f.close()
print unzip(buf)
